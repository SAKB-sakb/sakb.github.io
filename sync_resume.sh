#!/usr/bin/env bash
#
# sync_resume.sh
# --------------
# One-command sync: takes the newest .tex and .pdf you've downloaded
# from Prism, updates the website content, updates the downloadable
# CV, and pushes everything to GitHub Pages.
#
# SETUP (one time):
#   1. Edit SYNC_DIR and REPO_DIR below to match your machine.
#   2. chmod +x sync_resume.sh
#
# EVERY TIME YOU EDIT YOUR RESUME:
#   1. In Prism: download the PDF, and download/export the .tex source.
#      Save both into SYNC_DIR (default: ~/resume-sync).
#   2. Run: ./sync_resume.sh
#
# The script always uses the MOST RECENTLY MODIFIED .tex and .pdf
# files it finds in SYNC_DIR, so you don't need to rename anything —
# just save your fresh downloads into that folder each time.

set -euo pipefail

# ---- EDIT THESE TWO PATHS FOR YOUR MACHINE ----
SYNC_DIR="$HOME/resume-sync"
REPO_DIR="$HOME/sakb.github.io"
# ------------------------------------------------

PDF_FILENAME="S_Aditha_Krishna_Bhat_CV.pdf"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> Looking for latest .tex and .pdf in $SYNC_DIR"

if [ ! -d "$SYNC_DIR" ]; then
  echo "ERROR: $SYNC_DIR does not exist. Create it and put your downloaded .tex/.pdf there."
  exit 1
fi

LATEST_TEX=$(find "$SYNC_DIR" -name "*.tex" -type f -print0 | xargs -0 ls -t 2>/dev/null | head -n 1 || true)
LATEST_PDF=$(find "$SYNC_DIR" -name "*.pdf" -type f -print0 | xargs -0 ls -t 2>/dev/null | head -n 1 || true)

if [ -z "$LATEST_TEX" ]; then
  echo "ERROR: no .tex file found in $SYNC_DIR"
  exit 1
fi
if [ -z "$LATEST_PDF" ]; then
  echo "ERROR: no .pdf file found in $SYNC_DIR"
  exit 1
fi

echo "    tex: $LATEST_TEX"
echo "    pdf: $LATEST_PDF"

if [ ! -d "$REPO_DIR" ]; then
  echo "ERROR: repo not found at $REPO_DIR. Clone it first:"
  echo "    git clone https://github.com/SAKB-sakb/sakb.github.io.git \"$REPO_DIR\""
  exit 1
fi

echo "==> Updating index.html content from LaTeX"
python3 "$SCRIPT_DIR/sync_resume.py" "$LATEST_TEX" "$REPO_DIR/index.html"

echo "==> Updating downloadable CV PDF"
cp "$LATEST_PDF" "$REPO_DIR/$PDF_FILENAME"

echo "==> Committing and pushing"
cd "$REPO_DIR"
git add index.html "$PDF_FILENAME"

if git diff --cached --quiet; then
  echo "No changes to commit — site already matches this resume version."
  exit 0
fi

git commit -m "Sync resume from Prism ($(date +'%Y-%m-%d %H:%M'))"
git push origin main

echo "==> Done. Live in a minute or two at https://sakb-sakb.github.io/"
