---
id: computing-software.firmware-embedded-development.iot-protocols.coap-observe-notifications
name: coap-observe-notifications
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [coap-observe-notifications, coap-observe, coap, notification, max-age, iot-protocols]
level: practitioner
status: docs-checked
description: "CoAP observe notifications: Handle notification ordering and freshness."
sources:
  - https://www.rfc-editor.org/rfc/rfc7641
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CoAP observe notifications

**Goal:** Handle notification ordering and freshness.

## Steps
1. Observe option holds a 24-bit sequence value; client compares with the last using the wrap-around rule in RFC 7641 section 3.4
2. Max-Age tells how long the representation is fresh; after it expires the client must not assume the state is current and may re-register with a new GET using the same token
3. A server that sends notifications mostly as NON must send one as CON at least every 24 hours, so clients that went away drop out of the observer list
4. RFC 7641 sets congestion-control rules for notifications (including NSTART); follow them
5. A Reset sent in reply to a notification removes the observer

## Gotcha
Reordered UDP notifications can overwrite new state with old unless you apply the sequence comparison.

## Verify
- [ ] Out-of-order test keeps newest
- [ ] Max-Age expiry triggers refresh
- [ ] RST removes observer

## Checked

2026-11-03. Confirmed in RFC 7641: 24-bit Observe value and the wrap-around comparison (section 3.4), Max-Age freshness and re-registration, 24-hour confirmable rule, Reset removes the observer. Reworded steps 2-5 to the RFC wording.
Method: documentation only; no commands were run.
