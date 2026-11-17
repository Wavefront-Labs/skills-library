---
id: computing-software.web-development.vite.browser-support-targets
name: browser-support-targets
category: computing-software
field: web-development
product: vite
tags: [browser-compatibility, baseline-widely-available, build-target, legacy-plugin]
level: practitioner
status: docs-checked
description: "Understand Vite browser support: esnext in dev, Baseline Widely Available in builds, the minimum targets, no polyfills, and @vitejs/plugin-legacy."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/build.md
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/index.md
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/build-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dev: Vite assumes a modern browser and sets `esnext` as the transform target, so syntax is not lowered.

Production default: `build.target` is the special value `'baseline-widely-available'`, Baseline Widely Available as of a date fixed per major release (2026-01-01 for the docs' current major). It expands to `['chrome111', 'edge111', 'firefox114', 'safari16.4', 'ios16.4']`:
- Chrome >=111, Edge >=111, Firefox >=114, Safari >=16.4

Custom targets use `build.target` (the lowest is `es2015`; `'esnext'` assumes native dynamic imports and does minimal transpiling). Even with a lower target, Vite still needs native ESM dynamic import and `import.meta`:
- Chrome >=64, Firefox >=67, Safari >=11.1, Edge >=79

```bash
vite build --target es2020
```

Gotchas:
- Vite handles syntax transforms only; it does not polyfill. The docs point to a polyfill service that generates bundles from the User-Agent.
- For legacy browsers use the official `@vitejs/plugin-legacy`, which generates legacy chunks plus polyfills, loaded only in browsers without native ESM.
- A relative `base` needs `import.meta` support.

## Checked

Date: 2026-11-07. Read build.md in full (Browser Compatibility section), the Browser Support section of index.md (dev `esnext` transform target, Baseline dates) and build-options.md in full (`build.target` default `'baseline-widely-available'` and its expansion, `'esnext'`). Added the exact default value and expansion. Docs describe the major that uses the 2026-01-01 Baseline date; the pages do not print a version number, so none is claimed.

Method: documentation only; no commands were run.
