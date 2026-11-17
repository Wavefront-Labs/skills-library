---
id: computing-software.web-development.ghost.ghost-content-api-overview-and-keys
name: ghost-content-api-overview-and-keys
category: computing-software
field: web-development
product: ghost
tags: [ghost, content-api, api-key, headless-cms, accept-version, rest]
level: practitioner
status: docs-checked
description: "Ghost Content API basics: URL shape, key query parameter, Accept-Version header, public read-only endpoints and which resources it serves."
sources:
  - https://github.com/TryGhost/docs/blob/main/content-api.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: read public Ghost content from a browser or server with the Content API.

Base URL: `https://{admin_domain}/ghost/api/content/`. The admin domain can differ from the public site domain, and using the wrong domain or protocol causes CORS trouble in browsers. Ghost(Pro) sites use a `*.ghost.io` admin domain and require https.

Steps:
1. In Ghost Admin open Integrations and create a `Custom Integration`. It shows the API URL and the Content API key.
2. Append the key as a query parameter: `?key={key}`. Content API keys only expose public data, so they are safe in browsers and other insecure places. Sites in private mode should be careful where they share the key.
3. Send `Accept-Version: v{major}.{minor}` to state the minimum Ghost version your client works with.

Example: `curl -H "Accept-Version: v6.0" "https://example.com/ghost/api/content/posts/?key=<CONTENT_API_KEY>"`.

Endpoints: posts, pages, tags, authors, tiers and settings, all GET, all returning JSON and documented as stable. Single records are read by id (`/posts/{id}/`) or slug (`/posts/slug/{slug}/`). The API is designed to be fully cacheable, so fetching often is fine.

Gotcha: the Content key is public but the Admin API key is secret; never mix them up.

Verify: the request returns a JSON object keyed by resource name (for example `posts`) plus a `meta.pagination` block on browse calls.

## Checked

2026-11-04. Confirmed: URL shape, admin domain note, Custom Integration key, ?key= parameter, Accept-Version, endpoint list, id and slug reads, cacheability (Content API overview page). Removed: nothing.

Method: documentation only; no commands were run.
