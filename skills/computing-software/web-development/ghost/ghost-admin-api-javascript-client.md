---
id: computing-software.web-development.ghost.ghost-admin-api-javascript-client
name: ghost-admin-api-javascript-client
category: computing-software
field: web-development
product: ghost
tags: [ghost, admin-api, javascript, tryghost-admin-api, nodejs, publishing]
level: practitioner
status: docs-checked
description: "Use the Ghost Admin API JavaScript client for posts, pages and image uploads, including the updated_at requirement on edits."
sources:
  - https://github.com/TryGhost/docs/blob/main/admin-api/javascript.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: script content changes against Ghost from Node.js.

Setup: `const api = new GhostAdminAPI({ url: 'http://localhost:2368', key: '<ADMIN_API_KEY>', version: 'v6.0' })`. The `url` must not end with a slash. The client signs the JWT for you.

Calls (marked stable in the docs):
- `api.posts.browse()`, `read({id})`, `add({title})`, `edit({id, title, updated_at})`, `delete({id})`.
- The same set for `api.pages`.
- `api.images.upload({file: '/path/to/local/file'})`.

Note that `edit` needs the post's current `updated_at`, which Ghost uses for collision detection. Fetch the record first, then pass `post.updated_at` back.

The docs include a publishing example: find image references in HTML with a regex, upload each file with `images.upload`, replace the local paths with the returned URLs, then call `posts.add({title, html}, {source: 'html'})`. Content can also be supplied as Lexical JSON via the `lexical` field.

Tip: the `ref` option on image upload returns your original path in the response, which makes find-and-replace of local paths straightforward.

Verify: after `posts.add`, the returned object has an `id` and the fields you set.

## Checked

2026-11-04. Confirmed: constructor options, url without trailing slash, the stable call list, updated_at on edit, the publishing example, the ref option and lexical field (Admin API JavaScript client page). Removed: nothing.

Method: documentation only; no commands were run.
