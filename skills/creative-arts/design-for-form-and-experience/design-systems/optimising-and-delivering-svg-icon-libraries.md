---
id: creative-arts.design-for-form-and-experience.design-systems.optimising-and-delivering-svg-icon-libraries
name: optimising-and-delivering-svg-icon-libraries
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [svg-optimization, icon-library, svgo, icon-sprite, svg-icons, icon-delivery, react-icons]
level: practitioner
status: draft
description: "Optimise SVG icons with SVGO and deliver an icon library: clean exports, currentColor, sprite or component packages, tree-shaking, accessibility and versioned releases."
sources:
  - "SVGO documentation (svgo.dev/docs)"
  - "MDN Web Docs - SVG in HTML and accessibility (developer.mozilla.org/docs/Web/SVG)"
  - "SVGR - SVG to React components (react-svgr.com/docs)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SVG optimisation and icon library delivery

## Prepare the SVGs
1. **Export clean:** outline strokes only if needed for fidelity; flatten boolean shapes; remove hidden layers, masks and clip paths where possible; viewBox `0 0 24 24`, no fixed width/height.
2. **Optimise with SVGO:** `npx svgo -f icons -o dist --multipass`; with a config that **keeps `viewBox`** (`removeViewBox: false`), removes `width/height`, and replaces fills/strokes with `currentColor`:
```js
// svgo.config.js
module.exports = { multipass: true, plugins: [
  { name: 'preset-default', params: { overrides: { removeViewBox: false } } },
  'removeDimensions',
  { name: 'convertColors', params: { currentColor: true } } ] };
```
Do not strip IDs that the icon needs internally (gradients); prefix IDs to avoid collisions (`prefixIds`).
3. Naming: kebab-case matching design names; one icon per file.

## Deliver
- **React/Vue components** via SVGR (`npx @svgr/cli --icon --typescript icons`), each a named export for **tree-shaking** (ESM, `sideEffects: false`).
- **SVG sprite** (`<symbol>` plus `<use href="#id">`) for static sites; inline or external file with CORS caveats.
- **Icon font** is discouraged (accessibility, blurry rendering, loading).
- Provide `size` and `color` props; default `aria-hidden="true"` for decorative icons; for meaningful icons take `title` and use `role="img"`.
- Publish as a versioned package with a changelog (`creative-arts.design-for-form-and-experience.design-systems.versioning-deprecating-and-changelogging`); document a searchable gallery with names and tags.

## CI
Run svgo and a lint (viewBox, no hard-coded colours, size under about 1 KB) on every icon PR; snapshot-render icons for visual regression.

## Verify
- [ ] viewBox kept, colours replaced by currentColor, sizes small.
- [ ] Package is tree-shakeable; accessibility attributes handled.
- [ ] Gallery and CI checks exist.
