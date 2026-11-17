---
id: computing-software.software-engineering.javascript.js-template-literals-and-tagged-templates
name: js-template-literals-and-tagged-templates
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-template-literals, tagged-templates, string-raw, html-escaping]
level: practitioner
status: docs-checked
description: "Use template literals, multi-line strings and tagged templates (including safe interpolation)."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Template literals

- Backticks give multi-line strings and interpolation `${expr}`; to include a backtick, escape it with a backslash.
- Tagged template: a tag function receives the strings array plus the values. The first argument and its `raw` property are frozen, which lets a tag cache results by the identity of the strings array.
- `String.raw` produces raw strings without processing escapes.
- Invalid escape sequences are a syntax error unless a tag function is used; in a tagged template their cooked value is `undefined`.
- Tags enable safe construction (parameterised SQL, escaping HTML); plain interpolation into SQL, HTML or shell is injection.

## Checked

Date: 2026-11-02. Confirmed on MDN (Template_literals): interpolation, multi-line, backtick escape, frozen strings/raw, caching by identity, String.raw, invalid escape handling. Removed as not stated there: the String() conversion detail and the Windows-path example (not read).

Method: documentation only; no commands were run.
