---
id: computing-software.software-engineering.javascript.js-conditional-exports-dual
name: js-conditional-exports-dual
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, conditional-exports, js-packages]
level: advanced
status: draft
description: "Publish packages with exports conditions import/require/types and avoid the dual-package hazard."
sources: ["https://nodejs.org/api/packages.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Conditional exports and dual ESM/CJS packages

- `"exports": { ".": { "types": "./dist/index.d.ts", "import": "./dist/index.js", "require": "./dist/index.cjs", "default": "./dist/index.js" }, "./package.json": "./package.json" }`; `types` must come first, `default` last.
- `"type": "module"` makes `.js` ESM; use `.cjs`/`.mjs` explicitly for the other format.
- Dual hazard: both builds loaded at once create two copies of state; keep stateful code in one format and wrap the other, or ship ESM only (Node 22 `require(esm)` support is recent: confirm).
- `exports` blocks deep imports not listed; add subpaths intentionally.
- Verify with `publint` and `arethetypeswrong` (`attw --pack .`).

Self-check: `node -e "require('pkg')"` and `import 'pkg'` both resolve to the intended files.
