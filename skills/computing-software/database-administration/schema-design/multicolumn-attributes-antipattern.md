---
id: computing-software.database-administration.schema-design.multicolumn-attributes-antipattern
name: multicolumn-attributes-antipattern
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, multicolumn-attributes, repeating-groups, sql-antipatterns, first-normal-form, schema-patterns]
level: practitioner
status: draft
description: "Replace the multicolumn attributes antipattern (tag1, tag2, tag3 or phone1..phone3 columns) with a dependent table, and migrate existing data safely."
sources:
  - https://pragprog.com/titles/bksap1/sql-antipatterns-volume-1/
  - https://www.postgresql.org/docs/current/ddl-constraints.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multicolumn attributes (tag1 / tag2 / tag3)

## The antipattern (Karwin, SQL Antipatterns)
```sql
CREATE TABLE bugs (id bigint PRIMARY KEY, summary text, tag1 text, tag2 text, tag3 text);
```
Problems:
- Search: `WHERE tag1 = 'crash' OR tag2 = 'crash' OR tag3 = 'crash'`, repeated in every query and hard to index.
- Add/remove: find which column is empty; concurrent updates race for the same "free" slot.
- Uniqueness: nothing stops `tag1 = tag2`.
- Growth: the fourth tag requires `ALTER TABLE` and changes to every query.
Same smell: `phone1/phone2/phone3`, `address_line_home/work`, `q1_sales..q4_sales` (see also metadata tribbles).

## The fix: dependent table
```sql
CREATE TABLE bug_tags (
  bug_id bigint NOT NULL REFERENCES bugs(id) ON DELETE CASCADE,
  tag text NOT NULL,
  PRIMARY KEY (bug_id, tag));
CREATE INDEX ON bug_tags (tag);

SELECT b.* FROM bugs b JOIN bug_tags t ON t.bug_id = b.id WHERE t.tag = 'crash';
INSERT INTO bug_tags VALUES (1234, 'performance') ON CONFLICT DO NOTHING;
```
For typed multi-values (phones with kinds), add the attribute: `contact_phones(contact_id, kind, number)` with `UNIQUE (contact_id, kind)` if one per kind.

## Migration
```sql
INSERT INTO bug_tags (bug_id, tag)
SELECT id, tag FROM (
  SELECT id, tag1 AS tag FROM bugs UNION ALL
  SELECT id, tag2 FROM bugs UNION ALL
  SELECT id, tag3 FROM bugs) s
WHERE tag IS NOT NULL AND tag <> ''
ON CONFLICT DO NOTHING;
```
Then expand/contract: dual-write, switch reads to `bug_tags`, drop old columns after a transition period.

## When fixed columns are legitimate
When positions carry distinct meaning and the count is fixed by the domain (e.g. `address_line1`, `address_line2` in a postal format; `home_phone` vs `mobile_phone` with different rules). Then they are different attributes, not a repeating group.

## Verify
Counts: number of non-empty old tag values equals rows inserted into `bug_tags` (minus duplicates); queries by tag use the `bug_tags(tag)` index.
