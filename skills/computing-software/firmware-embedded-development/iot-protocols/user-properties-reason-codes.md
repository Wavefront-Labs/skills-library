---
id: computing-software.firmware-embedded-development.iot-protocols.user-properties-reason-codes
name: user-properties-reason-codes
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [user-properties-reason-codes, mqtt5-features, mqtt5, user-property, reason-code, iot-protocols]
level: practitioner
status: docs-checked
description: "MQTT 5 properties and reason codes: Use v5 metadata for diagnostics and request/response."
sources:
  - https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MQTT 5 properties and reason codes

**Goal:** Use v5 metadata for diagnostics and request/response.

## Steps
1. Reason codes now appear in CONNACK, PUBACK, SUBACK, DISCONNECT (e.g. 0x87 not authorised, 0x97 quota exceeded)
2. Reason String is human-readable only
3. User Property is repeatable key/value pairs for app metadata
4. Request/response: set Response Topic and Correlation Data on the request
5. Content Type and Payload Format Indicator describe the payload
6. Request Problem Information controls diagnostics

## Gotcha
Properties add bytes to every packet; do not stuff large metadata on constrained links.

## Verify
- [ ] Server returns granular reason codes
- [ ] Responder replies on Response Topic with same correlation data

## Checked

2026-11-03. Confirmed in the OASIS MQTT 5.0 specification: reason codes 0x87 Not authorized and 0x97 Quota exceeded, Reason String for diagnostics, repeatable User Property, Response Topic and Correlation Data, Content Type, Payload Format Indicator, Request Problem Information (default 1). Nothing removed.
Method: documentation only; no commands were run.
