# sakb.github.io

Personal résumé website for **S Aditha Krishna Bhat** — RTL Design Engineer, RISC-V SoC Subsystems.

🔗 Live site: https://sakb-sakb.github.io/

## About

A single-page résumé site styled as a chip floorplan — dark silicon background, copper/cyan trace accents, and a small diagram built from the three real projects on the résumé (IoMMU, AIA, IP Verification/Design Quality).

**Interactive features:**
- Sticky nav with scroll-spy (highlights the section you're currently viewing)
- Click-to-copy buttons on phone and email
- Expandable/collapsible project blocks (click a project header to toggle its bullets)
- "Download CV (PDF)" button — downloads the original résumé PDF
- "Print / Save as PDF" button — opens a print-friendly view of the page itself

## Tech

- Plain HTML + CSS + vanilla JS (no build step, no dependencies)
- Fonts: [IBM Plex Mono](https://fonts.google.com/specimen/IBM+Plex+Mono) / [IBM Plex Sans](https://fonts.google.com/specimen/IBM+Plex+Sans) via Google Fonts
- Hosted with [GitHub Pages](https://pages.github.com/)

## Structure

```
sakb.github.io/
├── index.html                       # entire site (markup + styles + JS in one file)
├── S_Aditha_Krishna_Bhat_CV.pdf     # résumé PDF, served by the "Download CV" button
└── scripts/
    ├── parse_tex.py                 # parses main.tex into structured data
    ├── sync_resume.py               # writes that data into index.html's AUTO markers
    └── sync_resume.sh               # one-command wrapper: sync + commit + push
```

> The filename `S_Aditha_Krishna_Bhat_CV.pdf` must match exactly what's referenced in `index.html`'s download button — if you rename the PDF, update the `href` in `index.html` too.

## Keeping the site in sync with your LaTeX resume (Prism)

`index.html` has HTML comment markers like `<!--AUTO:SUMMARY--> ... <!--/AUTO:SUMMARY-->` wrapped around every piece of résumé content (name, contact info, summary, each project's title/bullets, education, skills). The sync scripts only ever touch text between those markers — your design, CSS, and JS are never touched.

**One-time setup:**
```bash
mkdir -p ~/resume-sync
git clone https://github.com/SAKB-sakb/sakb.github.io.git ~/sakb.github.io
cd ~/sakb.github.io/scripts
chmod +x sync_resume.sh
```
If your repo or sync folder live somewhere else, edit `SYNC_DIR` and `REPO_DIR` near the top of `scripts/sync_resume.sh`.

**Every time you edit your resume in Prism:**
1. In Prism, download the **PDF** and download/export the **`.tex` source**.
2. Save both files into `~/resume-sync` (any filename — the script always picks the most recently modified `.tex` and `.pdf` in that folder).
3. Run:
   ```bash
   cd ~/sakb.github.io/scripts
   ./sync_resume.sh
   ```
4. The script updates `index.html`'s content, replaces `S_Aditha_Krishna_Bhat_CV.pdf`, commits, and pushes to GitHub. The live site redeploys within a minute or two.

**If you restructure your resume** (add a new job, a 4th project, a new skill category), the parser's regex patterns in `scripts/parse_tex.py` — and the matching `<!--AUTO:...-->` markers in `index.html` — will need small updates to match. The script prints a warning listing anything it couldn't find a marker for, rather than failing silently.

## Running locally

No build tools needed — just open the file:

```bash
git clone https://github.com/SAKB-sakb/sakb.github.io.git
cd sakb.github.io
open index.html      # macOS
# or: start index.html   (Windows)
# or: xdg-open index.html (Linux)
```

## Deploying / updating

1. Edit `index.html` with your changes.
2. Commit and push to the `main` branch:
   ```bash
   git add index.html
   git commit -m "Update resume site"
   git push origin main
   ```
3. GitHub Pages redeploys automatically — changes appear at the live URL within a minute or two.

## Contact

- Email: sadithakrishnabhat@gmail.com
- LinkedIn: [s-aditha-krishna-bhat](https://linkedin.com/in/s-aditha-krishna-bhat)
