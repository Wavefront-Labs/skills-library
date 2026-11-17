---
id: computing-software.data-engineering.data-warehouse-architecture.kimball-vs-inmon-and-one-big-table
name: kimball-vs-inmon-and-one-big-table
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, kimball, inmon, corporate-information-factory, bus-architecture, conformed-dimensions, data-mesh, enterprise-data-warehouse, one-big-table, architecture-philosophy, bottom-up-vs-top-down]
level: advanced
status: draft
description: "Choose a warehouse architecture philosophy (Kimball bus, Inmon CIF, OBT/wide-table) deliberately, based on org size and change rate, not fashion."   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources:
  - https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/
  - https://www.inmoncif.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Kimball vs Inmon vs One Big Table — pick the philosophy for a reason

**Goal:** choose a warehouse-wide architectural philosophy deliberately before the first mart gets built, because retrofitting conformance or normalization across dozens of marts built without a plan is far more expensive than designing for it up front. (This skill is the organization-wide philosophy; computing-software.data-engineering.data-warehouse-architecture.medallion-layering is the physical bronze/silver/gold layering most of these philosophies get implemented through today, and computing-software.data-engineering.data-modelling.normalization-and-denormalization-tradeoffs is the per-layer normalization decision.)

## 1. Kimball — bus architecture, bottom-up, conformed dimensions
Build one subject area's star schema at a time (orders, then shipments, then support tickets), each delivering value fast, **but** every dimension shared across subject areas must be a **conformed dimension** — the same `dim_customer` (same keys, same attributes, same grain) used by every fact table that touches a customer, not a slightly-different copy per subject area. The "bus" is the documented matrix of which facts use which conformed dimensions, agreed up front even though marts are built incrementally. Skipping conformance is how an org ends up with three different `customer_id` definitions across finance, sales and support marts that don't reconcile — the single most common Kimball-in-name-only failure.
- Fast time-to-value, works well for most analytics-focused teams, is what most modern cloud-warehouse tooling (dbt, Looker/dbt's semantic layer) is implicitly built around.

## 2. Inmon — Corporate Information Factory, top-down, normalized EDW first
Build a single normalized (3NF) enterprise data warehouse as the integrated system of record first, with departmental/subject-area data marts built *from* it afterward as summarized, denormalized extracts for specific consumers. The EDW is the single source of truth; marts are disposable/rebuildable views on top of it. This front-loads integration cost (a comprehensive enterprise model before any mart ships) in exchange for avoiding the "three customer_id definitions" problem structurally — the EDW enforces one definition before marts can diverge.
- Slower to first value, historically associated with large enterprises/regulated industries with the budget and patience for the upfront modeling; a smaller team building for speed usually can't justify this path first.
- Modern Data Vault 2.0 (see computing-software.data-engineering.data-modelling.data-vault-modelling) is largely the contemporary implementation of Inmon's "integrated system of record first" idea, replacing hand-normalized EDW modeling with hub/link/satellite structures designed for the same integration goal with better load parallelism.

## 3. One Big Table / wide-mart approach
Neither Kimball's star-schema bus nor Inmon's normalized EDW — instead, pre-join everything a specific consumer needs into one (or a few) wide, flattened tables, accepting redundancy and multiple sources of truth for the same joined attribute across different OBTs in exchange for radical query simplicity. Reasonable as a **consumption-layer pattern on top of either philosophy** (a Kimball mart rendered as an OBT for a specific dashboard tool that can't join well) but risky as the *only* architecture — without an underlying conformed/integrated layer, every OBT re-derives its own version of shared logic, and definitions drift between them with no mechanism to catch it.

## 4. Data mesh as a different axis entirely
Data mesh (domain-oriented ownership, data-as-a-product, federated governance) is orthogonal to Kimball/Inmon/OBT — it's an organizational/ownership model, not a schema-design philosophy. A mesh can be implemented with Kimball-style conformed dimensions per domain, Data-Vault-style integration, or OBT products — the mesh question is "who owns and publishes this data," the Kimball/Inmon question is "how is it structurally modeled." Don't treat adopting one as a substitute for deciding the other.

## 5. Choosing in practice
Most teams today default to a Kimball-flavored bus architecture implemented via medallion layering in a cloud warehouse (dbt + conformed dimension discipline), reaching for Data Vault/Inmon-style integration only when genuinely multi-source, high-change, or audit-heavy, and using OBT selectively at the consumption edge for specific BI-tool limitations — not as the whole architecture.

## Verify
- [ ] A documented bus matrix (or equivalent) names every conformed dimension and every fact table that uses it, before a second subject area is built.
- [ ] The same business key (customer, product) resolves to the same surrogate key across every mart that references it — checked by an actual cross-mart join test, not assumed.
- [ ] The choice between Kimball/Inmon/Data-Vault-style integration was made against actual source-system count and change-rate, not copied from a vendor's reference architecture unexamined.
- [ ] Any OBT in production has a documented upstream source of truth it was derived from, not an independently re-implemented join.
