---
id: computing-software.web-development.ghost.ghost-helpers-has-is-match-conditionals
name: ghost-helpers-has-is-match-conditionals
category: computing-software
field: web-development
product: ghost
tags: [ghost, handlebars, has-helper, is-helper, match-helper, conditionals, theme]
level: practitioner
status: docs-checked
description: "Choose between Ghost has, is and match helpers to branch on tags, route context and custom setting values in themes."
sources:
  - https://github.com/TryGhost/docs/blob/main/themes/helpers/functional/has.mdx
  - https://github.com/TryGhost/docs/blob/main/themes/helpers/functional/is.mdx
  - https://github.com/TryGhost/docs/blob/main/themes/helpers/functional/match.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the right conditional helper.

`{{#has}}` asks questions about the current context: tag, author, slug, id, any/all properties set, or loop number. Multiple attributes are OR. Example: `{{#has tag="#link"}}` detects an internal tag used to mark link posts. Supports `{{else}}`, `^` negation and `{{else has ...}}` chaining.

`{{#is "home"}}` checks the route context. Values: `home`, `index`, `post`, `page`, `tag`, `author`, `paged` (page 2 and beyond) and `private`. A comma means OR (`"post, page"`); AND is done by nesting. `{{^is "paged"}}` negates.

`{{#match}}` compares values: operators `=` (default), `!=`, `>`, `>=`, `<`, `<=`, `~` contains, `~^` starts with, `~$` ends with. It pairs well with custom settings: `{{#match @custom.color_scheme "!=" "Dark"}}...{{else}}...{{/match}}`. A string example: `{{#match slug "~^" "hash-episode-"}}`.

`{{#match featured}}` with no operator tests truthiness like `if`; values are tested by value and type, so `{{#match feature_image true}}` can be true but `{{#match feature_image 'true'}}` is always false. `>`, `<`, `>=`, `<=` are numeric comparisons.

`{{#has}}` details: `tag` and `author` take comma-separated lists (OR) and counts such as `count:1`, `count:>1`, `count:<2`; matching is lowercase on the name and ignores special characters. AND is done by nesting `has` helpers. `number="nth:3"` inside a foreach matches every third item (also `number="3, 6, 9"`).

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, no imported snippets): themes/helpers/functional/has.mdx (193 lines), is.mdx (51 lines), match.mdx (95 lines). Every context value and operator above matches. Removed as unconfirmed: the claim that boolean custom settings need only `{{#if}}` (not on these pages) and the Verify step. Added match evaluation rules and has counting and nth details.
Method: documentation only; no commands were run.
