---
id: computing-software.web-development.ghost.ghost-partials-and-dynamic-partials
name: ghost-partials-and-dynamic-partials
category: computing-software
field: web-development
product: ghost
tags: [ghost, handlebars, partials, theme, dynamic-partials, concat]
level: practitioner
status: docs-checked
description: "Reuse Ghost theme markup with partials: context inheritance, properties, and the block form for dynamic partial names."
sources:
  - https://github.com/TryGhost/docs/blob/main/themes/helpers/utility/partials.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: share template chunks without duplication.

Partials live in the theme's `partials/` directory and are called with `{{> "post-card"}}`. A partial inherits the calling context, so inside `{{#foreach posts}}` the card sees each post.

Properties: pass values per use, e.g. `{{> "call-to-action" heading="Sign up now"}}`, and read them as `{{heading}}` inside the partial.

Dynamic names: build the partial name with a sub-expression such as `(concat "icons/" type)`. Use the block form, not the inline form:
```handlebars
{{#> (concat "icons/" type)}}
  {{name}}
{{/undefined}}
```
The block form renders its inner content as a fallback if the partial does not exist; the inline form throws a page error. The closing tag must be `{{/undefined}}`, which looks odd but is the only form Handlebars accepts for a dynamic partial block.

The page's use case for dynamic partials is iterating a collection where each item needs a different partial, such as per-platform social icons. Partials are for repeating elements (such as a post card) or splitting components like a header out of large templates.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, 68 lines, no imported snippets): themes/helpers/utility/partials.mdx. Removed as unconfirmed: the claim that a partial named `pagination.hbs` overrides the pagination helper, and the Verify step. The `{{/undefined}}` closing tag and block-form fallback statements are the page's own wording.
Method: documentation only; no commands were run.
