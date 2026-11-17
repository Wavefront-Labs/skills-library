---
id: computing-software.data-engineering.data-modelling.naming-standards-and-data-dictionary
name: naming-standards-and-data-dictionary
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, naming-standards, data-dictionary, naming-conventions, class-words, column-naming, abbreviations, sqlfluff, metadata-standards]
level: practitioner
status: draft
description: "Define naming standards and a data dictionary: table/column patterns, class words (_id, _at, _amount), approved abbreviations, units and currency, and enforcing them with linting."
sources:
  - https://www.dama.org/cpages/body-of-knowledge
  - https://docs.getdbt.com/best-practices/how-we-style/1-how-we-style-our-dbt-models
  - https://docs.sqlfluff.com/en/stable/rules.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Naming standards and the data dictionary

**Goal:** anyone can guess a column's meaning, type and unit from its name, and find the authoritative definition in one place.

## Naming rules (example standard)
- **Case:** `snake_case`, lowercase, no quoted identifiers.
- **Tables:** plural nouns for entities (`customers`), layer prefixes in transformed layers (`stg_`, `int_`, `fct_`, `dim_`).
- **Primary keys:** `<entity>_id` (`customer_id`), same name everywhere it appears as a foreign key.
- **Class words (suffixes) state the kind of value:**
| Suffix | Meaning | Type |
|---|---|---|
| `_id` | Identifier | string/int |
| `_at` | Timestamp (UTC unless suffixed `_local`) | timestamp |
| `_date` | Calendar date | date |
| `_amount` | Money, with currency in a sibling `_currency` column or suffix `_usd` | decimal |
| `_count` / `_qty` | Counts / quantities | integer |
| `_pct` / `_rate` | Ratio (state 0-1 vs 0-100 in the dictionary) | decimal |
| `is_` / `has_` prefix | Boolean | boolean |
| `_code` | Code from a reference list | string |
- **Units in names** when ambiguous: `duration_seconds`, `weight_kg`.
- **Approved abbreviations list** (e.g. `qty` allowed, `amt` spelled out as `amount`): publish it; no ad-hoc abbreviations.
- Avoid reserved words (`date`, `order`, `user`) as column names.

## Data dictionary entries
For each business term and each published column: name, definition (one or two sentences, business language), data type, allowed values/range, unit/currency, source system and derivation, owner, sensitivity (PII class), example values. Keep it **in the model code** (dbt YAML descriptions + doc blocks, or catalog) rather than a detached spreadsheet, so it versions with the schema.

## Enforcement
- SQL linting: SQLFluff rules for capitalisation and aliasing (`capitalisation.identifiers`, `aliasing.*`), plus custom checks.
- CI script over the dbt manifest or `information_schema` that flags booleans without `is_/has_`, timestamps not ending `_at`, undocumented columns in marts.
- Review checklist for new tables.

## Verify
- [ ] A random sample of 20 mart columns follows the standard and has dictionary entries.
- [ ] CI blocks a new column named `flag1` or `date`.
