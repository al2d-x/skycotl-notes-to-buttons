<# project-structure.ps1 — PS5 compatible, ASCII-only, with excludes
   Place in: project-root\maintenance
   Default: writes output into maintenance\project-structure.txt
   Use -ToRoot to instead write into the project root.
#>

param(
    [string]$Output = "project-structure.txt",
    [switch]$ToRoot
)

$ErrorActionPreference = "Stop"

# Project root = parent of the folder containing this script
$Root = Split-Path -Parent $PSScriptRoot

# Where to write the file
if ($ToRoot) { $OutPath = Join-Path $Root $Output } else { $OutPath = Join-Path $PSScriptRoot $Output }

# Exclusions
$ExcludeDirs = @(
  ".git",".hg",".svn",".venv","venv","env","__pycache__",
  ".pytest_cache",".mypy_cache","node_modules",".idea",".vscode",
  "dist","build","out","target"
)
$ExcludeExt = @(".pyc",".pyd",".pyo",".dll",".exe",".so",".zip",".7z",".rar",".tar",".gz")

function ShouldSkipDir([IO.DirectoryInfo]$dir) {
    return $ExcludeDirs -contains $dir.Name
}
function ShouldSkipFile([IO.FileInfo]$file) {
    return $ExcludeExt -contains ($file.Extension.ToLowerInvariant())
}

function Get-Tree([string]$Path, [string]$Prefix = "") {
    $lines = New-Object System.Collections.Generic.List[string]

    # Include hidden/system; sort: dirs first, then files
    $items = Get-ChildItem -Force -LiteralPath $Path |
             Sort-Object @{Expression = { -not $_.PSIsContainer }}, Name

    for ($i = 0; $i -lt $items.Count; $i++) {
        $item = $items[$i]
        $last = ($i -eq $items.Count - 1)
        $branch = "+--"; if ($last) { $branch = "\--" }

        if ($item.PSIsContainer) {
            if (ShouldSkipDir $item) { continue }
            $lines.Add("$Prefix$branch $($item.Name)/")
            $childPrefix = $Prefix; if ($last) { $childPrefix += "    " } else { $childPrefix += "|   " }
            $childLines = Get-Tree -Path $item.FullName -Prefix $childPrefix
            foreach ($cl in $childLines) { $lines.Add($cl) }
        } else {
            if (ShouldSkipFile $item) { continue }
            $lines.Add("$Prefix$branch $($item.Name)")
        }
    }
    return $lines
}

$lines = @()
$lines += "# Project structure"
$lines += "root: $(Split-Path -Leaf $Root)"
$lines += "generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"
$lines += ""
$lines += "$(Split-Path -Leaf $Root)/"
$tree = Get-Tree -Path $Root -Prefix ""
foreach ($t in $tree) { $lines += $t }

$lines -join "`r`n" | Out-File -Encoding UTF8 -FilePath $OutPath
Write-Host "Wrote $OutPath"
