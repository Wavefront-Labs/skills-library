---
id: computing-software.web-development.ghost.ghost-admin-api-update-post-collision
name: ghost-admin-api-update-post-collision
category: computing-software
field: web-development
product: ghost
tags: [ghost, admin-api, update-post, updated-at, collision-detection, revisions]
level: practitioner
status: docs-checked
description: "Update Ghost posts safely: send the latest updated_at, understand that tags and authors are replaced, and save revisions."
sources:
  - https://github.com/TryGhost/docs/blob/main/admin-api/posts/updating-a-post.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: edit an existing post without clobbering newer changes.

`PUT /admin/posts/{id}/` with required field `updated_at`. Ghost uses it for collision detection so you do not overwrite more recent updates. Always GET the post first, modify the fields you need, and send the change with the fresh `updated_at`.

Other rules:
- Any writable post field can be updated.
- Tags and authors are replaced, not merged. To add a tag, take the current `tags` array from your GET, append the new one and send the full array.
- To save a new revision as part of the update, add `save_revision=true` to the query string.

Minimal body: `{"posts":[{"title":"New title","updated_at":"2023-05-01T10:00:00.000Z"}]}`.

The JavaScript client mirrors this: `api.posts.edit({id, title, updated_at: post.updated_at})`.

Verify: the response contains the new `updated_at`; reuse that value for any further edit.

## Checked

2026-11-04. Confirmed: PUT path, required updated_at, collision detection, replace-not-merge for tags and authors, save_revision=true (updating a post page). Removed: the stale-timestamp retry paragraph, which describes behaviour the page does not state.

Method: documentation only; no commands were run.
