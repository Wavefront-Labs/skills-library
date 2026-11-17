---
id: computing-software.web-development.frontend-development.import-maps
name: import-maps
category: computing-software
field: web-development
product: frontend-development
tags: [es-modules, javascript-modules, import-maps, bare-specifiers, buildless, cdn-modules, importmap-scopes, es-module-shims]
level: practitioner
status: docs-checked
description: "Using import maps for buildless ES modules: mapping bare specifiers, scopes, integrity, cache-busting with hashed URLs, and limits vs a bundler."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/script/type/importmap
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules
  - https://github.com/mdn/browser-compat-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Import maps

**Goal:** write `import { html } from 'lit'` in the browser without a bundler, with versioned, cacheable URLs.

## 1. Declare
```html
<script type="importmap">
{
  "imports": {
    "lit": "/vendor/lit/index.js",
    "lit/": "/vendor/lit/",
    "app/": "/js/"
  },
  "scopes": {
    "/vendor/legacy-widget/": { "lit": "/vendor/lit-legacy/index.js" }
  },
  "integrity": { "/vendor/lit/index.js": "sha384-…" }
}
</script>
<script type="module">import { LitElement } from 'lit'; import { boot } from 'app/main.js';</script>
```
- Trailing-slash keys map prefixes (`lit/decorators.js`).
- `scopes` let one subtree resolve a different version.
- `integrity` adds SRI metadata for module URLs (Chrome 127, Firefox 138, Safari 18 per browser-compat-data).
- The map must be declared and processed **before** any script that imports modules through it. Keep a single map.

## 2. Cache busting
Map logical names to fingerprinted files (`"app/main.js": "/js/main-3f9a2c.js"`) and serve those with long-lived caching; regenerate the map on deploy. 

## 3. Sources of modules
Vendor files locally (no third-party availability dependency) or point entries at a CDN. Pin exact versions in the map.

## 4. Limits
No tree shaking or minification of your own code, many small requests (a deep module graph is still a request waterfall; add `<link rel="modulepreload">` for the critical ones), no TypeScript/JSX without a build. Import maps are supported from Chrome 89, Firefox 108 and Safari 16.4.

## Verify
- [ ] Network panel: every module resolves (no "Failed to resolve module specifier").
- [ ] Changing a file changes its hashed URL and the map; unchanged files stay cached.
- [ ] Critical path waterfall depth is acceptable (modulepreload added where needed).

## Checked

2026-10-26. MDN importmap page (map must be processed before importing scripts; trailing-slash keys for prefixes; `scopes`; integrity metadata map) and browser-compat-data (import maps Chrome 89, Firefox 108, Safari 16.4; integrity Chrome 127, Firefox 138, Safari 18). Removed the unconfirmed Rails/Propshaft, multiple-map, CDN and es-module-shims statements.

Method: documentation only; no commands were run.
