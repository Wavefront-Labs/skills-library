---
id: computing-software.web-development.ghost.ghost-head-and-foot-helpers
name: ghost-head-and-foot-helpers
category: computing-software
field: web-development
product: ghost
tags: [ghost, ghost-head, ghost-foot, code-injection, structured-data, theme]
level: intro
status: docs-checked
description: "Place ghost_head and ghost_foot correctly in default.hbs so Ghost injects meta, structured data, API scripts and code injection."
sources:
  - https://github.com/TryGhost/docs/blob/main/themes/helpers/utility/ghost_head_foot.mdx
  - https://github.com/TryGhost/docs/blob/main/themes/structure.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep Ghost's system output working in a theme.

These helpers output vital system information at the top and bottom of the document and provide hooks to inject additional scripts and styles. Put `{{ghost_head}}` just before the closing head tag and `{{ghost_foot}}` just before the closing body tag in `default.hbs`. The theme structure page lists both among the required helpers (with `{{asset}}`, `{{body_class}}` and `{{post_class}}`).

`ghost_head` outputs: the meta description, Schema.org structured data as JSON-LD, structured data tags for Facebook Open Graph and Twitter Cards, RSS URL paths for feed discovery, scripts that enable the Ghost API, and anything added in the Code Injection section globally or at page level.

`ghost_foot` outputs anything added in the Code Injection section globally or at page level.

Practical implication: Ghost generates the meta description and the Open Graph and Twitter Card tags through `ghost_head`, so avoid duplicating them by hand in the theme.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, no imported snippets): themes/helpers/utility/ghost_head_foot.mdx (26 lines) and themes/structure.mdx (181 lines). Output lists and placement match; the required-helpers list is from structure.mdx. Removed as unconfirmed: the advice to use Code Injection so owners avoid editing files, the claim that missing members or search features mean a missing helper, and the Verify step; added structure.mdx to sources.
Method: documentation only; no commands were run.
