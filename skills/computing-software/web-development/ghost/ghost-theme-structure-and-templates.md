---
id: computing-software.web-development.ghost.ghost-theme-structure-and-templates
name: ghost-theme-structure-and-templates
category: computing-software
field: web-development
product: ghost
tags: [ghost, theme, handlebars, templates, default-hbs, post-hbs, index-hbs]
level: practitioner
status: docs-checked
description: "Lay out a Ghost theme: required index.hbs, post.hbs and package.json, plus default.hbs, home.hbs, page.hbs, partials and assets folders."
sources:
  - https://github.com/TryGhost/docs/blob/main/themes/structure.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: structure a theme Ghost will accept.

Recommended tree: `assets/` (css, fonts, images, js), optional `partials/`, `default.hbs`, `index.hbs`, `post.hbs`, `package.json`. Required: `index.hbs`, `post.hbs` and `package.json`.

Templates:
- `default.hbs`: base layout containing the html, head and body elements, the required `{{ghost_head}}` and `{{ghost_foot}}`, and shared header and footer. Other templates extend it.
- `index.hbs`: the required post-list template; also the fallback when there is no `tag.hbs` or `author.hbs`. Loop posts with `{{#foreach}}`.
- `home.hbs`: optional, renders only `/`.
- `post.hbs`: required single post template using the `{{#post}}` block. Per-post custom templates use `post-:slug.hbs`.
- `page.hbs`: optional static page template; falls back to `post.hbs`; `page-:slug.hbs` targets one page.

Templates are hierarchical, so one can extend another to avoid repeating base HTML. For significantly different layouts use the dynamic routing configuration layer or partials to encapsulate shared parts.

Required helpers: `{{asset}}`, `{{body_class}}`, `{{post_class}}`, `{{ghost_head}}`, `{{ghost_foot}}`. In `package.json`, optional `config.posts_per_page` (the page says the default is 5), `config.image_sizes`, `config.card_assets` and `config.custom`. Changes to `package.json` or a `.hbs` file in production mode need `ghost restart`. Ghost checks for fatal errors when a theme is uploaded in Ghost Admin; use GScan for a full validation report.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, 181 lines, no imported snippets): themes/structure.mdx. Every template, requirement and fallback above matches it. Changed: "routes.yaml" to the page's wording (it says dynamic routing configuration layer); replaced the invented Verify step with what the page says about upload checks and GScan; added required helpers and package.json properties.
Method: documentation only; no commands were run.
