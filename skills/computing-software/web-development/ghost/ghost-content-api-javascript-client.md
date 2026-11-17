---
id: computing-software.web-development.ghost.ghost-content-api-javascript-client
name: ghost-content-api-javascript-client
category: computing-software
field: web-development
product: ghost
tags: [ghost, content-api, javascript, nodejs, tryghost-content-api, sdk]
level: practitioner
status: docs-checked
description: "Use the Ghost Content API JavaScript client: constructor options, browse and read calls for posts, authors, tags and pages."
sources:
  - https://github.com/TryGhost/docs/blob/main/content-api/javascript.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: call the Content API without hand-building URLs.

Construct the client with `url` (API domain, no trailing slash), `key` (the hex Content API key from Integrations) and `version` (optional; the docs say to set `v6.0`; it is the minimum Ghost version your integration works with):

```js
const api = new GhostContentAPI({ url: 'https://example.com', key: '<CONTENT_API_KEY>', version: 'v6.0' });
api.posts.browse({limit: 5, include: 'tags,authors'}).then(posts => posts.forEach(p => console.log(p.title)));
```

Calls follow one pattern per resource:
- `api.posts.browse(opts)` resolves to an array with a `meta` property.
- `api.posts.read({id})` or `api.posts.read({slug}, {formats: ['html','plaintext']})` resolves to one record.
- The same browse and read pair exists for authors, tags and pages; `include` may be an array.
- Authors and tags accept `include: 'count.posts'`.

The client is a wrapper over the REST API and encodes filters and parameters for you, so no manual URL encoding is needed. Everything the Content API does is available through it.

Verify: logging `posts.meta.pagination` after a browse shows the page and total counts.

## Checked

2026-11-04. Confirmed: constructor options, browse and read forms, formats option, count.posts include, resolved array with meta, filter property use (Content API JavaScript client page). Removed: nothing material.

Method: documentation only; no commands were run.
