---
id: computing-software.data-engineering.data-quality.producer-side-validation-at-the-source
name: producer-side-validation-at-the-source
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, producer-validation, shift-left, data-contracts, schema-validation]
level: advanced
status: gated
description: "Validate data at the producer before it leaves the source: schema checks in services, outbox events, contract tests in producer CI, and rejecting vs flagging bad records."
sources:
  - https://docs.pact.io/
  - https://json-schema.org/understanding-json-schema
  - https://microservices.io/patterns/data/transactional-outbox.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Producer-side validation at the source

**Goal:** the team that creates data stops bad records from being emitted, instead of every consumer cleaning them up.

## Where producers validate
- **Entry points**: forms and APIs validate formats, required fields, reference values (country/currency lists) at write time.
- **Database constraints**: NOT NULL, CHECK, FK, UNIQUE in the source DB: the cheapest permanent rule.
- **Event emission**: serialize with a schema (Avro/Protobuf/JSON Schema) registered in a registry; serializers reject invalid payloads.
```python
from jsonschema import validate
validate(instance=event, schema=ORDER_CREATED_V2)   # raises jsonschema.ValidationError before publish (tested: "'x' is not of type 'integer'")
producer.produce("orders.created", value=serializer(event))
```
- **Transactional outbox**: write the event to an outbox table in the same transaction as the business change, so events are never lost or emitted for rolled-back changes; a relay (Debezium outbox router) publishes them.

## Contract tests in producer CI
- Generate/validate sample events against the published schema and contract rules in the producer's test suite.
- Schema compatibility check against the registry (`BACKWARD`) as a CI step (compatibility endpoint listed in the Confluent Schema Registry API reference): breaking changes fail the producer build, not the consumer pipeline at 3 am.
- Consumer-driven contracts (Pact-style) for APIs consumed by data pipelines (gated: unconfirmed, source is paywalled or blocked). A Debezium Outbox Event Router transformation exists (Debezium reference page fetched); the relay itself was not run.

## Reject or flag
- Reject when the record is unusable (missing key, wrong type).
- Flag (`quality_flags` array) when usable but suspicious (out-of-range values), so consumers can filter.
- Never silently fix: auto-corrections hide upstream bugs.

## Make it a shared responsibility
Data contracts define rules jointly; producers own enforcement at emission; platform provides libraries/registry; consumers report violations back as producer tickets.

## Verify
Producer CI fails on a breaking schema change; a deliberately invalid event is rejected at publish time and never appears downstream.
