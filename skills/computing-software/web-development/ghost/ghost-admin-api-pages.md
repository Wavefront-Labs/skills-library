---
id: computing-software.web-development.ghost.ghost-admin-api-pages
name: ghost-admin-api-pages
category: computing-software
field: web-development
product: ghost
tags: [ghost, admin-api, pages, static-pages, crud]
level: intro
status: docs-checked
description: "Manage Ghost static pages through the Admin API; pages mirror posts in request and response shape."
sources:
  - https://github.com/TryGhost/docs/blob/main/admin-api/pages/overview.mdx
  - https://github.com/TryGhost/docs/blob/main/themes/structure.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: create and maintain static pages programmatically.

Pages are static resources that are not included in channels or collections on the Ghost front end. In requests and responses they are identical to posts, so everything about the posts endpoints applies.

Endpoints:
- `GET /admin/pages/`
- `GET /admin/pages/{id}/`
- `GET /admin/pages/slug/{slug}/`
- `POST /admin/pages/`
- `POST /admin/pages/{id}/copy`
- `PUT /admin/pages/{id}/`
- `DELETE /admin/pages/{id}/`

Body wrapper is `{"pages": [{...}]}`. Updates still need the current `updated_at`. JavaScript client: `api.pages.browse`, `read`, `add`, `edit`, `delete`.

Theme side: a page renders with `page.hbs`, falling back to `post.hbs`; a custom per-page template named `page-:slug.hbs` can be mapped to one page by slug.

Typical use: sync an About or Terms page from a repository by reading it by slug, comparing, then sending a `PUT` with the latest `updated_at`.

Verify: the page appears at its slug URL and is absent from the home post list.

## Checked

2026-11-04. Confirmed: pages versus posts, the seven endpoints, the page.hbs fallback and page-:slug.hbs template names (pages overview and theme structure pages). Removed: nothing.

Method: documentation only; no commands were run.
