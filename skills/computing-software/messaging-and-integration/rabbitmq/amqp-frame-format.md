---
id: computing-software.messaging-and-integration.rabbitmq.amqp-frame-format
name: amqp-frame-format
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, amqp-frame-format, rmq-amqp-spec]
level: sme
status: docs-checked
description: "Read the AMQP 0-9-1 wire framing: protocol header, frame types (method, header, body, heartbeat) and frame-end byte."
sources:
  - https://www.rabbitmq.com/resources/specs/amqp0-9-1.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AMQP frame format

**Goal:** Debug at the wire level.

## Steps
1. Connections start with the header `AMQP 0 0 9 1`.
2. Frame: type (1 byte), channel (2), size (4), payload, frame-end 0xCE.
3. Types: method=1, content header=2, body=3, heartbeat=8 (the spec's grammar gives 8; its prose list says 4, so check against a capture).
4. A published message is a method frame followed by a content header frame and zero or more body frames; the maximum frame payload size is agreed during connection negotiation (Tune).
5. The header frame payload holds class-id, weight (unused, zero), a 64-bit body size and property flags.

## Failure modes
- A bad frame-end byte, unknown frame type or oversized frame is a fatal framing error; protocol errors raise a connection exception with a 5xx reply code (501 frame error, 503 command invalid or syntax error, 504 channel error, 505 unexpected frame).
- Heartbeat frames and connection-class frames must use channel 0; content frames must not.

## Verify
- Check that every frame you decode ends with 0xCE and that the heartbeat type value matches your broker.

## Checked

Protocol header, frame layout, frame types, frame-end value, content header layout and 5xx reply codes confirmed in the spec. The Wireshark verify step and the bare frame_max name were dropped as not in the spec.

Method: docs-checked 2026-11-09 against the AMQP 0-9-1 specification PDF from rabbitmq.com (sections 4.2.2 to 4.2.7 and the grammar appendix read via pdftotext).
