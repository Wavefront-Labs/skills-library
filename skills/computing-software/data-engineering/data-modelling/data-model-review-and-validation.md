---
id: computing-software.data-engineering.data-modelling.data-model-review-and-validation
name: data-model-review-and-validation
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, data-model-review, design-review, model-validation, data-governance]
level: advanced
status: draft
description: "Run a data model review: checklist for grain, keys, naming, normalisation, history, constraints, performance and ownership, with sign-off and automated checks."
sources:
  - https://www.dama.org/cpages/body-of-knowledge
  - https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/
  - https://dbt-labs.github.io/dbt-project-evaluator/latest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data model review and validation

**Goal:** catch design errors before tables are built and consumed, when they are cheap to fix.

## Inputs to the review
- Business questions the model must answer (5-10 concrete queries).
- Logical diagram (entities, relationships, cardinalities) and physical DDL/dbt models.
- Source-to-target mapping for each column.

## Checklist
**Grain and keys**
- Every table states its grain in one sentence ("one row per order line per day").
- Primary key declared and tested (unique + not null); surrogate vs natural key decision written down.
- Foreign keys resolvable (relationships tests); unknown/late members handled.
**Semantics**
- Names follow the naming standard; units and currencies explicit (`amount_eur`, `duration_s`).
- Additivity of each measure noted (additive, semi-additive, non-additive).
- Nullable columns justified; sentinel values documented.
**History**
- Which attributes need history (SCD type per attribute); effective dating consistent.
- Deletes: soft delete flag or hard delete detection.
**Fit for use**
- The 5-10 business queries written against the model and executed on sample data.
- No fan-out joins needed for common questions.
**Operational**
- Partitioning/clustering for main filters; expected size and growth.
- Owner, SLA, PII classification, retention.

## Validation steps
1. Prototype on a sample (dbt with `--empty` then a small date range).
2. Reconcile key metrics to the source/system of record (counts, sums by day).
3. Peer review by someone outside the team who will query it.
4. Automate what you can: tests for PK/FK, project evaluator rules, naming lint.

## Gotchas
- Reviewing only the diagram: most issues surface when you write the actual queries.
- Approving without the consumer present: they spot missing attributes immediately.

## Verify
Sign-off record lists the queries tested and the reconciliations passed; tests for keys exist in the repo.
