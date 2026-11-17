---
id: computing-software.database-administration.schema-design.fourth-and-fifth-normal-form
name: fourth-and-fifth-normal-form
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, fourth-normal-form, fifth-normal-form, multivalued-dependency, join-dependency, keys-normalisation]
level: practitioner
status: verified
description: "Recognise multivalued and join dependencies that 3NF/BCNF tables can still contain, and decompose to 4NF and 5NF to remove redundant combinations."
sources:
  - https://en.wikipedia.org/wiki/Fourth_normal_form
  - https://en.wikipedia.org/wiki/Fifth_normal_form
  - https://www.bkent.net/Doc/simple5.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 4NF / 5NF and multivalued dependencies

Most designs stop at 3NF/BCNF. 4NF and 5NF problems appear in tables whose key is all or most of their columns (junction tables mixing independent facts).

## 4NF: independent multivalued facts
Table `employee_skills_languages(employee, skill, language)`: an employee has several skills and speaks several languages, independently. To record 2 skills × 3 languages you need 6 rows (computed: the cross product has 6 rows); adding a language means adding one row per skill. This is a **multivalued dependency** (employee →→ skill, employee →→ language) not implied by a key.

Decompose:
```sql
CREATE TABLE employee_skills    (employee_id bigint, skill_id int,    PRIMARY KEY (employee_id, skill_id));
CREATE TABLE employee_languages (employee_id bigint, language_id int, PRIMARY KEY (employee_id, language_id));
```
Rule: if two multi-valued attributes are independent of each other, they belong in separate tables.

Counter-case: if the combination itself is a fact ("can teach skill X in language Y"), the three-column table is correct and in 4NF.

## 5NF: join dependencies
Classic agent-company-product: an agent sells a product for a company. If the business rule is "if an agent represents company C, and sells product P, and C makes P, then the agent sells P for C", the three-column table holds redundant rows derivable from three two-column tables (agent-company, agent-product, company-product). Decompose into the three pairs; rejoining them reproduces exactly the original facts.

Without that symmetric rule, the three-way table is not decomposable and already in 5NF. 5NF depends on business rules, not just data patterns: ask the domain expert.

## Spotting it in practice
- Junction tables with 3+ foreign keys and no other attributes.
- Inserts that must add many rows to keep the table "complete".
- Update anomalies: removing a skill requires deleting several rows.

## Trade-off
Further decomposition means more joins for reports that need the combinations; create a view for the combined shape.

## Verify
For the original table, check whether `SELECT DISTINCT a, b` joined to `SELECT DISTINCT a, c` on `a` reproduces exactly the original rows (then it was a non-4NF multivalued dependency and should be split). Run on the skills x languages example: both give 6 rows.
