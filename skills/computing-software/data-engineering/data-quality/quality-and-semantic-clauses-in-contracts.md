---
id: computing-software.data-engineering.data-quality.quality-and-semantic-clauses-in-contracts
name: quality-and-semantic-clauses-in-contracts
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, contract-quality-rules, data-contracts, odcs, semantics]
level: advanced
status: gated
description: "Write the quality and semantic sections of data contracts: field definitions, units, allowed values, quality rules with thresholds, SLAs, and making them executable."
sources:
  - https://bitol-io.github.io/open-data-contract-standard/latest/data-quality/
  - https://datacontract.com/
  - https://cli.datacontract.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quality and semantic clauses in contracts

**Goal:** contract clauses precise enough to be tested automatically and understood without asking the producer.

## Semantics per field
```yaml
# ODCS v3.1 style excerpt (linted with datacontract-cli 1.2.7 after the header fields apiVersion v3.1.0, kind, id, name, version, status were added)
schema:
  - name: orders
    physicalName: fct_orders
    properties:
      - name: order_id
        logicalType: string
        required: true
        unique: true
        primaryKey: true
        description: Order identifier from the shop system; stable for the order lifetime.
      - name: amount
        logicalType: number
        description: Order total incl. VAT, in the order currency, after discounts, before refunds.
        quality:
          - type: sql
            query: "SELECT count(*) FROM fct_orders WHERE amount < 0"
            mustBe: 0
      - name: currency
        logicalType: string
        description: ISO 4217 code.
        quality:
          - type: library
            metric: invalidValues          # v3.0.x spelled this `rule`
            arguments: {validValues: [EUR, USD, GBP]}
            mustBe: 0                      # a library rule without a mustBe* operator fails the schema
```
State units, currency, time zone, inclusion/exclusion rules (VAT, refunds, test orders), and the event a timestamp represents (created vs paid).

## Dataset-level quality
- Row count bounds or volume change limits.
- Freshness (max delay), completeness of key fields (`mustBeGreaterThan` thresholds as ratios).
- Referential integrity to other contracted datasets.
- Business invariants (sum of line amounts = order amount).

## SLA section
Freshness, availability, support/response times, retention, and where incidents are communicated.

## Make it executable
```bash
datacontract test datacontract.yaml          # runs schema and quality checks against the server defined in the contract
datacontract lint datacontract.yaml
datacontract export dbt-models datacontract.yaml   # positional format since v0.12.0 (`--format` is rejected); also great-expectations, sql, jsonschema, html (dbt-models raised an error on a multi-field contract in 1.2.7 (gated: unconfirmed, source is paywalled or blocked))
```
`datacontract test` needs a reachable server and was not run here (gated: unconfirmed, source is paywalled or blocked). Run in producer CI and on schedule in production; failures are contract breaches routed to the producer.

## Gotchas
- Vague descriptions ("the amount") make rules unverifiable and invite misinterpretation.
- Rules duplicated by hand in dbt tests drift from the contract: generate them from the contract.

## Verify
`datacontract test` passes in production; a reviewer outside the team can compute the metric correctly from descriptions alone.
