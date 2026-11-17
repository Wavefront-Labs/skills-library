---
id: computing-software.web-development.ghost.ghost-routes-yaml-custom-routes
name: ghost-routes-yaml-custom-routes
category: computing-software
field: web-development
product: ghost
tags: [ghost, routes-yaml, dynamic-routing, custom-routes, templates, data]
level: advanced
status: docs-checked
description: "Edit Ghost routes.yaml to map URLs to templates, load page or tag data into a route, and apply changes without breaking YAML."
sources:
  - https://github.com/TryGhost/docs/blob/main/themes/routing.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: create URLs that load specific theme templates.

All routing config lives in `content/settings/routes.yaml`. You can edit the file directly (restart Ghost to see changes) or upload it under Settings, Labs in Ghost Admin, where routes update at once. YAML nests with exactly 2 spaces; wrong indentation is the usual failure.

Default file: one collection at `/` (permalink `/{slug}/`, template `index`) plus taxonomies `tag: /tag/{slug}/` and `author: /author/{slug}/`.

Custom routes live under `routes:`:
```yaml
routes:
  /features/: features
  /about/team/:
    template: team
    data: page.team
```
- `/features/: features` serves `features.hbs`; no data is loaded automatically.
- `data: page.team` loads the Ghost page with slug `team` into the route and redirects the original URL to the new one; the data is available inside the `{{#page}}` helper.

Routes can use letters, numbers, slashes, hyphens and underscores, and can simulate subdirectories. Trailing slashes are required for dynamic routing to function correctly. A route such as `/about/` and a Ghost page with slug `about` can conflict, so only one of them works.

Feeds and APIs: a route can set `content_type` (for example `text/xml` or `json`) with a template that uses `{{#get}}`, e.g. `/podcast/rss/` with `template: podcast-feed`. Channels are custom routes with `controller: channel` and a `filter`, such as `filter: tag:[iphone,ipad,mac]`; `channel` is the only supported controller value.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, 445 lines, no imported snippets): themes/routing.mdx. All paths, restart and upload behaviour and the default file match. Removed the Verify step; added content_type, channel and slug-conflict details from the page.
Method: documentation only; no commands were run.
