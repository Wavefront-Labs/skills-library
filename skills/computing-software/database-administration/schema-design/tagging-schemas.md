---
id: computing-software.database-administration.schema-design.tagging-schemas
name: tagging-schemas
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, tagging-schema, tags, many-to-many, schema-patterns, folksonomy]
level: practitioner
status: verified
description: "Design tagging schemas: normalised tags plus junction table, AND/OR tag queries that use indexes, tag normalisation, counts, and array or JSON alternatives."
sources:
  - https://www.postgresql.org/docs/current/gin.html
  - https://pragprog.com/titles/bksap1/sql-antipatterns-volume-1/
  - https://use-the-index-luke.com/sql/join
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tagging schemas

## Normalised design ("toxi" schema)
```sql
CREATE TABLE tags (id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY, name text NOT NULL,
  slug text NOT NULL UNIQUE);                 -- normalised form: lower-case, trimmed
CREATE TABLE item_tags (item_id bigint NOT NULL REFERENCES items ON DELETE CASCADE,
  tag_id int NOT NULL REFERENCES tags ON DELETE CASCADE,
  tagged_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (item_id, tag_id));
CREATE INDEX ON item_tags (tag_id, item_id);
```
Normalise on write (`slug = lower(trim(name))`, Unicode NFC) to avoid `Postgres`, `postgres `, `PostgreSQL` duplicates; keep synonyms in a mapping table if needed.

## Queries
Items with tag X:
```sql
SELECT i.* FROM items i JOIN item_tags it ON it.item_id = i.id JOIN tags t ON t.id = it.tag_id WHERE t.slug = 'redis';
```
Items with ALL of tags (AND):
```sql
SELECT it.item_id FROM item_tags it JOIN tags t ON t.id = it.tag_id
WHERE t.slug IN ('redis','cluster')
GROUP BY it.item_id HAVING count(*) = 2;           -- = number of tags requested
```
Items with ANY (OR): same without HAVING, with `DISTINCT`. Exclusion (NOT tag): `NOT EXISTS`.

## Tag counts / clouds
`count(*) GROUP BY tag_id` gets expensive at scale; maintain `tags.usage_count` via triggers or periodic refresh (materialised view), accepting slight staleness.

## Alternatives
| Option | When |
|---|---|
| PostgreSQL `text[]` + GIN (`tags @> '{redis,cluster}'` for AND, `&&` for OR) | Tags are plain labels, no per-tag metadata, read with the item |
| JSON array + multi-valued index (MySQL 8.0.17+, queried with `MEMBER OF()`/`JSON_CONTAINS()`/`JSON_OVERLAPS()`) | Same idea in MySQL |
| Search engine (Elasticsearch `keyword` field) | Faceted search with counts at scale |
| Comma-separated string | Never (jaywalking) |

## Multi-tenant and permissions
Tag namespaces per tenant: `UNIQUE (tenant_id, slug)`; include `tenant_id` in the junction PK to keep tags from crossing tenants.

## Verify
The AND query returned the expected item on PostgreSQL 18. EXPLAIN for the AND query uses `item_tags (tag_id, item_id)` index scans; test data with variant spellings maps to one tag row.
