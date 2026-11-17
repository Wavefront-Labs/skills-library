---
id: computing-software.data-engineering.dbt.meta-owner-and-tag-conventions
name: meta-owner-and-tag-conventions
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-meta, model-owner, dbt-tags, governance-metadata, pii-tagging, tiering, dbt-project-evaluator, alert-routing]
level: practitioner
status: docs-checked
description: "Standardise dbt metadata: meta keys for owner/tier/PII/SLA, tags for scheduling and selection, enforcing them in CI, and consuming meta in alerting and catalogs."
sources:
  - https://docs.getdbt.com/reference/resource-configs/meta
  - https://docs.getdbt.com/reference/resource-configs/tags
  - https://github.com/dbt-labs/dbt-project-evaluator
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# meta, owner and tag conventions

**Goal:** every model carries machine-readable ownership and classification, used by alerting, catalogs and access control.

## Tags vs meta
- **tags**: for **selection** (`-s tag:nightly`), scheduling groups, and simple classification. Use them for selection and grouping.
- **meta**: for **metadata** (owner, tier, PII, SLA), arbitrary keys/values; read by tools via manifest.

## Convention example
```yaml
# dbt_project.yml (defaults by folder)
models:
  acme:
    marts:
      finance:
        +meta: {owner: "finance-analytics", slack: "#finance-data", tier: 1}
        +tags: ["finance", "nightly"]
```
```yaml
# per model/column
models:
  - name: dim_customers
    config:
      meta: {owner: "crm-data", tier: 1, sla_hours: 6, contains_pii: true}
    columns:
      - name: email
        meta: {pii: "email", masking: "hash"}
        tags: ["pii"]
```
Document the allowed keys/values (a short CONTRIBUTING section); free-form meta drifts.

## Enforce in CI
- `dbt-project-evaluator` package: rules for missing descriptions, tests, model naming, and custom checks.
- A small script over `target/manifest.json` that fails when a mart model has no `meta.owner` (check the manifest schema for the exact field paths).

## Consume
- Tools that read `meta` from the manifest can use it for alert routing, masking decisions and catalog display.

## Verify
- [ ] CI fails when a new mart lacks `meta.owner`.
- [ ] A failing tier-1 model alert reaches the owner's channel.

## Checked

2026-10-28. Confirmed against: meta and tags config pages (+meta in dbt_project.yml, meta in YAML config, column meta), dbt-project-evaluator README. Removed (not confirmable in the fetched pages): tag-merge claim, manifest script field paths, named alerting and catalog integrations, masking-policy automation.

Method: documentation only; no commands were run.
