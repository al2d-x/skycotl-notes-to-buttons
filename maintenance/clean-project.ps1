<# 
.SYNOPSIS
  Clean Python build/cache artifacts in the project and write a report.

.DESCRIPTION
  Removes Python cache/build folders and files (__pycache__, *.pyc, build/, dist/, *.egg-info, etc.)
  Creates a timestamped text report in the maintenance folder.
  By default it COMPLETELY SKIPS .venv/venv (no scanning inside). Use -IncludeVenv to allow pruning there.

.EXAMPLE
  .\maintenance\clean-project.ps1 -WhatIf
  # Show what would be removed, write a report, but do not delete.

.EXAMPLE
  .\maintenance\clean-project.ps1 -IncludeVenv
  # Also clean caches inside .venv/venv and allow deleting those dirs if matched.
#>

[CmdletBinding(SupportsShouldProcess = $true)]
param(
  [switch]$IncludeVenv
)

# --- Resolve paths ---
$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = (Resolve-Path (Join-Path $ScriptDir "..")).Path
$Timestamp   = Get-Date -Format "yyyyMMdd-HHmmss"
$ReportPath  = Join-Path $ScriptDir ("clean-report-{0}.txt" -f $Timestamp)

Write-Host "Project root: $ProjectRoot" -ForegroundColor Cyan
Write-Host "Report will be saved to: $ReportPath" -ForegroundColor Cyan

# --- Targets ---
$DirTargets = @(
  "__pycache__",
  ".pytest_cache",
  ".mypy_cache",
  ".ruff_cache",
  ".ipynb_checkpoints",
  ".hypothesis",
  ".nox",
  ".eggs",
  ".cache",
  "build",
  "dist",
  "*.egg-info"
)

# We only include venvs as deletion targets if explicitly requested.
if ($IncludeVenv) {
  $DirTargets += @(".venv", "venv")
}

$FilePatterns = @(
  "*.pyc", "*.pyo", "*.pyd",
  "Thumbs.db", ".DS_Store",
  ".coverage", "coverage.xml",
  "*.tmp", "*.log"
)

# --- Skip list (never traverse or touch unless -IncludeVenv) ---
$SkipPaths = @()
if (-not $IncludeVenv) {
  $SkipPaths += @(
    (Join-Path $ProjectRoot ".venv"),
    (Join-Path $ProjectRoot "venv")
  )
}

# Helper: path starts with any of $SkipPaths ?
function Test-IsSkipped {
  param([string]$Path)
  foreach ($s in $SkipPaths) {
    if ($s -and $Path.StartsWith($s, [System.StringComparison]::OrdinalIgnoreCase)) {
      return $true
    }
  }
  return $false
}

# --- Collections ---
$RemovedItems = @()
$Errors = @()

# --- Safe removers ---
function Remove-DirSafe {
  param([System.IO.DirectoryInfo]$Dir)
  $path = $Dir.FullName
  if ($PSCmdlet.ShouldProcess($path, "Remove directory")) {
    try {
      Remove-Item -LiteralPath $path -Recurse -Force -ErrorAction Stop
      $script:RemovedItems += [pscustomobject]@{ Type='dir'; Path=$path; Action='Deleted'; Reason=$null }
    } catch {
      $script:RemovedItems += [pscustomobject]@{ Type='dir'; Path=$path; Action='Error'; Reason=$_.Exception.Message }
      $script:Errors       += [pscustomobject]@{ Path=$path; Error=$_.Exception.Message }
    }
  } else {
    $script:RemovedItems += [pscustomobject]@{ Type='dir'; Path=$path; Action='WhatIf'; Reason=$null }
  }
}

function Remove-FileSafe {
  param([System.IO.FileInfo]$File)
  $path = $File.FullName
  if ($PSCmdlet.ShouldProcess($path, "Remove file")) {
    try {
      Remove-Item -LiteralPath $path -Force -ErrorAction Stop
      $script:RemovedItems += [pscustomobject]@{ Type='file'; Path=$path; Action='Deleted'; Reason=$null }
    } catch {
      $script:RemovedItems += [pscustomobject]@{ Type='file'; Path=$path; Action='Error'; Reason=$_.Exception.Message }
      $script:Errors       += [pscustomobject]@{ Path=$path; Error=$_.Exception.Message }
    }
  } else {
    $script:RemovedItems += [pscustomobject]@{ Type='file'; Path=$path; Action='WhatIf'; Reason=$null }
  }
}

# --- Scan & remove: directories ---
foreach ($target in $DirTargets) {
  # Enumerate all directories, but prune anything in $SkipPaths first
  $dirs = Get-ChildItem -Path $ProjectRoot -Recurse -Force -Directory -ErrorAction SilentlyContinue |
          Where-Object { -not (Test-IsSkipped $_.FullName) } |
          Where-Object { $_.Name -like $target }

  foreach ($d in $dirs) {
    Remove-DirSafe -Dir $d
  }
}

# --- Scan & remove: files ---
foreach ($pattern in $FilePatterns) {
  $files = Get-ChildItem -Path $ProjectRoot -Recurse -Force -File -ErrorAction SilentlyContinue -Filter $pattern |
           Where-Object { -not (Test-IsSkipped $_.DirectoryName) }
  foreach ($f in $files) {
    Remove-FileSafe -File $f
  }
}

# --- Summaries ---
$dirDeleted = @($RemovedItems | Where-Object { $_.Type -eq 'dir'  -and $_.Action -eq 'Deleted' }).Count
$fileDeleted= @($RemovedItems | Where-Object { $_.Type -eq 'file' -and $_.Action -eq 'Deleted' }).Count
$dirWhatIf  = @($RemovedItems | Where-Object { $_.Type -eq 'dir'  -and $_.Action -eq 'WhatIf'  }).Count
$fileWhatIf = @($RemovedItems | Where-Object { $_.Type -eq 'file' -and $_.Action -eq 'WhatIf'  }).Count
$errCount   = @($Errors).Count

$mode = if ($WhatIfPreference -or $PSBoundParameters.ContainsKey('WhatIf')) { "DRY-RUN (WhatIf)" } else { "ACTUAL DELETE" }
$successHeader = if ($errCount -eq 0) { "SUCCESS" } else { "SUCCESS (with $errCount warnings)" }

# --- Build report ---
$report = @()
$report += "Clean Report - $Timestamp"
$report += "Mode: $mode"
$report += "Root: $ProjectRoot"
$report += ""
$report += $successHeader
$report += "=============================="
$report += "Deleted:  $dirDeleted dirs, $fileDeleted files"
$report += "WhatIf:   $dirWhatIf dirs, $fileWhatIf files"
$report += ""
if ($errCount -gt 0) {
  $report += "Warnings"
  $report += "--------"
  foreach ($e in $Errors) {
    $report += "$($e.Path) :: $($e.Error)"
  }
  $report += ""
}

$report += "Done."

# --- Write report ---
$report | Set-Content -LiteralPath $ReportPath -Encoding UTF8

# --- Console summary ---
Write-Host ""
Write-Host "[$successHeader] Deleted: $dirDeleted dirs, $fileDeleted files | WhatIf: $dirWhatIf dirs, $fileWhatIf files" -ForegroundColor Green
if ($errCount -gt 0) {
  Write-Host "$errCount warning(s) occurred. See report for details." -ForegroundColor Yellow
}
Write-Host "Report saved to: $ReportPath" -ForegroundColor Cyan
