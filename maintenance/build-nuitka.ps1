<#  Build Sky: Notes → Buttons with Nuitka (Windows)
    Usage:
      powershell -ExecutionPolicy Bypass -File .\maintenance\build-nuitka.ps1
      powershell -File .\maintenance\build-nuitka.ps1 -Clean
      powershell -File .\maintenance\build-nuitka.ps1 -OneFile   # optional
#>

[CmdletBinding()]
param(
  [switch]$Clean,
  [switch]$OneFile
)

$ErrorActionPreference = 'Stop'

# --- Paths
$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = (Resolve-Path (Join-Path $ScriptDir '..')).Path
$VenvPy      = Join-Path $ProjectRoot '.venv\Scripts\python.exe'
$OutDir      = Join-Path $ProjectRoot 'build'

if (-not (Test-Path $VenvPy)) {
  throw "Virtualenv Python not found: $VenvPy"
}

# --- Version (read from main/__init__.py)
$VersionFile = Join-Path $ProjectRoot 'main\__init__.py'
if (-not (Test-Path $VersionFile)) { throw "Missing version file: $VersionFile" }
$VersionLine = (Get-Content $VersionFile -Raw) -split "`r?`n" | Where-Object { $_ -match '__version__\s*=\s*' } | Select-Object -First 1
if (-not $VersionLine -or ($VersionLine -notmatch "'|`"")) { throw "Could not read __version__ from $VersionFile" }
$AppVersion = ($VersionLine -split '["'']')[1]

# --- Clean
if ($Clean -and (Test-Path $OutDir)) {
  Write-Host "Cleaning $OutDir ..." -ForegroundColor Yellow
  Remove-Item -Recurse -Force $OutDir
}

# --- Common flags
$ExeName   = 'SkyNotesToButtons.exe'
$IconPath  = Join-Path $ProjectRoot 'assets\scotl_minimalist.ico'

# NOTE:
# - Use __main__.py as entry script (no '-m main') to avoid the '-m' option conflict.
# - Hide console with --windows-console-mode=disable (GUI app).
$Flags = @(
  '--standalone',
  '--enable-plugin=tk-inter',
  '--include-package=bs4',
  '--include-package=ttkbootstrap',
  '--include-package=services',
  '--include-package=profiles',
  '--include-package=ui',
  '--include-package=docs',
  '--include-data-dir=assets=assets',
  '--include-data-dir=sntb-ui=sntb-ui',
  '--include-data-dir=docs=docs',
  "--windows-icon-from-ico=$IconPath",
  '--windows-company-name=al2d-x',
  "--windows-product-name=Sky: Notes → Buttons",
  '--windows-file-description=Convert Sky Music HTML to controller/keyboard charts',
  "--windows-file-version=$AppVersion",
  "--windows-product-version=$AppVersion",
  '--windows-console-mode=disable',
  "--output-dir=$OutDir",
  '--remove-output',
  "--output-filename=$ExeName",
  '--assume-yes-for-downloads'  # auto-grab MSVC redist if needed
)

if ($OneFile) {
  $Flags += '--onefile'
}

# --- Build command
$Entry = Join-Path $ProjectRoot 'main\__main__.py'
$Args  = @('-m', 'nuitka') + $Flags + @($Entry)

Write-Host "Building v$AppVersion (OneFile: $OneFile)..." -ForegroundColor Cyan
& $VenvPy $Args
if ($LASTEXITCODE -ne 0) { throw "Nuitka failed with exit code $LASTEXITCODE" }

# --- Result path
if ($OneFile) {
  # OneFile outputs directly under $OutDir
  $ExePath = Join-Path $OutDir $ExeName
} else {
  # Standalone puts it under <entryname>.dist
  $ExePath = Join-Path $OutDir ("{0}.dist\{1}" -f ([IO.Path]::GetFileNameWithoutExtension($Entry)), $ExeName)
}

if (-not (Test-Path $ExePath)) {
  $ExePath = Get-ChildItem -Recurse -Path $OutDir -Filter $ExeName -File -ErrorAction SilentlyContinue |
             Select-Object -First 1 | ForEach-Object FullName
}

if ($ExePath) {
  Write-Host "Build OK → $ExePath" -ForegroundColor Green
  Start-Process explorer.exe (Split-Path -Parent $ExePath)
} else {
  Write-Warning "Build finished but EXE not found. Check the build folder."
}
