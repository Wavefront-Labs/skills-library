---
id: computing-software.web-development.web-performance.svg-optimisation-with-svgo
name: svg-optimisation-with-svgo
category: computing-software
field: web-development
product: web-performance
tags: [svgo, svg-optimisation, svg, image-optimisation, build-tooling]
level: practitioner
status: verified
description: "Optimising SVG with SVGO: CLI and config, preset-default plugins, keeping viewBox and ids, inline vs file trade-offs, and Vite or webpack build integration."
sources:
  - https://svgo.dev/docs/introduction/
  - https://svgo.dev/docs/preset-default/
  - https://github.com/svg/svgo
  - https://jakearchibald.github.io/svgomg/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SVG optimisation with SVGO

Exported SVGs from Figma, Illustrator or Sketch carry editor metadata, redundant groups, excessive precision and inline styles - savings depend on the exporter (check the byte count before and after).

## 1. CLI
```bash
npx svgo -f src/icons -o dist/icons --multipass
npx svgo logo.svg -o logo.min.svg
```
SVGOMG (web UI) is good for one-off files and seeing what each plugin does.

## 2. Config (SVGO v3/v4)
```js
// svgo.config.mjs
export default {
  multipass: true,
  floatPrecision: 2,
  plugins: [
    { name: "preset-default", params: { overrides: {
        cleanupIds: { minify: false, preserve: ["gradient-a"] },  // keep ids referenced by CSS/JS or <use>
        // inlineStyles / mergePaths can break animations - disable if needed
    } } },
    "removeDimensions",               // drop width/height, keep viewBox for responsive scaling
    { name: "removeAttrs", params: { attrs: ["data-name"] } },
  ],
};
```
- SVGO v4 (run on 4.1.0) no longer runs `removeViewBox` or `removeTitle` in `preset-default`: viewBox and `<title>` survive. SVGO 3.3.2 (run) drops both (the viewBox when it equals width/height), so on v3 disable `removeViewBox` explicitly (`overrides: { removeViewBox: false }`) - without viewBox the SVG can't scale - and keep titles that act as accessible names. `sortAttrs` is already part of v4's `preset-default`, so it needs no extra entry. v4's preset still converts `<rect>` to `<path>` and shortens colours (`#ff0000` to `red`).
- `removeDimensions` makes icons size via CSS; keep `width`/`height` on large illustrations used as `<img>` to avoid CLS.
- Icons meant to inherit colour: replace fills with `currentColor` (`convertColors: { currentColor: true }` or manual).
- `prefixIds` (not in the preset; add it) avoids id collisions when many inline SVGs share a page.

## 3. Build integration
- Vite: `vite-plugin-svgo` or `vite-svg-loader` (Vue) / SVGR (`@svgr/plugin-svgo`) for React components.
- webpack: `image-minimizer-webpack-plugin` with svgo; SVGR runs SVGO by default.
- Commit optimised sources or optimise in build - not both inconsistently.

## 4. Inline vs file
Inline SVG: no request, styleable, but repeated in every HTML page and not cached separately. External `<img src>` or a sprite (`<use href="/sprite.svg#icon">`): cached, can't be styled from page CSS (sprites can with `currentColor`). Large illustrations as files; small UI icons inline or sprite.

## 5. Gotchas
Precision too low distorts small icons (check at 16px); `mergePaths` can change rendering where paths overlap; scripts/foreignObject need manual review (SVG uploads from users should be sanitised, not just optimised).

## Verify
- [ ] Optimised files visually identical at intended sizes; viewBox present; size reduction recorded; referenced ids preserved.
