---
id: computing-software.web-development.ghost.ghost-content-api-settings-endpoint
name: ghost-content-api-settings-endpoint
category: computing-software
field: web-development
product: ghost
tags: [ghost, content-api, settings, navigation, site-metadata]
level: intro
status: docs-checked
description: "Fetch Ghost global site settings from the Content API: title, navigation, timezone and code injection in one object."
sources:
  - https://github.com/TryGhost/docs/blob/main/content-api/settings.mdx
  - https://github.com/TryGhost/docs/blob/main/content-api.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: read site-wide configuration for a headless front end.

Endpoint: `GET /content/settings/`. It is a special case: it returns a single object under `settings` rather than an array, and it does not accept any query parameters.

Keys in the sample response: `title`, `description`, `logo`, `icon`, `accent_color`, `cover_image`, `facebook`, `twitter`, `lang`, `timezone`, `codeinjection_head`, `codeinjection_foot`, `navigation` and `secondary_navigation` (arrays of `{label, url}` objects), `meta_title`, `meta_description`, `og_image`, `og_title`, `og_description`, `twitter_image`, `twitter_title`, `twitter_description`, `members_support_address` and `url`.

Typical use in a headless site:
1. Fetch settings once at build or request time and cache them.
2. Build menus from `navigation` and `secondary_navigation`.
3. Use `lang` and `timezone` for locale-aware rendering.
4. Inject `codeinjection_head` and `codeinjection_foot` if you want parity with Ghost-rendered pages.

The full URL form is `https://{admin_domain}/ghost/api/content/` plus the path, with the key as `?key={key}`; the Content API URL and key come from a Custom Integration under Integrations in Ghost Admin. Example: `curl "https://example.com/ghost/api/content/settings/?key=<KEY>"`.

Gotcha: do not rely on `include`, `fields` or `limit` here; the endpoint accepts no query parameters besides the key.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, no imported snippets): content-api/settings.mdx (60 lines) and content-api.mdx (103 lines, URL, key and endpoint table). The key list is exactly the sample response. Removed: the claim that the footer menu comes from `secondary_navigation` (page does not say what it is for) and the Verify step; the `/ghost/api/content/` URL form is from the overview page. "Besides the key" is inferred from the overview page, which says keys go in `?key=`.
Method: documentation only; no commands were run.
