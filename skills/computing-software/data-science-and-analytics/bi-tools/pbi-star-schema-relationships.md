---
id: computing-software.data-science-and-analytics.bi-tools.pbi-star-schema-relationships
name: pbi-star-schema-relationships
category: computing-software
field: data-science-and-analytics
product: bi-tools
tags: [power-bi-star-schema, pbi-relationships, cross-filter-direction, pbi-modelling]
level: practitioner
status: docs-checked
description: "Model facts and dimensions as normalized tables with one-to-many relationships, role-playing date tables and explicit measures."
sources:
  - https://learn.microsoft.com/power-bi/guidance/star-schema
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Star schema in Power BI
- Classify tables as dimension or fact. There is no table property for this: the one-to-many (or many-to-one) relationship cardinality decides it; the "one" side is the dimension, the "many" side the fact.
- Strive for normalized fact and dimension tables; when a source is a denormalized export, shape it into several tables with Power Query. A snowflake dimension may be merged into a single denormalized table (generally the benefits outweigh multiple tables), at the cost of redundant data and storage.
- Add surrogate keys (index columns) when the source lacks a unique key; merge the index into the "many" side to create the one-to-many relationship.
- Explicit measures are needed when authors query with MDX (Analyze in Excel, MDX paginated reports) and to control how columns are summarized (for example, hide Unit Price and expose min/max/average measures).
- Many-to-many dimension relationships: the recommended design is a factless bridging table. See the Microsoft many-to-many and bi-directional relationship guidance articles.
## Gotchas
- Only one relationship between two tables can be active; others are inactive and are used only through a DAX measure with `USERELATIONSHIP`.
- For role-playing dimensions (order, ship, delivery date), a common technique is one dimension table per role, each with a single active relationship; this duplicates the date table (more storage, rarely a concern) and removes the need for per-role measures. Rename columns per role (for example Ship Year).
- Hiding columns does not stop report authors on Power BI Desktop live connections from showing hidden fields.
## Verify
- [ ] Model view shows a clean star; totals match the source.

## Checked
Confirmed on the star schema guidance page: table type via cardinality, normalization guidance, snowflake dimensions, surrogate keys, implicit versus explicit measures and MDX reasons, bridging table recommendation, inactive relationships and USERELATIONSHIP, role-playing dimension technique, hidden-field caveat. Removed: single-direction filter default, "dedicated Date table marked as a date table", "avoid bidirectional filtering" and "flat wide tables bloat memory", which the page only points to other articles for or does not state.
Method: docs-checked 2026-11-09 against the Microsoft Learn star schema guidance page (grep plus sections read).
