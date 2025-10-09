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

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# --- Paths
$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = (Resolve-Path (Join-Path $ScriptDir '..')).Path
$VenvPy      = Join-Path $ProjectRoot '.venv\Scripts\python.exe'
$OutDir      = Join-Path $ProjectRoot 'build'
$AssetsDir   = Join-Path $ProjectRoot 'assets'
$UiDir       = Join-Path $ProjectRoot 'sntb-ui'
$DocsDir     = Join-Path $ProjectRoot 'docs'
$IconPath    = Join-Path $AssetsDir 'scotl_minimalist.ico'
$Entry       = Join-Path $ProjectRoot 'main\__main__.py'
$ExeName     = 'SkyNotesToButtons.exe'

if (-not (Test-Path $VenvPy)) { throw "Virtualenv Python not found: $VenvPy" }
if (-not (Test-Path $Entry))  { throw "Entry point not found: $Entry" }

# --- Version (read from main/__init__.py)
$VersionFile = Join-Path $ProjectRoot 'main\__init__.py'
if (-not (Test-Path $VersionFile)) { throw "Missing version file: $VersionFile" }
$verMatch = [regex]::Match((Get-Content $VersionFile -Raw), "(?m)^__version__\s*=\s*['""]([^'""]+)['""]\s*$")
if (-not $verMatch.Success) { throw "Could not read __version__ from $VersionFile" }
$AppVersion = $verMatch.Groups[1].Value

# --- Clean
if ($Clean -and (Test-Path $OutDir)) {
  Write-Host "Cleaning $OutDir ..." -ForegroundColor Yellow
  Remove-Item -Recurse -Force $OutDir
}

# --- Ensure data dirs exist
foreach ($p in @($AssetsDir, $UiDir, $DocsDir)) {
  if (-not (Test-Path $p)) { throw "Required data directory missing: $p" }
}

# --- Flags
$Flags = @(
  '--standalone',
  '--enable-plugin=tk-inter',
  '--include-package=bs4',
  '--include-package=ttkbootstrap',
  '--include-package=services',
  '--include-package=profiles',
  '--include-package=ui',
  '--include-package=docs',
  "--include-data-dir=$AssetsDir=assets",
  "--include-data-dir=$UiDir=sntb-ui",
  "--include-data-dir=$DocsDir=docs",
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
  '--assume-yes-for-downloads'
)
if ($OneFile) { $Flags += '--onefile' }

# --- Build
$Args = @('-m','nuitka') + $Flags + @($Entry)
Write-Host "Building v$AppVersion (OneFile: $OneFile)..." -ForegroundColor Cyan
& $VenvPy $Args
if ($LASTEXITCODE -ne 0) { throw "Nuitka failed with exit code $LASTEXITCODE" }

# --- Locate result
$ExePath = Get-ChildItem -Recurse -Path $OutDir -Filter $ExeName -File -ErrorAction SilentlyContinue |
           Select-Object -First 1 | ForEach-Object FullName

if ($ExePath) {
  Write-Host "Build OK → $ExePath" -ForegroundColor Green
  Start-Process explorer.exe (Split-Path -Parent $ExePath)
} else {
  Write-Warning "Build finished but EXE not found. Check the build folder."
}
