---
id: computing-software.web-development.frontend-development.esm-and-commonjs-interop
name: esm-and-commonjs-interop
category: computing-software
field: web-development
product: frontend-development
tags: [es-modules, javascript-modules, esm-cjs-interop, package-exports, type-module, dual-package, require-esm, conditional-exports]
level: practitioner
status: verified
description: "Navigating ESM vs CommonJS in Node and bundlers: type module, package.json exports and conditions, require(esm), default-import interop and dual-package hazards."
sources:
  - https://nodejs.org/api/packages.html
  - https://nodejs.org/api/esm.html#interoperability-with-commonjs
  - https://nodejs.org/api/modules.html#loading-ecmascript-modules-using-require
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESM and CommonJS interop

**Goal:** packages and apps load the same way in Node, bundlers and tests, without "require is not defined" or "default is not a function".

## 1. How Node decides
- `.mjs` = ESM, `.cjs` = CJS, `.js` = per nearest `package.json` `"type"` (`"module"` or default `"commonjs"`).
- Node 22+ can `require()` ESM modules that have no top-level await (`require(esm)`, unflagged in 22.12/20.19); older versions throw `ERR_REQUIRE_ESM`. ESM can always `import` CJS. In Node 20.20 `require("esm-lib")` returned `[Module: null prototype] { __esModule: true, default: 5, n: 1 }`: with a default export you read `.default`.
- Node also detects ESM syntax in ambiguous `.js` files (`--experimental-detect-module`; on by default in Node 20.20: an `import` file with no `"type"` ran, and `--no-experimental-detect-module` gave `SyntaxError: Cannot use import statement outside a module`) - don't rely on it; set `"type"`.

## 2. Importing CJS from ESM
```js
import pkg from 'cjs-lib';          // module.exports becomes the default export (always works)
import { helper } from 'cjs-lib';   // works only if Node's static analysis (cjs-module-lexer) detects the named export
```
The classic bug: a CJS build compiled from TS/Babel sets `exports.default = fn`, so `import x from` gave `{ default: [Function: fn], helper: 1 }` in Node 20 but `fn` in bundlers. A CJS module whose export keys are computed (`{ ...o, ["he"+"lper"]: 2 }`) exposed only `default` to `import()`, so named imports of it fail. Fix with `esModuleInterop` in TS, or access `.default` defensively.

## 3. package.json exports
```json
{
  "name": "my-lib",
  "type": "module",
  "exports": {
    ".": { "types": "./dist/index.d.ts", "import": "./dist/index.js", "require": "./dist/index.cjs" },
    "./utils": "./dist/utils.js",
    "./package.json": "./package.json"
  },
  "sideEffects": false
}
```
- `exports` **encapsulates**: deep imports not listed are blocked (`ERR_PACKAGE_PATH_NOT_EXPORTED`, confirmed for `my-lib/hidden.js`).
- Condition order matters; `types` first, `default` last.
- **Dual-package hazard**: shipping both ESM and CJS can load two copies (separate singletons/`instanceof` failures). Prefer ESM-only now that `require(esm)` exists, or make the ESM wrapper re-export the CJS build.

## 4. ESM gotchas in Node
No `__dirname`/`__filename` (use `import.meta.dirname` / `import.meta.filename` in Node 20.11+), no `require` (use `createRequire(import.meta.url)`), relative imports need file extensions, JSON imports need `with { type: 'json' }` (without it Node 20 threw `ERR_IMPORT_ASSERTION_TYPE_MISSING`).

## Verify
- [ ] `node -e "require('my-lib')"` and `node --input-type=module -e "import 'my-lib'"` both work as intended.
- [ ] `publint` and `@arethetypeswrong/cli` report no problems.
- [ ] Only one copy of the package in the bundle analyzer.
