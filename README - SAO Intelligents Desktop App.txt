SAO INTELLIGENTS — WINDOWS DESKTOP APP PACKAGE

This package opens SAO Intelligents in its own desktop-style app window using Microsoft Edge or Google Chrome. It keeps the current SAO Intelligents 16.2 features and runs the companion Python service locally for web search.

QUICK INSTALL
1. Extract the entire ZIP into a permanent folder (for example, Documents\SAO Intelligents). Do not launch it from inside the ZIP.
2. Make sure Python 3 is installed on Windows. The launcher uses `py -3` or `python`.
3. Double-click `Install SAO Intelligents App.bat`. This creates a SAO Intelligents shortcut on your Desktop and in your Start Menu.
4. Double-click the new SAO Intelligents shortcut. The local service starts and SAO Intelligents opens in a clean app window in Edge or Chrome.

OPTIONAL: INSTALL AS A FULL PWA
1. Open SAO Intelligents using `Launch SAO Intelligents App.bat`.
2. Click the `Install App` button in SAO Intelligents, or use the Edge/Chrome menu and choose Apps > Install this site as an app (the wording may vary).
3. Once installed, the app gets its own Start Menu entry and app window. Keep using the included Desktop shortcut to ensure the local service starts first.

IMPORTANT
- This is an installable desktop-style PWA / browser app package, not a compiled native .EXE installer.
- Python 3 and Edge or Chrome are required. The launcher starts the local server at 127.0.0.1:8790 and opens the app window.
- Keep the extracted app folder in the same location after creating shortcuts. Moving it later breaks the shortcuts; rerun Install SAO Intelligents App.bat if you move it.
- The app uses the browser profile's local storage for accounts, chats, preferences, and local passwords. Use the same browser profile as before if you want to keep data from the earlier SAO Intelligents browser version. If the app opens in a different browser profile, local data may not appear.
- The service worker caches the app shell for offline reopening, but AI models still need their first download. Web search needs internet, and image models may need downloads on first use. The local companion server must start for the app to open from its shortcut.
- Local profiles do not sync between devices and do not have cloud password recovery.

TROUBLESHOOTING
- If the app does not open, install Python 3 and try again.
- If it opens in a normal browser tab, use the Install App button or the browser menu to install it as a PWA.
- If a port error appears, close older SAO Intelligents windows and server processes, then retry. This package uses port 8790.
