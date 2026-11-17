---
id: computing-software.data-engineering.data-modelling.data-vault-modelling
name: data-vault-modelling
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, data-vault, data-vault-2.0, hub, link, satellite, business-key, hash-key, point-in-time-table, bridge-table, raw-vault, business-vault, auditability, enterprise-data-warehouse]
level: advanced
status: draft
description: "Model with Data Vault 2.0 (hubs, links, satellites) for auditable, highly-adaptable enterprise warehouses."   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources:
  - https://www.scalefree.com/data-vault/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data Vault 2.0 — model for change, not for query speed

**Goal:** build a warehouse layer that survives new sources, merging systems, and audit requirements without a redesign — at the cost of needing a second (business vault/mart) layer before anyone queries it directly.

## 1. The three core structures
- **Hub**: one row per unique business key (e.g. `customer_id`), with a surrogate hash key (`hub_hashkey`, usually MD5/SHA of the business key), the business key itself, load timestamp, and record source. Hubs never update — a business key seen before is never re-inserted, only referenced.
- **Link**: represents a relationship/transaction between hubs (e.g. `order` linking `customer` hub and `product` hub), keyed by a hash of the combined business keys of what it connects. Links are also insert-only — a new relationship occurrence is a new link row, never an update.
- **Satellite**: holds the actual descriptive attributes and **all their history**, keyed by the parent hub/link's hash key plus a load timestamp, with a hashdiff (hash of all tracked columns) to detect whether a new row is needed. A new source extract that produces the same hashdiff as the latest satellite row is **not inserted** — this is what keeps satellites from growing on every load when nothing changed.
- **Why split this way:** structure (hubs/links) and descriptive data (satellites) change independently and at different rates — adding a new attribute means adding a new satellite, not altering an existing wide table; a new source system for the same business entity means a new satellite off the existing hub, not a schema migration across the whole model.

## 2. Loading pattern — insert-only, parallel-loadable
Every table is append-only; nothing is ever updated or deleted in the raw vault (this is the audit/compliance selling point — full history, including corrections, is preserved as new rows, never overwritten). Because hubs, links and satellites have no foreign-key-enforced load order dependency on each other beyond hash key existence, loads can be **massively parallelized** across many source feeds — a major operational win over a star schema's typically more sequential ETL, but it means load logic must handle "satellite arrived before its hub row was committed" gracefully (insert the hub row as part of the same load, or resolve in a staging step first).

## 3. Raw vault vs business vault
- **Raw vault**: a direct, unmodified capture of source data in hub/link/satellite form — no business rules, no deduplication logic beyond the mechanical hashdiff check, no conformed definitions across sources. This is deliberate: it is the permanent, auditable record of "what the source said, when."
- **Business vault**: a second layer applying business rules, same-as links (resolving "these two customer records are really the same person" across sources), computed satellites, and conformance — built *on top of* the raw vault, re-derivable/re-runnable if the rules change, never replacing the raw vault's untouched history.
- **Information mart**: the actual query-facing layer, usually a dimensional model (star schema — see computing-software.data-engineering.data-modelling.dimensional-modelling-and-scd) built from business vault + raw vault. Nobody should query hubs/links/satellites directly in production BI — the model is optimized for load flexibility and auditability, not read performance; point BI tools at the mart.

## 4. When it's the wrong tool
Data Vault's overhead (many more tables, more joins per query, a mandatory mart layer before anyone gets value) only pays off at genuine enterprise scale: multiple source systems for the same entities, frequent structural change, strict audit/lineage requirements (regulated industries), or long-lived warehouses expected to integrate systems not yet known at design time. For a single-source, stable-schema analytics warehouse, a straightforward dimensional model is less work end to end — don't adopt Data Vault for its reputation; adopt it for the specific flexibility/audit problem it solves.

## Verify
- [ ] Hub/link hash keys are computed identically (same algorithm, same key ordering/concatenation convention) across every loading job — a convention drift here silently fragments what should be one entity into two.
- [ ] A satellite load with unchanged source data produces zero new rows (hashdiff comparison is actually being checked, not just timestamp-appended blindly).
- [ ] Raw vault tables have no UPDATE or DELETE statements anywhere in the load code.
- [ ] A business mart/star schema exists and is what BI tools actually query — not the raw vault directly.
