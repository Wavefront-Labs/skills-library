---
id: computing-software.web-development.directus.collection-create-primary-key
name: collection-create-primary-key
category: computing-software
field: web-development
product: directus
tags: [collection-create, primary-key-type, immutable-names, directus-prefix]
level: practitioner
status: docs-checked
description: "Create a Directus collection and choose its primary key type, knowing the collection name and key strategy cannot be changed afterwards."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/01.data-model/1.collections.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Collections are database tables plus Directus metadata. Create them from the Data Model settings in the Data Studio, via the Collections API, or directly in the database.

Decide before creating:
- **Name**: unique, case sensitive, used across the Studio and APIs. It cannot be changed afterwards, including casing. You can only override its display with collection naming translations.
- **Primary key type**, also fixed once selected:
  - Auto-incremented integer (1 to 2^31-1).
  - Auto-incremented big integer (1 to 2^63-1), only on MySQL and PostgreSQL.
  - Generated UUID.
  - Manually entered string; Directus forbids duplicates.
- The wizard can add optional fields: archived, sort, and created/updated by and when.

Gotchas:
- Directus-specific settings live only in `directus_` system collections, so removing Directus leaves no proprietary data in your own tables.
- Primary keys are used in relationships and the Items API.

## Checked

2026-11-04: collection creation routes, immutable name and key type, the four ID types with ranges and the MySQL/PostgreSQL restriction for big integers, optional wizard fields and the directus_ prefix note confirmed against the Directus Collections page. Removed a Verify line the page does not state.

Method: documentation only; no commands were run.
