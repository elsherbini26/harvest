# Harvest Training & Education Center website

Static site, published with GitHub Pages from the `main` branch.

- `index.html` is the English page and `ar/index.html` is the Arabic page. Both are generated.
- To change text, edit `tools/template.html` (English text, with the Arabic in each `data-ar` attribute), then run `python3 tools/build.py`.
- Styles are in `css/style.css`, behaviour in `js/main.js`, images in `images/`.
- When the site moves to another domain, change `SITE` in `tools/build.py` and rebuild.
