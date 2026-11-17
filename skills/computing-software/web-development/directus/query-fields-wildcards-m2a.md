---
id: computing-software.web-development.directus.query-fields-wildcards-m2a
name: query-fields-wildcards-m2a
category: computing-software
field: web-development
product: directus
tags: [query-fields, wildcards, m2a-fields-syntax, api-search]
level: practitioner
status: docs-checked
description: "Select Directus response fields with dot notation and wildcards, fetch per-collection fields in Many to Any relations, and use the search parameter."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/04.connect/3.query-parameters.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`fields` picks returned fields; dot notation reaches nested relations and `*` is a wildcard at that depth.

```http
GET /items/posts?fields=title,author.name
GET /items/posts?fields=*,images.*
```

`*.*` returns all fields plus immediate relations. Production advice: request only needed fields; wildcards are slower and larger.

**Many to Any**: scope fields per related collection with `m2a-field:collection-scope.field`:

```http
GET /items/posts?fields[]=title&fields[]=sections.item:headings.title&fields[]=sections.item:paragraphs.body
```

SDK equivalent: `fields: ["title", { sections: [{ item: { headings: ["title"], paragraphs: ["body"] } }] }]`. In GraphQL use union types (`... on headings { title }`); in GraphQL filters replace `:` with a double underscore because names cannot contain `:`.

**search**: `?search=Directus` matches across all string and text fields of the collection (not related items). It is easy but less optimized than filters.

## Checked

2026-11-04: confirmed against the Directus docs Query Parameters page (Fields, Many to Any Fields, Filter GraphQL note, Search sections). Removed the unsupported verify line.

Method: documentation only; no commands were run.
