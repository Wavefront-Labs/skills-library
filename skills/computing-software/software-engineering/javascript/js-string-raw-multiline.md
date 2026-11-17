---
id: computing-software.software-engineering.javascript.js-string-raw-multiline
name: js-string-raw-multiline
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, string-raw, js-template-literals]
level: intro
status: docs-checked
description: "Use String.raw to keep backslashes in template literals, and know how substitutions and escaped template syntax behave."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/raw"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String.raw

- `String.raw` is the only built-in template literal tag. It returns the raw string form: escape sequences are ineffective and backslashes stay in the output. `String.raw\`Hi\n${2 + 3}!\`` is `Hi\n5!` with `\` and `n` as two characters.
- Useful for Windows-style paths, since backslashes need no escaping (MDN's `about.html` file path example).
- Substitutions (`${...}`) are still processed.
- A tagged function cannot bypass template syntax: to include a backtick or `${` you must escape them with a backslash, and because the output is raw the backslash is preserved (`` String.raw`Hi \${name}!` `` gives `Hi \${name}!`).
- Called as a normal function, `String.raw(strings, ...subs)` needs an object with a `raw` property, or it throws `TypeError`.
- Do not use `String.raw` directly as an identity tag; MDN has a separate "identity tag" recipe.

Self-check: the result of `` String.raw`\n` `` has length 2.

## Checked

Date: 2026-11-03. Confirmed on MDN String/raw: raw output and examples, Windows path, substitutions, escaping template syntax, TypeError, identity-tag warning. Removed as not stated there: regex source use, dedenting multiline text, line continuation, invalid escapes in tagged templates (`undefined` cooked), and the `.replace(/^\s+/gm, "")` idiom; the title and description no longer promise multiline-string guidance.

Method: documentation only; no commands were run.
