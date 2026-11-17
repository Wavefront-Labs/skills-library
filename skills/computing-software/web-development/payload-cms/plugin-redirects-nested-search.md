---
id: computing-software.web-development.payload-cms.plugin-redirects-nested-search
name: plugin-redirects-nested-search
category: computing-software
field: web-development
product: payload-cms
tags: [redirects-plugin, nested-docs-plugin, search-plugin, breadcrumbs]
level: practitioner
status: docs-checked
description: "Configure the Redirects, Nested Docs and Search plugins with their basic options."
sources:
  - https://payloadcms.com/docs/plugins/redirects
  - https://payloadcms.com/docs/plugins/nested-docs
  - https://payloadcms.com/docs/plugins/search
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Redirects, Nested Docs and Search plugins

Goal: add URL redirects, page hierarchy and fast search.

Redirects (`@payloadcms/plugin-redirects`) adds a `redirects` collection with `from` and `to` (a URL or document reference). Use it to write HTTP redirects in your frontend.

```ts
redirectsPlugin({ collections: ['pages'] })   // options include overrides, redirectTypes
```

Nested Docs (`@payloadcms/plugin-nested-docs`) adds a `parent` field and `breadcrumbs`; editing an ancestor cascades to descendants.

```ts
nestedDocsPlugin({
  collections: ['pages'],
  generateLabel: (_, doc) => String(doc.title),
  generateURL: (docs) => docs.reduce((url, doc) => `${url}/${String(doc.slug)}`, ''),
})
```

Search (`@payloadcms/plugin-search`) maintains an indexed `search` collection that stores only the data you choose and can prioritise results by collection:

```ts
searchPlugin({ collections: ['pages', 'posts'], defaultPriorities: { pages: 10, posts: 20 } })
```

The search collection is queried with the normal Payload APIs (each record has a `priority` field usable as `?sort=`) and can be reindexed on demand. Copied fields do not inherit the source collection's access control, so sync only data that is safe to expose, or give the field its own `access.read` in `searchOverrides`.

Verify: create a page and see matching entries in the redirects, breadcrumbs or search collection.

## Checked

2026-11-04. Read plugins/redirects, plugins/nested-docs and plugins/search. Confirmed: the redirects collection with from and to (document reference allowed), redirectsPlugin options (collections, overrides, redirectTypes, redirectTypeFieldOverride) and that the frontend does the actual redirecting; the nestedDocsPlugin example with generateLabel and generateURL, the parent field, breadcrumbs, and recursive descendant updates; the searchPlugin example with defaultPriorities, the indexed search collection, priority sorting and on-demand reindexing. Added: the two extra sources and the search access-control warning.
Method: documentation only; no commands were run.
