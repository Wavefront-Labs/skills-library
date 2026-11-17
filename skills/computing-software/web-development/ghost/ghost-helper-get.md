---
id: computing-software.web-development.ghost.ghost-helper-get
name: ghost-helper-get
category: computing-software
field: web-development
product: ghost
tags: [ghost, handlebars, get-helper, theme, api-query, block-parameters]
level: advanced
status: docs-checked
description: "Query extra data in Ghost themes with the get helper: browse or read posts, tags, authors, tiers and newsletters server-side."
sources:
  - https://github.com/TryGhost/docs/blob/main/themes/helpers/functional/get.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pull data beyond what a template context provides.

`{{#get}}` makes a custom query to the Ghost API for publicly available data. Requests are made server-side before the templates render. With only a resource name it performs a browse (a list; iterate it with `{{#foreach}}`); with a resource field such as `id` or `slug` as an attribute it performs a read of one record.

Resources: the page says `"posts"`, `"tags"`, `"authors"` and `"tiers"`, and also lists `newsletters` ("any newsletter"). Posts are any published post, tags any tag with a post, authors any author who has published a post.

Examples:
```handlebars
{{#get "posts"}}{{#foreach posts}}{{title}}{{/foreach}}{{/get}}

{{#get "posts" id="2" include="tags,authors" as |post|}}{{#post}}{{title}}{{/post}}{{/get}}

{{#get "tags" limit="100"}}{{tags}}{{/get}}
```
The default browse returns the 15 newest posts. Attributes are identical to the Content API ones: `limit` (1-100, default 15; over 100 returns 100), `page`, `order` (for example `order="published_at asc"`), `include` and `filter`. Browse requests accept all of them; read requests accept only `include`. `limit=@config.posts_per_page` uses the theme setting (default 5 per the page).

Block parameters go between pipes and there are two: the data collection and the pagination object, for example `{{#get "posts" as |articles pages|}}` then `{{pages.total}}`.

`{{else}}` on get only runs on an error (mostly useful for debugging; `{{error}}`). To show content when there are no results, put `{{else}}` inside the `{{#foreach}}`.

The `filter` attribute takes NQL (`,` for or, `+` for and, `-` for negation); see `computing-software.web-development.ghost.ghost-content-api-nql-filtering`. Data from the template can be passed into the filter, for example `filter="primary_tag:{{primary_tag.slug}}"`; wrap values with spaces in single quotes; use data attributes such as `{{published_at}}`, not helpers like `{{date}}`, because helpers are not called inside a filter.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, 373 lines; the page's last tier-signup example has broken markup in the source but nothing above depends on it; no imported snippets): themes/helpers/functional/get.mdx. Removed as unconfirmed: the note that the query runs on every render so get blocks should be kept modest, and the Verify step. Noted the page's own inconsistency: it says available resources are posts, tags, authors, tiers but then also lists newsletters. Added attributes, block params, else behaviour and filter data-passing rules.
Method: documentation only; no commands were run.
