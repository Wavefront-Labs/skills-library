---
id: computing-software.database-administration.sql.sql-schema-normalisation
name: sql-schema-normalisation
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-normalization, third-normal-form, denormalization, schema-design-basics]
level: practitioner
status: draft
description: "Normalise tables to 3NF/BCNF, recognise anomalies and denormalise deliberately."
sources: ["https://www.postgresql.org/docs/current/", "https://www.sqlite.org/docs.html", "https://www.iso.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Normalisation

- 1NF: atomic values, no repeating groups (no comma lists, no `phone1, phone2`). 2NF: no partial dependency on part of a composite key. 3NF: non-key columns depend only on the key ("the key, the whole key, and nothing but the key"). BCNF: every determinant is a candidate key.
- Symptoms of poor design: update anomaly (same fact in many rows), insertion anomaly (cannot record X without Y), deletion anomaly.
- Many-to-many needs a junction table with a composite primary key and two foreign keys.
- Model nullable attributes that apply to a subset as a separate table or subtype, not as many NULL columns.
- Denormalise on evidence: read-heavy aggregates, reporting stars, counters maintained by trigger or batch; document the source of truth and rebuild path.
- Naming: singular or plural tables consistently, `snake_case`, `id` and `<table>_id` foreign keys, no reserved words.
- Check design with sample queries before building.
