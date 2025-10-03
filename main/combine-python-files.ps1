<# combine-python.ps1
────────────────────────────────────────
• Appends the contents of every .py file in the current folder
  and all sub‑folders (except .venv, .git, .idea, __pycache__)
  to combined_python.txt (UTF‑8).
• Adds a clear header before each file’s code, showing its
  relative path.
• Skips itself if renamed with a .py extension.
• Opens the result in Notepad when done.
#>

# --- Config ---------------------------------------------------------------
$OutputFile  = "combined_python.txt"      # File to build
$HeaderLine  = "#" * 70                   # Visual separator
$SkipFolders = @('.venv','.git','.idea','__pycache__')  # folders to ignore
# --------------------------------------------------------------------------

# Ensure the output file exists and start fresh (PS‑5‑safe)
if (-not (Test-Path $OutputFile)) {
    "" | Out-File -FilePath $OutputFile -Encoding UTF8
} else {
    Clear-Content -Path $OutputFile            # remove to “always‑append”
}

# Regex that detects any of the skip folders in a path (handles \ or /)
$skipPattern = "[\\/](?:{0})(?:[\\/]|$)" -f ($SkipFolders -join '|')

# Get the name of this script so we don’t re‑read ourselves if renamed *.py
$self = $MyInvocation.MyCommand.Name

# Root folder for later relative‑path trimming
$root = (Get-Location).Path + "\"            # include trailing slash

# Loop through all .py files, depth-first, skipping unwanted folders
Get-ChildItem -Path . -Filter *.py -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object {
        $_.Name -ne $self -and
        -not ($_.FullName -match $skipPattern)    # skip .venv, .git, .idea, __pycache__
    } |
    Sort-Object FullName |
    ForEach-Object {
        # Add a blank line between files for readability
        Add-Content -Path $OutputFile -Encoding UTF8 -Value "`r`n"
        Get-Content -Path $_.FullName -Encoding UTF8 |
            Add-Content -Path $OutputFile -Encoding UTF8
    }

# Pop open Notepad so you can review the combined file
Start-Process notepad.exe $OutputFile
