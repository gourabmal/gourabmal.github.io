# Gourab Mal — Portfolio

A responsive, buildless portfolio for GitHub Pages. Open `index.html` or serve this folder:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Then visit `http://127.0.0.1:8765/`.

## Pages

- `index.html`: selected work, skill groups, employment history, about, education, courses, awards, and contact.
- `high-quality-meats.html`, `chips.html`, `kenosis.html`, and `first-axis-capital.html`: descriptive project URLs.
- `website-monitoring.html` and `ai-article-generator.html`: additional project details.
- `cartpilot-demo.html`: clearly labeled personal demo, with a click-to-load YouTube player.
- `cv.html`: accessible HTML version of the latest CV, with PDF and Word downloads.
- `thankyou.html`: legacy contact route; directs visitors to email without claiming a message was sent.

## Content and maintenance

`scripts/build_site.py` creates the HTML pages. It reads the current Word CV in `assets/docs/Gourab_Mal_CV.docx` for work experience, courses, and the HTML CV (including its compact skills section). The homepage's full skills inventory is maintained in `portfolio_skills`, combining the CV skills with the original public portfolio's technologies, platforms, and integrations. Other project and homepage copy also lives in the generator. Edit the generator before regenerating; manual HTML changes will otherwise be replaced.

When the CV changes, replace **both** files in `assets/docs/` with the new matching PDF and DOCX, then run:

```sh
python3 scripts/build_site.py
```

The layout and interactions live in `css/portfolio.css` and `js/portfolio.js`. All project images and fonts are local. The font license is included in `assets/fonts/LICENSE.txt`. Older `css/style.css` and `js/index.js` files are retained but are not loaded by the redesigned pages.

## Behavior

- Project filters work in the browser; all projects remain available without JavaScript.
- Mobile navigation supports keyboard controls and Escape.
- Email buttons open the visitor's email app. The copy button reports success or displays the address when clipboard access is unavailable.
- CartPilot loads YouTube only after the visitor presses Play. Its direct YouTube link remains available without JavaScript.
- The site has no message-submission backend, analytics, external font requests, or build dependencies.

## Casual-copying deterrents

The shared stylesheet disables ordinary text selection and image dragging. The shared script cancels right-click menus, copy/cut/selection/drag events, F12, common Inspect/Console shortcuts, View Source, and Save Page shortcuts while the page has focus. Editable fields and the email fallback remain usable; the Copy Email button and explicit CV downloads still work.

These are interface deterrents, not content protection. They cannot stop browser-menu DevTools, disabled JavaScript/CSS, screenshots, source requests, or downloading public assets. Downloaded PDF/Word files and external video frames are outside these controls. No anti-debugging loops, content obfuscation, or crawler blocking are used.

## Publishing

Copy this folder's contents to the existing GitHub Pages repository's configured publishing directory. Preserve the repository's existing GitHub Pages settings. The canonical URLs assume the existing `https://gourabmal.github.io/` domain.

The local redesign does not publish or push to GitHub automatically.

## Search metadata and branding

Every main page includes a unique title, description, canonical URL, Open Graph/Twitter sharing tags, and JSON-LD structured data. The homepage identifies the website and Gourab's professional profile; detail pages include breadcrumbs. `sitemap.xml` lists the nine canonical content pages. The legacy contact fallback is marked `noindex`.

Old `project-1.html` through `project-4.html` URLs are small immediate HTML redirects with canonical links to the renamed pages. GitHub Pages does not support custom HTTP 301 rules, so these preserve old shared URLs on the existing static host. New internal links and the sitemap use descriptive names only.

Brand assets:

- `assets/logo/gm-monogram.svg`: editable, scalable GM logo; PNG export alongside it.
- `assets/favicon/favicon.svg`, PNG sizes, `apple-touch-icon.png`, and root `favicon.ico`: browser and device icons.
- `assets/logo/social-preview.svg` and `.png`: source artwork and 1200 × 630 social-sharing image.

After publication, submit `https://gourabmal.github.io/sitemap.xml` through the site's Google Search Console account and inspect the homepage. Metadata supports discovery and presentation; indexing and rankings are decided by search engines.

References: [Google site names](https://developers.google.com/search/docs/appearance/site-names), [favicon guidance](https://developers.google.com/search/docs/appearance/favicon-in-search), and [profile structured data](https://developers.google.com/search/docs/appearance/structured-data/profile-page).
