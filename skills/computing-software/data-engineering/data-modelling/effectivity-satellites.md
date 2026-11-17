---
id: computing-software.data-engineering.data-modelling.effectivity-satellites
name: effectivity-satellites
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, data-vault, effectivity-satellite, link-satellite, driving-key, relationship-history, start-end-dates]
level: advanced
status: verified
description: "Track when Data Vault link relationships start and end with effectivity satellites: driving keys, start/end dates, reassignments, deletions and current-link queries."
sources:
  - https://automate-dv.readthedocs.io/en/latest/tutorial/tut_eff_satellites/
  - https://datavaultalliance.com/news/dv/understanding-data-vault-2-0/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Effectivity satellites

**Goal:** links record that a relationship ever existed; effectivity satellites record **when it was active**, so you can answer "which account manager owned this customer on 2026-03-01".

## Problem
`link_customer_manager` gets a row for (C1, M1), later (C1, M2). Links are insert-only, so both rows remain forever. Without effectivity, you cannot tell that M1 ended when M2 started.

## Driving key
The side of the link whose change ends the previous relationship. For "a customer has one manager at a time", the driving key is `customer`: a new manager for C1 closes the old (C1, M1) relationship.

## Structure
```
eff_sat_customer_manager
  hk_customer_manager   (link hash key)
  start_date
  end_date              (9999-12-31 for open)
  effective_from        (business date)
  load_dts, record_source
```

## Load logic (per batch)
1. For each driving key in staging, find the currently open link row(s) in the effectivity satellite.
2. If staging has a different link for that driving key, insert a **closing** row for the old link (`end_date = effective_from` of the new) and an **opening** row for the new link (`end_date = 9999-12-31`).
3. If the source signals deletion of a relationship (no row for the driving key in a full extract, or CDC delete), insert a closing row.
4. Insert-only: never update existing rows; the latest row per link hash key is its current state.

automate_dv macro:
```sql
{{ automate_dv.eff_sat(src_pk='HK_CUSTOMER_MANAGER', src_dfk='HK_CUSTOMER', src_sfk='HK_MANAGER',
                       src_start_date='START_DATE', src_end_date='END_DATE',
                       src_eff='EFFECTIVE_FROM', src_ldts='LOAD_DTS', src_source='RECORD_SOURCE',
                       source_model='stg_customer_manager') }}
```
(`src_dfk` driving foreign key, `src_sfk` secondary; parameter names confirmed in the automate_dv macros docs. The current-relationship query below was run on DuckDB with a M1 -> M2 reassignment and returned only (C1, M2).)

## Querying current relationships
```sql
with latest as (
  select *, row_number() over (partition by hk_customer_manager order by load_dts desc) rn
  from eff_sat_customer_manager)
select l.hk_customer, l.hk_manager
from link_customer_manager l
join latest e on e.hk_customer_manager = l.hk_customer_manager and e.rn = 1
where e.end_date = '9999-12-31';
```
Point in time: `where start_date <= :as_of and end_date > :as_of` on the latest version of each row as of the load time.

## Gotchas
- Choosing the wrong driving key closes relationships that should coexist (many-to-many cases may need no driving key: track each pair independently with source-provided start/end).
- Incremental (delta) sources cannot tell you a relationship ended unless they send deletes; full extracts or CDC are required for closure detection.
- Relationships that reopen (C1 back to M1) produce a new open row for the old link hash key: fine, latest row wins.

## Verify
- [ ] Each driving key has at most one open relationship at any time (test).
- [ ] Reassignment test: C1 M1 -> M2 produces a closing and an opening row.
