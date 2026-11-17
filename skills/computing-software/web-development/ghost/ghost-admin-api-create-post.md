---
id: computing-software.web-development.ghost.ghost-admin-api-create-post
name: ghost-admin-api-create-post
category: computing-software
field: web-development
product: ghost
tags: [ghost, admin-api, create-post, lexical, source-html, authors, tags]
level: practitioner
status: docs-checked
description: "Create Ghost posts through the Admin API: required title, Lexical or HTML source, and short versus long form tags and authors."
sources:
  - https://github.com/TryGhost/docs/blob/main/admin-api/posts/creating-a-post.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: create a draft or published post by API.

`POST /admin/posts/` with required field `title`. Every other field can be empty or has a default applied automatically. Body shape: `{"posts": [{...}]}`.

Content: Ghost stores Lexical. To send HTML instead, use the `source` parameter (`source=html`). Conversion is lossy because Ghost produces its best available Lexical representation, so use well-formed HTML with correct block and inline elements. For lossless HTML, wrap it in a single Lexical card.

Authors: a post must always have at least one author. With token authentication the default is the staff user with the Owner role.

Tags and authors in the same request:
- Short form: a plain string. Tags are identified by name, authors by email address.
- Long form: an object with at least one identifying key-value pair, for example `{"name": "my tag"}` or `{"id": "<author id>"}`.

Tags that cannot be matched are created automatically. If no author matches, Ghost falls back to the staff user with the Owner role.

Example minimal published post: `{"posts":[{"title":"Hello","status":"published","tags":["News"]}]}`, with `?source=html` and an `html` field if sending HTML.

Verify: the response returns the post with an `id`, a generated `slug` and the tags and authors you linked.

## Checked

2026-11-04. Confirmed: required title, defaults for other fields, lexical versus source=html, lossy conversion, the single-card route for lossless HTML, author default, short and long forms (creating a post page). Removed: nothing; added the unmatched tag and author fallback rules from the page.

Method: documentation only; no commands were run.
