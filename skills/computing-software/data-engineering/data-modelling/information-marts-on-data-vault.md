---
id: computing-software.data-engineering.data-modelling.information-marts-on-data-vault
name: information-marts-on-data-vault
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, information-mart, data-vault, business-vault, dimensional-modelling]
level: advanced
status: draft
description: "Build information marts on a Data Vault: PIT and bridge tables, deriving dimensions and facts, virtualised vs materialised marts, and performance patterns."
sources:
  - https://books.google.com/books?vid=ISBN9780128025109
  - https://automate-dv.readthedocs.io/en/latest/tutorial/tut_point_in_time/
  - https://automate-dv.readthedocs.io/en/latest/tutorial/tut_bridges/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Information marts on top of a vault

**Goal:** turn the raw/business vault into consumer-friendly star schemas without losing auditability.

## Layers
Raw vault (hubs, links, satellites, as loaded) -> business vault (computed satellites, SAL resolution, PIT, bridges) -> **information marts** (dimensions/facts or wide tables for a use case).

## PIT (point-in-time) tables
One row per hub key per snapshot date, with the satellite keys/load dates valid at that time. Makes dimension queries equi-joins instead of range joins across many satellites.
```sql
select p.customer_hk, p.snapshot_date, s1.name, s2.segment
from pit_customer p
join sat_customer_details s1 on s1.customer_hk = p.customer_hk and s1.load_date = p.sat_details_ldts
join sat_customer_crm s2     on s2.customer_hk = p.customer_hk and s2.load_date = p.sat_crm_ldts;
```

## Bridge tables
Pre-join hub/link paths (order -> customer -> account) with keys per snapshot, so facts can join to dimensions in one step.

## Deriving dimensions and facts
- Dimension = hub + PIT + satellites, current view (SCD1) or per snapshot (SCD2-like by snapshot date).
- Fact = link (+ link satellites with measures) joined through bridge to dimension keys; grain = the link's unit of work.
- Use hash keys from the vault as dimension keys or generate integer surrogate keys in the mart.

## Virtual vs materialised
- Views over PIT/bridge (virtual marts): always current, flexible, slower.
- Materialised tables (dbt models): fast for BI; rebuild/incremental per snapshot.
Start virtual, materialise hot marts.

## Gotchas
- Building marts directly from raw satellites with range joins is slow and error-prone: build PITs first.
- Business rules belong in business vault or mart, not in raw vault loads.
- Snapshot frequency of PITs defines the history granularity users see.

## Verify
Mart dimension row counts per snapshot equal hub key counts present at that snapshot; facts reconcile to link satellite totals.
