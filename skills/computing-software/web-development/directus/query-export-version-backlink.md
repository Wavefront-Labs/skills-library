---
id: computing-software.web-development.directus.query-export-version-backlink
name: query-export-version-backlink
category: computing-software
field: web-development
product: directus
tags: [query-export, query-version, version-raw, backlink-parameter]
level: advanced
status: docs-checked
description: "Use the Directus export, version, versionRaw and backlink query parameters to download results, read content versions and trim circular wildcard output."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/04.connect/3.query-parameters.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- **export**: saves the response to a file: `?export=csv` (also `json`, `xml`, `yaml`).
- **version**: reads a content version by key when versioning is on: `GET /items/posts/1?version=v1`, also on lists. Reserved keys: `published` (or `main`) for the base item, `draft` for the global draft. In GraphQL it is supported only on single item and singleton reads (`posts_by_id(id: 1, version: "v1")`).
- Versioned responses include `$meta` with `version_id` (the `directus_versions` id, not the key). If a version has no saved changes or cannot apply, `$meta` also carries `delta`, plus an `error` object on failure.
- Item-less drafts appear in lists with a `null` primary key; request nested fields such as `fields=*,tags.*.*` to read existing related records.
- **versionRaw=true**: returns relational delta changes in detailed form; single item reads only.
- **backlink=false**: with `*.*` wildcard expansion, excludes reverse relations to avoid circular, duplicated data. Default is true. Explicit field paths like `author.articles` are not filtered.

## Checked

2026-11-04: confirmed against the Directus docs Query Parameters page (Export, Version, Version Meta, Item-less Drafts, VersionRaw, Backlink sections). Removed the unsupported verify line.

Method: documentation only; no commands were run.
