---
id: computing-software.web-development.mkdocs.extra-css-javascript
name: extra-css-javascript
category: computing-software
field: web-development
product: mkdocs
tags: [extra-css, extra-javascript, module-scripts, script-attributes]
level: practitioner
status: docs-checked
description: "Add custom CSS and JavaScript with extra_css and extra_javascript, including the 1.5 mapping form with type, async and defer."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/customizing-your-theme.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Both options are lists of files relative to `docs_dir` (default `[]`).

```yaml
extra_css:
  - css/extra.css
  - css/second_extra.css

extra_javascript:
  - some_plain_javascript.js        # <script src="..."></script>
  - implicitly_as_module.mjs        # type="module" added (plain string only)
  - path: explicitly_as_module.mjs
    type: module
  - path: deferred_plain.js
    defer: true
  - path: scripts/async_module.mjs
    type: module
    async: true
```

Since 1.5 each JS item is a string or a mapping with required `path` and optional `type` (string), `async`, `defer` (booleans). Only the plain-string form detects `.mjs`; otherwise write `type: module`.

Gotchas:
- Extra CSS and JavaScript files are added to the generated HTML after the page content; to include a library earlier, use the theme `custom_dir`.
- `*.js` and `*.css` are always copied from `docs_dir`, linked or not.

## Checked

2026-11-04. Confirmed against the MkDocs configuration guide (extra_css, extra_javascript) and Customizing Your Theme: defaults `[]`, the 1.5 mapping keys, `.mjs` detection for plain strings only, files always copied, and the after-content note. Removed: a claim about `script_tag` and a generic verify line.

Method: documentation only; no commands were run.
