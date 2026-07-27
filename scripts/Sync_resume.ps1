<#
.SYNOPSIS
    sync_resume.ps1 — One-command sync: takes the newest .tex and .pdf
    you've downloaded from Prism, updates the website content, updates
    the downloadable CV, and pushes everything to GitHub Pages.

.DESCRIPTION
    SETUP (one time):
      1. Edit $SyncDir and $RepoDir below to match your machine.
      2. You may need to allow local scripts to run once:
             Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

    EVERY TIME YOU EDIT YOUR RESUME:
      1. In Prism: download the PDF, and download/export the .tex source.
         Save both into $SyncDir (default: E:\sakb-resume\resume-sync).
      2. Run: .\sync_resume.ps1

    The script always uses the MOST RECENTLY MODIFIED .tex and .pdf
    files it finds in $SyncDir, so you don't need to rename anything —
    just save your fresh downloads into that folder each time.
#>

# ---- EDIT THESE TWO PATHS FOR YOUR MACHINE ----
$SyncDir = "E:\sakb-resume\resume-sync"
$RepoDir = "E:\sakb-resume\sakb.github.io"
# ------------------------------------------------

$PdfFilename = "S_Aditha_Krishna_Bhat_CV.pdf"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "==> Looking for latest .tex and .pdf in $SyncDir"

if (-not (Test-Path $SyncDir)) {
    Write-Error "ERROR: $SyncDir does not exist. Create it and put your downloaded .tex/.pdf there."
    exit 1
}

$LatestTex = Get-ChildItem -Path $SyncDir -Filter *.tex -File -Recurse |
    Sort-Object LastWriteTime -Descending | Select-Object -First 1
$LatestPdf = Get-ChildItem -Path $SyncDir -Filter *.pdf -File -Recurse |
    Sort-Object LastWriteTime -Descending | Select-Object -First 1

if (-not $LatestTex) {
    Write-Error "ERROR: no .tex file found in $SyncDir"
    exit 1
}
if (-not $LatestPdf) {
    Write-Error "ERROR: no .pdf file found in $SyncDir"
    exit 1
}

Write-Host "    tex: $($LatestTex.FullName)"
Write-Host "    pdf: $($LatestPdf.FullName)"

if (-not (Test-Path $RepoDir)) {
    Write-Error "ERROR: repo not found at $RepoDir. Clone it first:`n    git clone https://github.com/SAKB-sakb/sakb.github.io.git `"$RepoDir`""
    exit 1
}

Write-Host "==> Updating index.html content from LaTeX"
python "$ScriptDir\sync_resume.py" "$($LatestTex.FullName)" "$RepoDir\index.html"
if ($LASTEXITCODE -ne 0) {
    Write-Error "sync_resume.py failed — see output above."
    exit 1
}

Write-Host "==> Updating downloadable CV PDF"
Copy-Item -Path $LatestPdf.FullName -Destination (Join-Path $RepoDir $PdfFilename) -Force

Write-Host "==> Committing and pushing"
Push-Location $RepoDir
try {
    git add index.html $PdfFilename

    $staged = git diff --cached --quiet; $hasChanges = ($LASTEXITCODE -ne 0)
    if (-not $hasChanges) {
        Write-Host "No changes to commit — site already matches this resume version."
        exit 0
    }

    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    git commit -m "Sync resume from Prism ($timestamp)"
    git push origin main

    Write-Host "==> Done. Live in a minute or two at https://sakb-sakb.github.io/"
}
finally {
    Pop-Location
}
