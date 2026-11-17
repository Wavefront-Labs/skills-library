---
id: computing-software.data-engineering.data-quality.enforcing-data-contracts
name: enforcing-data-contracts
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, data-contracts, contract-enforcement, schema-registry, dbt-model-contracts, ci-gates, runtime-validation, breaking-changes, producer-ownership]
level: advanced
status: gated
description: "Enforce data contracts at every point: producer CI with breaking-change checks, schema registry compatibility, dbt model contracts, runtime validation with quarantine, and consumer alerts."
sources:
  - https://docs.getdbt.com/docs/collaborate/govern/model-contracts
  - https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html
  - https://cli.datacontract.com/
  - https://docs.confluent.io/cloud/current/sr/fundamentals/data-contracts.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enforcing data contracts

**Goal:** contracts that actually stop breaking changes and bad data, rather than YAML that drifts from reality.

## 1. Enforcement points
| Where | What it catches | Mechanism |
|---|---|---|
| Producer CI (design time) | breaking schema/semantic changes before merge | `datacontract breaking`, schema registry compatibility check, dbt contract + `state:modified` checks |
| Write time (runtime) | data that violates schema/rules as it's produced | schema registry serializers, registry data-quality rules, dbt contracts (DDL constraints), table constraints |
| After load (runtime) | quality rules, SLAs | `datacontract test`, dbt tests, DQ monitors |
| Consumer side | unexpected changes that slipped through | consumer-side tests/monitors on what they rely on |

## 2. Producer CI
```bash
# in the producer repo's PR pipeline
git show origin/main:contracts/orders.yaml > /tmp/orders_main.yaml
datacontract breaking /tmp/orders_main.yaml contracts/orders.yaml     # exit code 1 when a property is removed (tested, v1.2.7); it compares schema, not version numbers
datacontract lint contracts/orders.yaml
```
- Kafka: register schemas with compatibility `BACKWARD` (or `FULL`) per subject; CI calls the registry compatibility endpoint (`POST /compatibility/subjects/<subject>/versions/latest`, listed in the Confluent Schema Registry API reference) before deploy; producers use `auto.register.schemas=false` in prod (gated: unconfirmed, setting name not re-fetched) so only CI registers.
- Breaking change = new major version (new topic/table or versioned model) + deprecation window + consumer notification — not an edit in place.

## 3. dbt model contracts
```yaml
models:
  - name: orders
    config:
      contract: {enforced: true}
    columns:
      - {name: order_id, data_type: bigint, constraints: [{type: not_null}, {type: primary_key}]}   # constraints need a table/incremental model (dbt warns they are unsupported on views)
      - {name: amount, data_type: "decimal(18,2)"}
    versions:
      - v: 2
      - v: 1
        deprecation_date: 2026-12-31
```
With `contract.enforced`, the build fails if the model's columns/types don't match (tested on dbt 1.12.6: double vs declared decimal(18,2) is a compilation error); dbt flags breaking changes to contracted models in `state:modified` comparisons (gated: unconfirmed, not run). Versioned models with `deprecation_date` parsed and built. Model versions + `deprecation_date` give consumers a migration window.

## 4. Runtime validation and quarantine
- Validate at ingestion against the contract (types, required fields, enums); rows failing go to a quarantine table/DLQ with the violated rule.
- Decide per contract: **block** (stop publish, alert producer) for critical breaks; **quarantine and continue** under a threshold for row-level issues.
- Confluent data contracts can attach rules (CEL conditions, migration rules) to schemas, enforced in serializers.

## 5. Make it social, not just technical
- Producer owns the contract and is paged for contract violations of their data.
- Consumers register in the contract (or catalog) so producers know whom a change affects.
- Contract changes reviewed like API changes; changelog published.

## Verify
- [ ] A PR removing a contracted column fails CI in the producer repo.
- [ ] A message with an incompatible schema is rejected by the registry in prod.
- [ ] Contract test results are visible to both producer and consumers.
