---
id: computing-software.data-engineering.data-modelling.reverse-engineering-a-schema
name: reverse-engineering-a-schema
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, reverse-engineering-schema, information-schema, schema-discovery, implicit-foreign-keys, data-profiling, erd-generation, legacy-database, source-systems]
level: advanced
status: draft
description: "Document an unfamiliar source schema: extract tables/keys from information_schema, infer undeclared foreign keys and grain by profiling, generate an ERD, and confirm with owners."
sources:
  - https://www.postgresql.org/docs/current/information-schema.html
  - https://schemaspy.org/
  - https://www.dama.org/cpages/body-of-knowledge
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reverse-engineering an existing schema

**Goal:** before building pipelines on a legacy or vendor database, know its entities, keys, relationships and grain, including the rules nobody declared.

## 1. Extract declared structure
```sql
-- tables, columns, types (Postgres; similar views exist in most RDBMS)
select table_schema, table_name, column_name, data_type, is_nullable
from information_schema.columns where table_schema not in ('pg_catalog', 'information_schema')
order by 1, 2, ordinal_position;
-- declared PK/FK
select tc.table_name, tc.constraint_type, kcu.column_name, ccu.table_name as ref_table, ccu.column_name as ref_column
from information_schema.table_constraints tc
join information_schema.key_column_usage kcu using (constraint_schema, constraint_name)
left join information_schema.constraint_column_usage ccu using (constraint_schema, constraint_name)
where tc.constraint_type in ('PRIMARY KEY', 'FOREIGN KEY');
```
Tools: SchemaSpy (`java -jar schemaspy.jar -t pgsql -host ... -db ... -o out/`) produces an HTML ERD and orphan-table reports; DBeaver ER diagrams; `dbt-codegen` for warehouse copies.

## 2. Infer what is not declared
Many systems (ORM-managed, vendor apps) declare no FKs.
- **Name matching:** columns named `<entity>_id` or `<table>id` -> candidate FK to that table's PK.
- **Containment test:** `select count(*) from child c left join parent p on c.x = p.id where c.x is not null and p.id is null` -> near zero = likely FK.
- **Grain/uniqueness:** `select count(*), count(distinct col1, col2) from t` to find the real natural key.
- **Status/type columns:** `select col, count(*) group by col` to discover enums and soft-delete flags (`is_deleted`, `status = 'X'`).
- **Audit columns:** `created_at`/`updated_at` presence and whether `updated_at` actually changes (needed for incremental extraction).
- **Polymorphic references:** `(owner_type, owner_id)` pairs pointing to different tables.

## 3. Read the code and data history
Application ORM models, stored procedures and views often encode the real relationships. Query logs (top queries' joins) show how the app navigates the schema.

## 4. Document and confirm
Produce an ERD (DBML/Mermaid) marking declared vs inferred relationships, grain per table, CDC/incremental suitability, and open questions. Review with the source system owner; record answers in the data dictionary.

## Verify
- [ ] Every table you will extract has a confirmed grain and key.
- [ ] Inferred FKs have measured orphan rates noted.
- [ ] Open questions list is closed or explicitly accepted as risk.
