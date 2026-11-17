---
id: computing-software.web-development.ghost.ghost-template-inheritance-block-contentfor
name: ghost-template-inheritance-block-contentfor
category: computing-software
field: web-development
product: ghost
tags: [ghost, handlebars, block-helper, contentfor, body-helper, layouts]
level: advanced
status: docs-checked
description: "Create layout slots in Ghost themes with block and contentFor, and understand where body is used and the template restrictions."
sources:
  - https://github.com/TryGhost/docs/blob/main/themes/helpers/utility/block.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: build flexible layout inheritance in a theme.

`{{{block "block-name"}}}` creates a placeholder (a slot, with a unique id) in a template, which can optionally be filled when the template is inherited by another template file. A child template fills it with `{{#contentFor "block-name"}}...{{/contentFor}}`; the inherited template is referenced with `{{!< template-name}}` at the top of the file. If `contentFor` is not used, the block is gracefully skipped. Example from the page: `default.hbs` holds `{{{block "scripts"}}}` before the closing body tag, and `page.hbs` starts with `{{!< default}}` and supplies a `<script>` inside `{{#contentFor "scripts"}}`.

`{{{body}}}` behaves like a block that needs no contentFor: the inheriting template's own content is inserted where the body helper sits.

Important restrictions:
- A file containing `{{{block}}}` definitions cannot be a template Ghost uses directly.
- `post.hbs`, `page.hbs` and `index.hbs` may inherit from layouts and use `contentFor`, but may not contain block definitions.

See the theme structure skill for how default.hbs and other templates relate.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, 67 lines, no imported snippets): themes/helpers/utility/block.mdx. Restrictions and the body example match. Removed as unconfirmed: the use-case list, the "block renders empty" troubleshooting advice (the page says an unfilled block is skipped gracefully), and the Verify step. Added the `{{!< template-name}}` syntax from the page.
Method: documentation only; no commands were run.
