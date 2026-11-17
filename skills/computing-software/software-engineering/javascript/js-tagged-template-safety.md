---
id: computing-software.software-engineering.javascript.js-tagged-template-safety
name: js-tagged-template-safety
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, tagged-template-escaping, js-template-literals]
level: advanced
status: docs-checked
description: "How tag functions receive strings and values, the frozen cached strings array, raw strings, and tags that return non-strings; the base for escaping tags."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tagged templates: mechanics for escaping tags

- A tag function gets an array of string values first, then the expressions: `myTag\`That ${person} is a ${age}.\`` calls `myTag(strings, personExp, ageExp)`. The strings array length equals the number of substitutions plus one, so it is never empty.
- The tag may return a string or something completely different (MDN shows tags that return a closure). The tag name is arbitrary and can be any expression with precedence greater than 16, such as property access or a call.
- For one tagged template expression the tag is always called with the exact same literal array, however often it is evaluated, so a tag can cache on the array's identity. The first argument and its `raw` property are frozen.
- `strings.raw` holds the strings as entered, without processing escape sequences. `String.raw` builds raw strings; `String.raw({ raw: strings }, ...values)` makes an identity tag that behaves like an untagged literal.
- MDN notes that template literals coerce expressions directly to strings, while `+` coerces operands to primitives first.
- Untagged literals chained like ``` `Hello``World` ``` throw a `TypeError`; a tagged template on an optional chain is a `SyntaxError`.
- Design for safety on top of this: treat the literal parts as author-written and the substituted values as data, and escape or parameterise inside the tag. MDN's page documents the mechanism, not an escaping policy; check your target context's own guidance (HTML escaping, parameterised SQL) before relying on a tag.

Self-check: log `strings` and `strings.raw` from a tag called with a `\n` in the literal and confirm they differ.

## Checked

Confirmed against MDN "Template literals" (Tagged templates and Raw strings sections), read 2026-11-08. Removed: the specific escaped character list, the `{text, values}` SQL shape and the lit-html and `innerHTML` advice, since the page does not state them.
Method: docs-only read of cited pages, 2026-11-08
