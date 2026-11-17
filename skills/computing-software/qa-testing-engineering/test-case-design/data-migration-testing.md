---
id: computing-software.qa-testing-engineering.test-case-design.data-migration-testing
name: data-migration-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [migration-testing, data-migration-testing, maintenance-testing, etl-testing, reconciliation, retirement-testing]
level: practitioner
status: draft
description: "Test data migrations and system retirements: mapping review, row counts and checksums, sample comparison, transformation rules, rerun and rollback."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data migration and retirement testing

**Goal:** all data that should move arrives complete, correctly transformed, and usable in the target system. ISTQB CTFL v4.0 2.3.

## Plan
- Review the **mapping specification** (source field -> transform -> target field), defaults for missing values, rejected-record rules.
- Get a **production-sized** (masked) copy for at least one full rehearsal; migration speed and edge cases only show at scale.

## Checks
1. **Counts**: rows per table/entity source vs target, minus documented rejects.
   ```sql
   SELECT COUNT(*) FROM src.customers WHERE active = 1;   -- vs
   SELECT COUNT(*) FROM tgt.customer;
   ```
2. **Aggregates / checksums**: sums of balances, counts per status, per month; hash of concatenated key fields per row compared between systems.
3. **Field-level sample comparison**: random sample plus targeted edge cases (nulls, max lengths, special characters, unicode, old date formats, deleted/closed records).
4. **Transformation rules**: each rule exercised by at least one record.
5. **Referential integrity**: no orphans in target.
6. **Business validation**: users run key processes on migrated data (open old order, refund it).
7. **Rerun / delta** migration and **rollback** procedure, timed against the cut-over window.

## Retirement
Archive data per retention rules, verify archived data can be retrieved and read, and decommissioned interfaces no longer receive traffic.

## Gotchas
- Character encoding (Latin-1 to UTF-8) silently corrupts names; include accented and CJK samples.
- Time zone shifts on timestamps; compare in UTC.

## Verify
A reconciliation report signed off by data owners: counts, aggregates and sample comparison all match or are explained.
