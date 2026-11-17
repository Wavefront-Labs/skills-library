---
id: computing-software.messaging-and-integration.rabbitmq.envelope-wrapper-and-enricher
name: envelope-wrapper-and-enricher
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, envelope-wrapper-and-enricher]
level: practitioner
status: docs-checked
description: "Wrap messages in a standard envelope of headers and enrich them from reference data."
sources:
  - https://www.enterpriseintegrationpatterns.com/patterns/messaging/
  - https://www.rabbitmq.com/docs/publishers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Envelope wrapper and content enricher

**Goal:** Standardise metadata.

## Steps
1. Use the standard AMQP 0-9-1 message properties where they exist: `message_id`, `correlation_id`, `type`, `timestamp`, `content_type`, `content_encoding`. Put anything else (schema version, trace id) in application headers.
2. An enricher consumes, adds fields from a lookup, and republishes to the next exchange.
3. Version the schema in a header or the `type` value.

## Failure modes
- Unversioned payload changes break consumers.

## Verify
- Validate envelope fields in a consumer test.

## Checked
2026-11-09. Envelope Wrapper and Content Enricher named on the EIP messaging index. The RabbitMQ Publishers page lists message id, correlation id, type, timestamp, content type, content encoding, headers and reply-to among the message properties. Removed: the "trace id" and "schema version" as named properties (they are not standard properties, so they now go in application headers) and the version note.
Method: documentation only; no commands were run.
