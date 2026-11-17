---
id: computing-software.data-engineering.data-modelling.normalization-and-denormalization-tradeoffs
name: normalization-and-denormalization-tradeoffs
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, normalization, denormalization, third-normal-form, 3nf, one-big-table, obt, wide-table, update-anomaly, nested-struct, columnar-storage, star-schema, snowflake-schema]
level: practitioner
status: draft
description: "Decide how normalized a model should be at each layer (3NF staging vs denormalized marts), and the specific failure modes of over/under-normalizing."   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources:
  - https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Normalization vs denormalization — the right amount per layer, not one global answer

**Goal:** stop treating "normalized" or "denormalized" as a house style applied everywhere; pick deliberately per layer based on who writes to it and who reads from it.

## 1. Why normalization rules (3NF) exist, and why columnar warehouses change the calculus
3NF (no partial or transitive dependencies on the key) exists to prevent **update anomalies**: with a customer's city stored redundantly on every one of their orders, updating their city means finding and updating every order row, and missing one leaves the data inconsistent with itself. This matters enormously in an OLTP system doing row-by-row writes. It matters far less for reads-only analytical data that is fully rebuilt/reloaded from source on each run — if the mart is regenerated from the normalized source of truth every load, there's no "update anomaly" risk because nothing is ever partially updated in place.

## 2. The standard layering (and why each layer's normalization level differs)
- **Raw/landing**: as close to source shape as possible, often not normalized at all in the relational sense — it's a copy, not a model. Normalization isn't the goal here; fidelity to source is.
- **Staging/3NF (or Data Vault)**: normalized or hub-style, optimized for **integration correctness** — a single definition of each entity, easy to audit, easy to add new sources to without redesign. Writes happen here; this is where update-anomaly protection earns its cost.
- **Marts (star schema, denormalized dimensions)**: deliberately denormalized — a dimension table holds the full `category > subcategory > product` hierarchy flattened into one row per product rather than split into a normalized `product → subcategory → category` chain of tables (that would be a **snowflake schema**, Kimball's term for an over-normalized star). Flattening trades redundant storage (cheap in a columnar warehouse) for **fewer joins per query** — the thing that actually matters for BI tool and analyst query performance and comprehension.
- **One Big Table (OBT) / wide marts**: pushes denormalization further, pre-joining facts and all relevant dimension attributes into a single wide table. Good for tools that can't do joins well (some BI semantic layers, simple dashboards) or for radically simplifying self-serve access; costly in storage and in "which column is the source of truth" clarity if multiple OBTs re-derive the same joined attribute slightly differently. Don't default to OBT everywhere — it's a specific tool for specific consumer limitations, not a universal upgrade over a star schema.

## 3. Snowflaking — usually a mistake in the mart layer
Normalizing a dimension table into a snowflake (splitting `product` into `product` + `category` + `subcategory` tables) saves storage and centralizes an update, but costs a join on every query that touches that dimension's attributes, and most BI tools and analysts find the extra joins a usability tax out of proportion to the storage saved — columnar compression already handles repeated string values (category names) efficiently without needing normalization to do it. Reserve snowflaking in marts for genuinely huge dimensions with independently-changing sub-hierarchies, not as a default "cleaner" choice.

## 4. Nested/repeated structures as a third option
Modern columnar formats (Parquet, BigQuery's nested/repeated fields, Snowflake's VARIANT) let you keep a one-to-many relationship (an order and its line items) as a single row with a nested array instead of either normalizing (two tables + a join) or denormalizing (duplicating order-level data across every line-item row). This avoids both the join cost and the duplication, at the cost of needing `UNNEST`/`FLATTEN`-aware query patterns and some BI tools handling nested fields poorly — evaluate per consumer before committing a mart's shape to nested structures.

## Verify
- [ ] Each layer's normalization level was a deliberate choice tied to that layer's actual write/read pattern, not a copy-pasted house style.
- [ ] No mart-layer dimension is snowflaked without a specific, named reason (dimension size, independent sub-hierarchy update cadence).
- [ ] A denormalized attribute's source of truth is documented — if it's rebuilt from staging on every load (safe) vs. mutated in place anywhere (anomaly risk).
- [ ] If nested/repeated structures are used, the consuming BI tool/query layer was confirmed to handle them before the mart shipped.
