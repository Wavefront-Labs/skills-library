---
id: computing-software.messaging-and-integration.rabbitmq.headers-exchange
name: headers-exchange
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, headers-exchange]
level: practitioner
status: docs-checked
description: "Route on message header values with x-match all or any instead of the routing key."
sources:
  - https://www.rabbitmq.com/tutorials/amqp-concepts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Headers exchange

**Goal:** Route on several attributes without encoding them in a key.

## Steps
1. Bind with arguments, for example `{"x-match":"all","format":"pdf","type":"report"}`.
2. `x-match` `all` requires every header to match; `any` requires one. `any-with-x` and `all-with-x` also use headers that start with `x-` for matching.
3. For `any` and `all`, headers beginning with `x-` are not used to evaluate matches.

## Failure modes
- Headers starting with `x-` are silently ignored in `any` and `all` mode; use the `-with-x` variants to match on them.

## Verify
- Publish with headers format=pdf,type=report and check the target queue count.

## Checked

Date: 2026-11-02. Confirmed in the AMQP 0-9-1 concepts tutorial (headers exchange section): `x-match` values and `x-` header handling. Removed as not stated there: header type mismatch and performance claims.

Method: documentation only; no commands were run.
