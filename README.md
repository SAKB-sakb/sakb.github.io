# sakb.github.io

Personal résumé website for **S Aditha Krishna Bhat** — RTL Design Engineer, RISC-V SoC Subsystems.

🔗 Live site: [https://sakb-sakb.github.io/](https://sakb-sakb.github.io/sakb.github.io/)

## About

A single-page résumé site styled as a chip floorplan — dark silicon background, copper/cyan trace accents, and a small diagram built from the three real projects on the résumé (IoMMU, AIA, IP Verification/Design Quality).

## Tech

- Plain HTML + CSS (no build step, no dependencies)
- Fonts: [IBM Plex Mono](https://fonts.google.com/specimen/IBM+Plex+Mono) / [IBM Plex Sans](https://fonts.google.com/specimen/IBM+Plex+Sans) via Google Fonts
- Hosted with [GitHub Pages](https://pages.github.com/)

## Structure

```
sakb.github.io/
└── index.html   # entire site (markup + styles in one file)
```

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
