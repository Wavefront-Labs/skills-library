---
id: computing-software.web-development.svelte.markup-attributes
name: markup-attributes
category: computing-software
field: web-development
product: svelte
tags: [basic-markup, attribute-expressions, spread-attributes, shorthand-attributes, text-expressions]
level: intro
status: docs-checked
description: "Svelte markup basics: component vs element tags, dynamic and boolean attributes, shorthand and spread order, text expressions, regex in braces, and comments."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/01-basic-markup.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tags: lowercase (`<div>`) is an HTML element; capitalised or dot notation (`<Widget>`, `<my.stuff>`) is a component.

Attributes can hold expressions: `href="page/{p}"` or `disabled={!clickable}`. Boolean attributes are included when truthy and excluded when falsy. Other attributes are included unless nullish (`title={null}` renders no attribute).

Shorthand when name and value match: `<button {disabled}>`. Same for props: `<Widget foo={bar} answer={42} />`.

Spread passes many at once; order matters. In `<Widget a="b" {...things} c="d" />`, `things.a` wins over `a="b"`, while `c="d"` wins over `things.c`.

Text expressions: `{expression}`. `null` and `undefined` are omitted; everything else is coerced to a string and escaped (use `{@html}` for HTML). Wrap a regex literal in parentheses: `{(/^[A-Za-z ]+$/).test(value) ? x : y}`. For literal braces use HTML entities `&lbrace;` / `&rbrace;`.

Comments: `<!-- svelte-ignore a11y_autofocus -->` silences warnings for the next markup block; `<!-- @component ... -->` text shows on hover over the component name.

Note: quoting a single expression (`disabled="{n !== 42}"`) currently does not change parsing, but in Svelte 6 will coerce to a string.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the basic markup page: tag casing rules, attribute and boolean handling, shorthand, spread order, text expressions, regex parentheses, brace entities, svelte-ignore and @component comments, and the Svelte 6 quoting note. Nothing removed.
