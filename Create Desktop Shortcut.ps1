$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$launcher = Join-Path $root 'Launch SAO Intelligents App.bat'
$icon = Join-Path $root 'icons\sao-intelligents.ico'
if (-not (Test-Path $launcher)) { throw 'Launcher file is missing.' }
$shell = New-Object -ComObject WScript.Shell
$targets = @(
  (Join-Path ([Environment]::GetFolderPath('Desktop')) 'SAO Intelligents.lnk'),
  (Join-Path ([Environment]::GetFolderPath('Programs')) 'SAO Intelligents.lnk')
)
foreach ($path in $targets) {
  $folder = Split-Path -Parent $path
  if (-not (Test-Path $folder)) { New-Item -ItemType Directory -Path $folder -Force | Out-Null }
  $shortcut = $shell.CreateShortcut($path)
  $shortcut.TargetPath = "$env:WINDIR\System32\cmd.exe"
  $shortcut.Arguments = '/c "' + $launcher + '"'
  $shortcut.WorkingDirectory = $root
  $shortcut.Description = 'Open SAO Intelligents AI desktop app'
  if (Test-Path $icon) { $shortcut.IconLocation = "$icon,0" }
  $shortcut.Save()
}
