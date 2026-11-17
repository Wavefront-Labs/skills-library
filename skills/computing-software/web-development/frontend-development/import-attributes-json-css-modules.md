---
id: computing-software.web-development.frontend-development.import-attributes-json-css-modules
name: import-attributes-json-css-modules
category: computing-software
field: web-development
product: frontend-development
tags: [import-attributes, css-module-scripts, json-modules, adoptedstylesheets, javascript-modules]
level: practitioner
status: docs-checked
description: "Importing JSON and CSS as modules with import attributes (with type json/css), Node and bundler support, adoptedStyleSheets, and migrating from assert."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import/with
  - https://nodejs.org/api/esm.html#json-modules
  - https://nodejs.org/api/errors.html#err_import_attribute_missing
  - https://github.com/mdn/browser-compat-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Import attributes: JSON and CSS modules

## 1. Syntax
```js
import config from "./config.json" with { type: "json" };
import sheet from "./card.css" with { type: "css" };
const { default: messages } = await import(`./i18n/${lang}.json`, { with: { type: "json" } });
```
The attribute is a check: the import fails unless the response is served as the expected type (for JSON, `application/json`), so a URL expected to hold data cannot silently run as script.

## 2. CSS module scripts
```js
import sheet from "./card.css" with { type: "css" };
class Card extends HTMLElement {
  constructor() { super(); this.attachShadow({ mode: "open" }).adoptedStyleSheets = [sheet]; }
}
document.adoptedStyleSheets = [...document.adoptedStyleSheets, sheet];
```
The import yields a `CSSStyleSheet` that can be adopted by several roots. Per browser-compat-data, `type: "css"` is in Chrome 123 and Firefox 147 and not in Safari; check support before relying on it unbundled.

## 3. Environment support
- Browsers: `type: "json"` import attributes are in Chrome 123, Firefox 138 and Safari 17.2. MDN marks the old `assert` keyword as non-standard: replace `assert` with `with`.
- Node: the `with { type: 'json' }` syntax is mandatory for JSON modules (no longer experimental since v22.12 / v23.1, backported to v20.18.3 and v18.20.5); a missing attribute raises `ERR_IMPORT_ATTRIBUTE_MISSING`.

## Gotchas
- JSON modules export only `default`; `import { name } from "./pkg.json"` fails in browsers/Node.
- Node returns the same object for repeated imports of the same JSON path, so mutations are visible to every importer; copy before mutating.
- Modules are identified by their served media type, not the file extension: a server sending `text/plain` for `.json` fails a `type: "json"` import.

## Verify
- [ ] Network panel shows the CSS module fetched once even with many components.

## Checked

2026-10-26. MDN import attributes (the `assert` keyword is non-standard; media-type check; HTML spec defines json, text and css types), Node ESM docs (JSON modules: syntax mandatory, default export only, same object returned on repeat imports) and Node errors page, plus browser-compat-data for type json and css support. Removed the unconfirmed TypeScript, bundler, `@import` and one-line-command statements.

Method: documentation only; no commands were run.
