---
id: computing-software.database-administration.schema-design.entity-attribute-value-antipattern
name: entity-attribute-value-antipattern
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, schema-patterns, eav, entity-attribute-value, jsonb, custom-fields, sql-antipatterns, dynamic-attributes]
level: practitioner
status: verified
description: "Recognise the entity-attribute-value antipattern, its integrity and query costs, and replace custom-field EAV with JSON columns, subtype tables or sparse columns."
sources:
  - https://pragprog.com/titles/bksap1/sql-antipatterns-volume-1/
  - https://www.postgresql.org/docs/current/datatype-json.html
  - https://learn.microsoft.com/en-us/sql/relational-databases/tables/use-sparse-columns
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entity-attribute-value (EAV) antipattern

**Goal:** support user-defined or highly variable attributes without the integrity loss and query pain of a generic attribute table.

## What EAV looks like
```sql
CREATE TABLE attributes (entity_id bigint, attr_name text, attr_value text, PRIMARY KEY (entity_id, attr_name));
```
## Why it hurts
- No types: dates, numbers and booleans as text; no CHECK, NOT NULL or FK per attribute.
- Reassembling one entity needs a pivot or one self-join per attribute:
  ```sql
  SELECT e.id, c.attr_value AS color, s.attr_value AS size
  FROM products e
  LEFT JOIN attributes c ON c.entity_id = e.id AND c.attr_name = 'color'
  LEFT JOIN attributes s ON s.entity_id = e.id AND s.attr_name = 'size';
  ```
- Filtering on several attributes requires multiple joins or `GROUP BY ... HAVING count = N`; the planner estimates poorly.
- Typos in `attr_name` create new "attributes" silently.

## Better options
| Situation | Use |
|---|---|
| Known attributes per product type | Subtype tables (class table inheritance) or columns on the main table |
| Truly user-defined custom fields | JSON column (`jsonb` in PostgreSQL, JSON in MySQL/SQL Server) + validation in app or JSON schema; GIN or expression indexes on queried keys |
| Many optional columns, SQL Server | `SPARSE` columns + column sets (see SQL Server docs; not run here) |
| Search / faceting across attributes | Search engine (Elasticsearch) fed from the DB |

```sql
ALTER TABLE products ADD COLUMN attrs jsonb NOT NULL DEFAULT '{}';
CREATE INDEX ON products USING gin (attrs jsonb_path_ops);
SELECT * FROM products WHERE attrs @> '{"color": "red", "size": "M"}';
```

## If EAV is mandated (legacy, clinical systems)
- Typed value columns (`value_int`, `value_date`, `value_text`) with a CHECK that exactly one is set.
- An attribute definition table (name, type, required) referenced by FK.
- Materialised pivot views for reporting.

## Verify
After migrating to JSON, a multi-attribute filter is one predicate using the GIN index (`EXPLAIN` shows Bitmap Index Scan on a large enough table; on a tiny table the planner prefers a Seq Scan) instead of N self-joins.
