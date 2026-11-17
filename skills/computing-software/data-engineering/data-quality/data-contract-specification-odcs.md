---
id: computing-software.data-engineering.data-quality.data-contract-specification-odcs
name: data-contract-specification-odcs
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, data-contracts, odcs, open-data-contract-standard, datacontract-cli, bitol, schema-definition, sla-properties, contract-testing]
level: practitioner
status: gated
description: "Write data contracts in the Open Data Contract Standard (ODCS) YAML and work with datacontract-cli: schema, quality rules, SLAs, ownership, linting, testing, exporting and breaking-change checks."
sources:
  - https://bitol-io.github.io/open-data-contract-standard/latest/
  - https://github.com/bitol-io/open-data-contract-standard
  - https://cli.datacontract.com/
  - https://github.com/datacontract/datacontract-cli
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data contract specification: ODCS and datacontract-cli

**Goal:** a machine-readable agreement between a data producer and its consumers — schema, semantics, quality and service levels — versioned in Git and testable.

## 1. ODCS document (v3 shape)
```yaml
apiVersion: v3.1.0
kind: DataContract
id: 0e5d1a6e-orders-contract
name: orders
version: 1.2.0
status: active
domain: sales
dataProduct: sales-orders
description:
  purpose: Confirmed customer orders for revenue reporting and fulfilment analytics.
  limitations: Excludes test orders and B2B marketplace orders.
schema:
  - name: orders
    physicalName: gold.sales.orders
    logicalType: object
    properties:
      - {name: order_id, logicalType: integer, physicalType: BIGINT, primaryKey: true, required: true, unique: true}
      - {name: customer_id, logicalType: integer, required: true}
      - name: amount
        logicalType: number
        physicalType: DECIMAL(18,2)
        required: true
        quality:
          - {metric: nullValues, mustBe: 0}      # ODCS >= 3.1 library metric; there is no range metric, use a sql rule for ranges (v3.0.x called this field `rule`)
      - {name: email, logicalType: string, classification: restricted}
    quality:
      - type: sql
        description: no orders dated in the future
        query: SELECT COUNT(*) FROM gold.sales.orders WHERE order_date > CURRENT_DATE
        mustBe: 0
servers:
  - {server: prod, type: databricks, catalog: gold, schema: sales}
team:
  - {username: jdoe, role: owner}
support:
  - {channel: "#sales-data", url: https://chat.example.com/sales-data}
slaProperties:
  - {property: latency, value: 4, unit: h}
  - {property: retention, value: 3, unit: y}
```
Linted with datacontract-cli 1.2.7: valid against ODCS v3.1.0. The same file with `metric:` under `apiVersion: v3.0.2` fails (`'rule' is a required property`), so `metric` vs `rule` depends on the version. Library metrics in the ODCS data-quality doc include `rowCount`, `nullValues`, `missingValues`, `invalidValues` (arguments `validValues`/`pattern`) and `duplicateValues`. `datacontract init` writes v3.2.0 by default.

## 2. datacontract-cli
```bash
pip install 'datacontract-cli[all]'
datacontract init datacontract.yaml                           # starter (--template takes a URL, not a name like `odcs`)
datacontract lint datacontract.yaml                           # schema-valid contract?
datacontract test datacontract.yaml --server prod             # connects to the server, checks schema + quality rules
datacontract export dbt-models datacontract.yaml              # format is positional since v0.12.0 (`--format` is rejected); also: sql, avro, jsonschema, great-expectations, html ... (gated: unconfirmed, dbt-models raised `'list' object has no attribute 'name'` on the example contract in 1.2.7)
datacontract import sql --source ddl.sql                      # bootstrap from existing DDL (format is a subcommand)
datacontract breaking old.yaml new.yaml                       # breaking-change detection (exit code 1 when a property was removed; tested)
datacontract changelog old.yaml new.yaml
```
Credentials come from environment variables per server type (e.g. `DATACONTRACT_DATABRICKS_TOKEN`) (gated: unconfirmed, `datacontract test` needs a live server and was not run).

## 3. Writing good contracts
- One contract per published dataset/output port, owned by the **producer**.
- Semantic descriptions per column (units, currency, time zone, nullable meaning).
- Quality rules that consumers actually rely on (keys, ranges, referential, freshness) — not every possible check.
- SLAs measurable from data: freshness/latency, availability, retention.
- Semantic versioning: patch = docs, minor = additive (new optional column), major = breaking (removed/renamed/type-narrowed column, tighter semantics). Major versions publish in parallel for a deprecation period.

## Verify
- [ ] `datacontract lint` passes in CI for every contract.
- [ ] `datacontract test` runs on schedule (or after each load) against prod.
- [ ] PRs changing a contract run `datacontract breaking` and require consumer sign-off on majors.
