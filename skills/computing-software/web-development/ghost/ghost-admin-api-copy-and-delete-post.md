---
id: computing-software.web-development.ghost.ghost-admin-api-copy-and-delete-post
name: ghost-admin-api-copy-and-delete-post
category: computing-software
field: web-development
product: ghost
tags: [ghost, admin-api, copy-post, duplicate, delete-post, templates]
level: intro
status: docs-checked
description: "Duplicate a Ghost post through the Admin API: the copy endpoint appends Copy to title and slug and returns a draft."
sources:
  - https://github.com/TryGhost/docs/blob/main/admin-api/posts/copying-a-post.mdx
  - https://github.com/TryGhost/docs/blob/main/admin-api/pages/overview.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use an existing post as a template.

Copy: `POST /admin/posts/{id}/copy`. The required input is the `id` in the path. Ghost duplicates the post, appends "Copy" to the title and slug (for example `My test post (Copy)` and `my-test-post-copy`), and returns the new post created as a draft. Pages have the same endpoint at `POST /admin/pages/{id}/copy`.

Pattern for template-based publishing:
1. Keep a draft post that holds your standard layout.
2. Call the copy endpoint to produce a fresh draft.
3. Update the copy's title, slug and content with a normal `PUT` using its `updated_at`.
4. Publish when ready.

Delete: the endpoint table lists Delete for posts and pages; the pages overview shows `DELETE /admin/pages/{id}/` and the JavaScript client exposes `api.posts.delete({id})`. Back up first if you may need the content again.

Verify: the copy response has a new `id`, a title ending in `(Copy)` and a draft state.

## Checked

2026-11-04. Confirmed: the copy endpoint path, required id, " (Copy)" title and slug suffix, draft result, pages copy endpoint, DELETE for pages (copying a post, pages overview, Admin API overview, JavaScript client pages). Removed: the unconfirmed REST path `DELETE /admin/posts/{id}/` (the pages path is documented, the posts path is not shown).

Method: documentation only; no commands were run.
