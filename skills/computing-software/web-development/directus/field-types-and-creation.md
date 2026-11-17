---
id: computing-software.web-development.directus.field-types-and-creation
name: field-types-and-creation
category: computing-software
field: web-development
product: directus
tags: [field-types, field-create, alias-fields, geospatial-types]
level: practitioner
status: docs-checked
description: "Create Directus fields: pick an interface, key and type from the unified type groups, and know alias fields, geospatial limits and immutable keys."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/01.data-model/2.fields.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Directus maps vendor types to one set:
- Text: String, Text, UUID, Hash, Alias
- Numeric: Integer, Big Integer, Float, Decimal
- Boolean: Boolean
- Date and time: Timestamp, DateTime, Date, Time
- Binary: Binary
- Structured: JSON, CSV
- Geospatial: Point, LineString, Polygon and their Multi variants (GeoJSON, only if the database has spatial extensions)

Alias fields have no database column (presentational and some relational fields).

Creating a field: choose an **interface** first (it drives available types), then the **key** (unique name per collection, used in Studio and API) and **type**.

Gotchas:
- Field key and type cannot be changed after creation, including casing. Use field name translations to relabel.
- Schema settings include length, default value, nullable, unique, indexed and searchable.
- Width (half, full, fill) is set from the three-dot menu on the data model page, not the field config. Half is max 380px and full 760px.

## Checked

2026-11-04: confirmed against the Directus docs Fields page: type groups, alias fields, geospatial note, interface/key/type, immutable key and type, schema settings, field width values. Split the Binary type into its own group and removed the unsupported verify line.

Method: documentation only; no commands were run.
