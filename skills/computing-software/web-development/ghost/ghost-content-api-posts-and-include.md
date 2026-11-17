---
id: computing-software.web-development.ghost.ghost-content-api-posts-and-include
name: ghost-content-api-posts-and-include
category: computing-software
field: web-development
product: ghost
tags: [ghost, content-api, posts, include, authors, tags, primary-author]
level: practitioner
status: docs-checked
description: "Fetch Ghost posts from the Content API by id or slug, and use include to get tags and authors that are omitted by default."
sources:
  - https://github.com/TryGhost/docs/blob/main/content-api/posts.mdx
  - https://github.com/TryGhost/docs/blob/main/content-api/parameters.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get posts with their related tags and authors.

Routes: `GET /content/posts/`, `GET /content/posts/{id}/`, `GET /content/posts/slug/{slug}/`. Browse results come back newest first by `published_at`.

The most common gotcha: a post response does not contain tags or authors unless you ask. Add `&include=authors,tags`. That adds an `authors` array and a `primary_author` object, plus a `tags` array and a `primary_tag` object. For authors and tags, `&include=count.posts` adds `"count": {"posts": N}`. For tiers the available includes are `monthly_price`, `yearly_price` and `benefits`.

Other post fields worth knowing from the sample response: `html`, `url`, `excerpt`, `reading_time`, `visibility`, `access`, `feature_image`, `canonical_url`, `codeinjection_head`, plus `og_*`, `twitter_*` and `meta_*` fields.

By default only `html` is returned. Add `&formats=html,plaintext` to also get the plaintext rendering (posts and pages only).

`fields` trims the response (`&fields=title,url`) but the docs warn it does not play well with `include`, so test the combination before relying on it.

Verify: with `include=tags` the JSON has `primary_tag`; without it the key is absent.

## Checked

2026-11-04. Confirmed: routes, newest-first ordering, the include gotcha, authors and tags includes with primary_author and primary_tag, count.posts, tier includes, formats, fields caveat (Content API posts and parameters pages). Removed: nothing.

Method: documentation only; no commands were run.
