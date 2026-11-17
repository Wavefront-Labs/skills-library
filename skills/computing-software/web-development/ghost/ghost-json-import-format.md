---
id: computing-software.web-development.ghost.ghost-json-import-format
name: ghost-json-import-format
category: computing-software
field: web-development
product: ghost
tags: [ghost, import, migration, json, meta, data-block, posts-tags]
level: advanced
status: docs-checked
description: "Build a custom Ghost import JSON file: valid JSON, the meta block with exported_on and version, and the data block of posts, tags and users."
sources:
  - https://github.com/TryGhost/docs/blob/main/migration/custom.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: import content from another system into Ghost.

The file must be valid JSON (test with a linter). The structure may optionally be wrapped in an object with a top-level `db` key; both wrapped and unwrapped forms are valid, but you must include a `meta` object and a `data` object.

`meta` has two keys: `exported_on` (epoch timestamp in milliseconds) and `version` (the Ghost version the import is valid for).

`data` mirrors the underlying database structure rather than the API, so you can override fields the API would ignore. It holds arrays of objects for posts, tags, users and the relationships between them.

Relationships: define links between posts and tags (a posts_tags array) and posts and users (a posts_authors array). Ids inside the file are relative to the file only: a post with `id: "1234"` and a link row referencing `post_id: "1234"` are linked together, but neither relates to a record with that id already in your database.

Use the Ghost schema on GitHub for allowed fields, types, lengths and validations.

The page's `data` shape lists `posts`, `posts_meta` (optional, keyed by `post_id`), `tags`, `posts_tags`, `users` and `posts_authors`. The sample post has `id`, `title`, `slug`, `html` (the comment says `lexical` could be used instead), `comment_id`, `feature_image`, `type` (post or page), `status` (published or draft), `visibility` (public, members or paid), `created_at`, `updated_at`, `published_at` and `custom_excerpt`. Sample `users` carry `roles` (Contributor, Author, Editor or Administrator). The sample `meta` is `exported_on: 1753891082041` and `version: "6.0.0"`.

The final JSON must contain no comments; the page's example includes them only for readability. Test validity with a JSON linter such as JSONLint.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, 125 lines, no imported snippets): migration/custom.mdx. Removed as unconfirmed: the "minimal file, import in Ghost Admin, inspect, scale up" process, the statement that the same docs section covers platform-specific migrations, and the Verify step. Added the data keys, field values and no-comments rule from the page.
Method: documentation only; no commands were run.
