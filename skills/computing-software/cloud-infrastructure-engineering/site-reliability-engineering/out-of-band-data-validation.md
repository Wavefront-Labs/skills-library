---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.out-of-band-data-validation
name: out-of-band-data-validation
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [out-of-band-data-validation, data-validation-pipeline, data-integrity, invariants, early-detection]
level: advanced
status: docs-checked
description: "Out-of-band data validators per the SRE Book third layer: pick invariants that would devastate users, run them often enough, rate-limit them, and give on-call tooling."
sources: ["https://sre.google/sre-book/data-integrity/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Out-of-band data validation

Source: SRE Book, "Data Integrity: What You Read Is What You Wrote", "Third Layer: Early Detection".

## Why
- Bad data propagates: references to missing or corrupt data are copied and links fan out, and later transactions and format changes make restoring from a given backup harder as time passes. The sooner a loss is known, the easier and more complete recovery can be.
- Cloud developers face referential integrity between datastores, schema changes, aging code, zero-downtime data migrations and evolving integration points. Without conscious effort the data quality of a growing service degrades.
- Do not delegate integrity to the storage API alone: implementations of consensus algorithms are "riddled with hacks, optimizations, bugs, and educated guesses", so "trust storage systems, but verify". The book also says to check the most critical data with out-of-band validators even when API semantics suggest you need not.

## What to validate
- Validators are tricky: too strict and simple, appropriate changes make them fail, so engineers abandon them; too lax and user-affecting corruption slips through. Only validate invariants that cause devastation to users.
- The book's example: Google Drive periodically validates that file contents align with listings in Drive folders, and its developers enhanced the validators to fix such inconsistencies automatically, which turned a 2013 data loss emergency into business as usual.

## How often and at what cost
- Gmail developers know bugs introducing inconsistencies are detected within 24 hours and "shudder at the thought" of running validators less often than daily.
- Validators can be expensive: a significant part of Gmail's compute footprint supports daily validators, and they lower server-side cache hit rates. Gmail has knobs to rate-limit validators and refactors them to reduce disk contention (one refactoring cut disk spindle contention by 60% without much reducing the invariants covered). The largest Gmail validator is divided into 10 to 14 shards, one validated per day.
- As a service scales, sacrifice rigor in the daily validators but keep catching the most disastrous scenarios within 24 hours, with more rigorous validation at reduced frequency. Compute Storage had to find a more efficient way to verify metadata when its validators could no longer finish within a day.

## What effective validation needs
Validation job management; monitoring, alerts and dashboards; rate-limiting features; troubleshooting tools; production playbooks; and validation APIs that make validators easy to add and refactor. Failed validations can be hard to troubleshoot because intermittent causes can vanish in minutes to days, so drill-down into validation audit logs is essential (Gmail on-call gets playbook entries, a BigQuery-like investigation tool and a dashboard).

Small teams cannot afford to build all of that, so the book suggests a central infrastructure team provide the framework while product teams maintain the custom business logic of each validator.

## Checked
- 2026-11-08: all points were confirmed on the SRE Book Data Integrity page.
- Removed: the invariant table, SQL example, metric name, read-only credential and weekly full-scan advice, the "validator shares code" and backup-retention gotchas, and the Great Expectations/Soda/dbt tooling note (the Great Expectations page cited was an introduction stub and is dropped from sources).
Method: docs-only read of cited pages, 2026-11-08
