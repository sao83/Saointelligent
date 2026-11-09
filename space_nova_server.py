#!/usr/bin/env python3
"""SAO Intelligents local companion server.

Serves the app and provides DuckDuckGo web search. It binds to localhost only.
"""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
MAX_BODY = 2 * 1024 * 1024


class DuckParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.results = []
        self.current = None
        self.capture = None
        self.capture_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = set((attrs.get("class") or "").split())
        if tag == "div" and "result" in classes:
            if self.current and self.current.get("title"):
                self.results.append(self.current)
            self.current = {"title": "", "url": "", "snippet": ""}
        if self.current is None:
            return
        if tag == "a" and "result__a" in classes:
            self.current["url"] = attrs.get("href", "")
            self.capture = "title"
            self.capture_depth = 1
        elif tag in ("div", "a") and "result__snippet" in classes:
            self.capture = "snippet"
            self.capture_depth = 1
        elif self.capture:
            self.capture_depth += 1

    def handle_endtag(self, tag):
        if self.capture:
            self.capture_depth -= 1
            if self.capture_depth <= 0:
                self.capture = None
                self.capture_depth = 0
        if tag == "div" and self.current and self.current.get("title"):
            if self.current not in self.results:
                self.results.append(self.current)
            self.current = None

    def handle_data(self, data):
        if self.current is not None and self.capture:
            self.current[self.capture] += data


def unwrap_duck_url(value: str) -> str:
    value = (value or "").strip()
    parsed = urlparse(value if ":" in value else "https:" + value)
    query = parse_qs(parsed.query)
    if "uddg" in query:
        value = query["uddg"][0]
    elif value.startswith("//"):
        value = "https:" + value
    return value


def search_duckduckgo(query: str):
    query = re.sub(r"\s+", " ", query).strip()[:300]
    if not query:
        raise ValueError("Enter a search question first.")
    url = "https://html.duckduckgo.com/html/?" + urlencode({"q": query})
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; SAOIntelligents/11.0)"})
    try:
        with urlopen(request, timeout=18) as response:
            html = response.read(2_500_000).decode("utf-8", "replace")
    except (HTTPError, URLError, TimeoutError) as exc:
        raise RuntimeError(f"Could not reach the search service: {exc}") from exc
    parser = DuckParser()
    parser.feed(html)
    if parser.current and parser.current.get("title"):
        parser.results.append(parser.current)

    cleaned, seen = [], set()
    for item in parser.results:
        title = re.sub(r"\s+", " ", item.get("title", "")).strip()
        link = unwrap_duck_url(item.get("url", ""))
        snippet = re.sub(r"\s+", " ", item.get("snippet", "")).strip()
        if not title or not link:
            continue
        parsed = urlparse(link)
        if parsed.scheme not in ("http", "https") or not parsed.netloc or link in seen:
            continue
        seen.add(link)
        cleaned.append({"title": title, "url": link, "snippet": snippet})
        if len(cleaned) >= 6:
            break
    if not cleaned:
        raise RuntimeError("The search provider returned no readable results. Try again later.")
    return cleaned


def json_response(handler, status, data):
    payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(payload)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(payload)


class SAOIntelligentsHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt, *args):
        sys.stdout.write("[SAO Intelligents] " + (fmt % args) + "\n")

    def read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length < 1 or length > MAX_BODY:
            raise ValueError("Request is empty or too large.")
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def do_GET(self):
        if self.path == "/api/health":
            json_response(self, 200, {"ok": True, "service": "SAO Intelligents local server"})
            return
        return super().do_GET()

    def do_POST(self):
        try:
            data = self.read_json()
            if self.path == "/api/search":
                results = search_duckduckgo(str(data.get("query", "")))
                json_response(self, 200, {"results": results})
                return
            json_response(self, 404, {"error": "Unknown API route."})
        except ValueError as exc:
            json_response(self, 400, {"error": str(exc)})
        except HTTPError as exc:
            try:
                details = exc.read().decode("utf-8", "replace")[:1500]
            except Exception:
                details = str(exc)
            json_response(self, 502, {"error": "Search service error: " + details})
        except Exception as exc:
            json_response(self, 502, {"error": str(exc) or "The local service could not complete the request."})


def main():
    port = 8790
    server = ThreadingHTTPServer(("127.0.0.1", port), SAOIntelligentsHandler)
    print("SAO Intelligents is running at http://127.0.0.1:%d/space_nova.html" % port)
    print("Keep this window open while using SAO Intelligents. Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping SAO Intelligents.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
