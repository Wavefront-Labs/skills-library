---
id: computing-software.web-development.jekyll.collections-liquid-attributes
name: collections-liquid-attributes
category: computing-software
field: web-development
product: jekyll
tags: [site-collections, document-attributes, hard-coded-posts, collection-label, future-dated-docs]
level: advanced
status: docs-checked
description: "Read collection and document attributes in Liquid via site.collections: label, docs, files, directory, output, url, relative_path, plus the posts quirk and time rules."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/collections.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`site.collections` holds each collection's config metadata plus:

- `label`: the collection name.
- `docs`: array of documents.
- `files`: array of static files.
- `relative_directory`: source directory relative to the site source.
- `directory`: full path to the source directory.
- `output`: whether documents are written as individual files.

`posts` is hard-coded and exists even without a `_posts` directory, so filter it out when iterating. Find one collection with:

```liquid
{{ site.collections | where: "label", "myCollection" | first }}
```

Document attributes (besides front matter): `content` (unrendered; text after the front matter), `output` (rendered result), `path` (full), `relative_path`, `url` (only written when the collection has `output: true`), `collection`, `date`.

Time rules: except for `posts`, all documents in your collections are accessible via Liquid regardless of date. A document is written to disk only if the collection has `output: true`, and future-dated ones also need `site.future` to be true. For finer control set `published: false` (default `true`) in the document's front matter.

## Checked

2026-11-04. Confirmed against the Jekyll Collections page: site.collections attributes, document attributes, hard-coded posts note and the time rules. Nothing removed.

Method: documentation only; no commands were run.
