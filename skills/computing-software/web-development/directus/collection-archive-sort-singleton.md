---
id: computing-software.web-development.directus.collection-archive-sort-singleton
name: collection-archive-sort-singleton
category: computing-software
field: web-development
product: directus
tags: [collection-archive, manual-sort, singleton, display-template]
level: practitioner
status: docs-checked
description: "Configure Directus collection settings: archive field and values, manual sort field, singleton mode, display template and the accountability level."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/01.data-model/1.collections.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Open the collection in Data Model settings.

- **Singleton**: skips the collection page and opens the single item detail page.
- **Display Template**: how an item appears inside relationship fields, e.g. an author's name.
- **Archive**: set Archive Field, Archive App Filter, Archive Value and Unarchive Value. The wizard's `archived` field is boolean (archive `true`, unarchive `false`); a manual field can be any string or boolean field. Archived items are hidden only in the app; the API still returns them unless you filter.
- **Sort**: if no sort field was created, add an integer field and select it as the sort field. Then click the sort icon in the column and drag rows. For relational M2M, O2M or M2A, also set the sort field in the field's relationship section.
- **Accountability**: by default all activity and revisions are tracked; you can track only activity, or nothing.
- **Save as Copy** does not copy related items; recreate the relationships.

## Checked

2026-11-04: singleton, display template, archive settings and boolean wizard field, sort field setup including relational fields, accountability levels and Save as Copy behaviour confirmed against the Directus Collections page. Removed a Verify line the page does not state.

Method: documentation only; no commands were run.
