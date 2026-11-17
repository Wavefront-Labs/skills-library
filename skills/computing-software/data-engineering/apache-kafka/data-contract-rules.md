---
id: computing-software.data-engineering.apache-kafka.data-contract-rules
name: data-contract-rules
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, schema-registry, schema-rules, data-contracts, cel, migration-rules, schema-metadata, field-encryption]
level: advanced
status: docs-checked
description: "Attach data contract rules and metadata to Schema Registry schemas: CEL validation rules, DLQ actions, JSONata migration rules across breaking versions, and tags."
sources:
  - https://docs.confluent.io/platform/current/schema-registry/fundamentals/data-contracts.html
  - https://docs.confluent.io/cloud/current/sr/fundamentals/data-contracts.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data contract rules and metadata (Schema Registry)

Confluent Schema Registry (Confluent Platform 7.4+ Enterprise, or Cloud with the Stream Governance Advanced package; rules execute in the client serializers) extends a schema with **metadata** and a **ruleSet**, turning it into a data contract.

## Metadata
```json
"metadata": {"properties": {"owner": "payments-team", "email": "payments@acme.example", "slo_freshness": "5m"},
             "tags": {"Order.card_number": ["PII"]}}
```
Used for ownership, discovery, and to target rules at tagged fields.

## Domain rules (validate or transform on write/read)
```json
"ruleSet": {"domainRules": [
  {"name": "positiveTotal", "kind": "CONDITION", "mode": "WRITE", "type": "CEL",
   "expr": "message.total > 0", "onFailure": "DLQ",
   "params": {"dlq.topic": "orders-invalid"}}
]}
```
- `CEL` (Common Expression Language) conditions run in the producer serializer: failure raises `SerializationException` (`onFailure: ERROR`, default), drops the record (`NONE`), or sends it to a DLQ.
- `CEL_FIELD` applies an expression to each field matching tags/types (e.g. mask PII on read).
- The non-Java clients (.NET, Go, Python, JavaScript) do not yet support the DLQ action.
- Register with `POST /subjects/orders-value/versions` including `metadata` and `ruleSet` alongside `schema`.

## Migration rules (breaking changes)
Allow an incompatible new version and translate between versions on read/write:
```json
"ruleSet": {"migrationRules": [
  {"name": "renameUpgrade", "kind": "TRANSFORM", "type": "JSONATA", "mode": "UPGRADE",
   "expr": "$merge([$sift($, function($v, $k) {$k != 'state'}), {'status': $.'state'}])"},
  {"name": "renameDowngrade", "kind": "TRANSFORM", "type": "JSONATA", "mode": "DOWNGRADE",
   "expr": "$merge([$sift($, function($v, $k) {$k != 'status'}), {'state': $.'status'}])"}]}
```
Pair with `compatibilityGroup` metadata (e.g. `"application.major.version": "2"`): compatibility is checked only within a group, so v2 can break v1 while consumers pinned with `use.latest.with.metadata=application.major.version=1` keep reading v1-shaped records.

## Requirements and caveats
- Rules execute in the clients: the `kafka-schema-rules` dependency must match the serializer version, and both must be 7.4 or above.
- Rules are not enforced broker-side; a producer without the serializer bypasses them.
- Keep CEL expressions cheap; they run per record.

## Verify
- [ ] Producing an invalid record lands in `orders-invalid` (or throws) in a test.
- [ ] A v1 consumer with the metadata pin reads v2-produced records correctly via DOWNGRADE.

## Checked
2026-11-01. Confirmed against Confluent's Data Contracts page: version and edition requirements, rule fields (type, mode, onFailure, ERROR default for failure), CEL and CEL_FIELD executors, `kafka-schema-rules`, DLQ client limits, `compatibilityGroup` and `application.major.version`. Removed: the ENCRYPT rule example and its claims, and the old-client behaviour claim, which were not confirmed. The JSONATA migration rule pattern matches the page's rename example.
Method: documentation only; no commands were run.
