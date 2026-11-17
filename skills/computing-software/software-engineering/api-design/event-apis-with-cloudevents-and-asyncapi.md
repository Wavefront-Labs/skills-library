---
id: computing-software.software-engineering.api-design.event-apis-with-cloudevents-and-asyncapi
name: event-apis-with-cloudevents-and-asyncapi
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, cloudevents, asyncapi, event-driven-api, event-schema, message-contracts]
level: advanced
status: docs-checked
description: "Design and document event-driven APIs: CloudEvents envelopes, AsyncAPI documents for channels and payloads, schema evolution and consumer guarantees."
sources: ["https://cloudevents.io/", "https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md", "https://www.asyncapi.com/docs/reference/specification/v3.0.0"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event APIs with CloudEvents and AsyncAPI

## CloudEvents envelope
Required attributes: `id`, `source`, `specversion` and `type`. Optional attributes include
`datacontenttype`, `dataschema`, `subject` and `time`; `data` carries the payload in the media
format named by `datacontenttype`. The spec says `type` SHOULD be prefixed with a reverse-DNS name,
so version it in the name, e.g. `com.example.order.shipped.v1`.
```json
{"specversion":"1.0","id":"evt-1","source":"/orders-service","type":"com.example.order.shipped.v1",
 "subject":"orders/o1","datacontenttype":"application/json",
 "data":{"order_id":"o1"}}
```
Producers MUST ensure `source` + `id` is unique per distinct event; a re-sent duplicate MAY reuse
the same `id`, and consumers MAY treat events with identical `source` and `id` as duplicates, so that
pair is the dedupe key. Events travel over many protocols (HTTP, AMQP, MQTT, Kafka, NATS and others)
through protocol bindings.

## AsyncAPI document
AsyncAPI describes message-driven APIs in a machine-readable format and is protocol-agnostic. In
v3.0.0 an operation has an `action` of `send` or `receive` and references a channel:
```yaml
asyncapi: 3.0.0
info: {title: Orders events, version: 1.0.0}
channels:
  orderShipped:
    address: orders.shipped
operations:
  publishShipped: {action: send, channel: {$ref: '#/channels/orderShipped'}}
```
The spec advises against deriving a receiver document from a sender one (or vice versa): the
channel one app receives on need not be the one another sends to.

## Contract rules
- State delivery semantics: at-least-once (consumers idempotent on `source` + `id`), ordering scope
  (per `subject` or partition key only), retention/replay window.
- Payload: event-carried state transfer (full snapshot) vs notification + fetch. Snapshots reduce
  callbacks but leak more data; choose per event.
- Evolution: additive fields only within a version; a breaking change is a new `type` (`.v2`)
  published in parallel for a migration window.
- Never put secrets or full PII in events; they get copied to many systems.

## Checked

Date: 2026-11-01. Confirmed against the CloudEvents core spec (required attributes, reverse-DNS
type, source + id uniqueness, protocol list) and the AsyncAPI 3.0.0 specification (protocol-agnostic,
`action` send/receive). Removed the HTTP header naming, schema registry products, generator
and validator commands and per-binding claims, which the cited pages do not state.
Method: documentation only; no commands were run.
