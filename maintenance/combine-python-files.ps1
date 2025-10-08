<# combine-python.ps1 — always outputs in its own folder #>

param(
    [string]$OutputFile = "combined_python.txt"
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$OutputPath  = Join-Path $PSScriptRoot $OutputFile  # <— changed line

$SkipFolders = @('.venv', '.git', '.idea', '__pycache__')
$skipPattern = "[\\/](?:{0})(?:[\\/]|$)" -f ($SkipFolders -join '|')
$self = $MyInvocation.MyCommand.Name

"" | Out-File -FilePath $OutputPath -Encoding UTF8  # fresh start

Get-ChildItem -Path $ProjectRoot -Filter *.py -Recurse -File -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -ne $self -and -not ($_.FullName -match $skipPattern) } |
  Sort-Object FullName |
  ForEach-Object {
      Add-Content -Path $OutputPath -Encoding UTF8 -Value "`r`n"
      Get-Content -Path $_.FullName -Encoding UTF8 |
        Add-Content -Path $OutputPath -Encoding UTF8
  }

Start-Process notepad.exe $OutputPath
Write-Host "Combined all .py files into: $OutputPath"
