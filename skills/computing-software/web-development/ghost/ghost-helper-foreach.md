---
id: computing-software.web-development.ghost.ghost-helper-foreach
name: ghost-helper-foreach
category: computing-software
field: web-development
product: ghost
tags: [ghost, handlebars, foreach, loop, theme-helper]
level: practitioner
status: docs-checked
description: "Use Ghost's foreach helper instead of Handlebars each: loop variables, else blocks and the posts loop pattern."
sources:
  - https://github.com/TryGhost/docs/blob/main/themes/helpers/functional/foreach.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: loop over posts, tags or users in a Ghost theme.

`{{#foreach}}` is a special, context-aware loop helper designed for lists of posts that can also iterate tags or users. The docs say it should always be used instead of Handlebars `each` in Ghost themes.

```handlebars
{{#foreach posts}}
  <h2>{{title}}</h2>
  {{excerpt words="26"}}
  {{date format="DD MMMM YYYY"}}
{{/foreach}}
```

Data variables inside the block: `@index` (0-based), `@number` (1-based), `@key` (object key when iterating an object; the page says there is no real use case in Ghost at present), `@first`, `@last`, `@odd` and `@even` (based on `@index`), and `@rowStart` and `@rowEnd` when `columns` is passed (for example `{{#foreach posts columns="3"}}`).

Attributes:
- `limit="3"` stops after that many iterations. It only passively limits, so a number above the collection size has no effect.
- `from="2" to="5"` select items; both are 1-indexed and inclusive.
- `visibility`: by default only public data is shown (hidden tiers and internal tags are left out); `visibility="all"` shows all data and `none` shows hidden data.

Block params name the current item: `{{#foreach posts as |my_post|}}{{#my_post}}...{{/my_post}}{{/foreach}}`, which the page says is useful with advanced features like the `{{get}}` helper.

Like all block helpers it supports `{{else}}`, which runs when there is no data to iterate over.

The `{{#get}}` helper's output can be iterated with foreach: fetch with get, then loop the resulting block.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, 186 lines, no imported snippets): themes/helpers/functional/foreach.mdx. One caveat on the page itself: the visibility example block is not closed in the source, which does not affect the text read. Removed as unconfirmed: the `^` negation claim (the page heading mentions negation but shows only `{{else}}`), the tip about `@first` and `@last` layout choices, and the Verify step. Added limit, from, to, visibility, columns and block params from the page.
Method: documentation only; no commands were run.
