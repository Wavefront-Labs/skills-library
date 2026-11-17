---
id: computing-software.firmware-embedded-development.iot-protocols.coap-observe-registration
name: coap-observe-registration
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [coap-observe-registration, coap-observe, coap, observe, rfc7641, iot-protocols]
level: practitioner
status: docs-checked
description: "CoAP observe registration: Subscribe to a resource with CoAP Observe."
sources:
  - https://www.rfc-editor.org/rfc/rfc7641
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CoAP observe registration

**Goal:** Subscribe to a resource with CoAP Observe.

## Steps
1. Send GET with Observe option = 0 (register) and a token
2. Server answers 2.05 with an Observe value (sequence number) and keeps sending notifications with the same token
3. Deregister with Observe = 1 or an RST on a notification
4. Resources can advertise the obs attribute in link-format as a hint that they are observable

## Gotcha
The token identifies the observation: use a distinct token per observation and keep it until you cancel; a new GET with the same token re-registers.

## Verify
- [ ] Registration returns Observe option
- [ ] Cancel stops notifications
- [ ] obs attribute in /.well-known/core

## Checked

2026-11-03. Confirmed in RFC 7641: Observe 0 registers, Observe 1 deregisters, Reset removes the entry, notifications reuse the token, obs link attribute is a hint. Removed: the claims that resources must advertise obs and that servers limit observers.
Method: documentation only; no commands were run.
