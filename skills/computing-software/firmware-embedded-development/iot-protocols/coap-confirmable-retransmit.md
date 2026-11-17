---
id: computing-software.firmware-embedded-development.iot-protocols.coap-confirmable-retransmit
name: coap-confirmable-retransmit
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [coap-confirmable-retransmit, coap-messages, coap, confirmable, ack-timeout, iot-protocols]
level: practitioner
status: docs-checked
description: "CoAP confirmable retransmission: Get reliability over UDP with correct timers."
sources:
  - https://www.rfc-editor.org/rfc/rfc7252
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CoAP confirmable retransmission

**Goal:** Get reliability over UDP with correct timers.

## Steps
1. CON message retransmits until ACK or RST
2. ACK_TIMEOUT 2 s, ACK_RANDOM_FACTOR 1.5, so first timeout is random in 2-3 s
3. MAX_RETRANSMIT 4, doubling the interval each time
4. Last retransmission happens within MAX_TRANSMIT_SPAN 45 s; the sender gives up after MAX_TRANSMIT_WAIT 93 s
5. NSTART 1 limits outstanding interactions per peer
6. Piggybacked response: ACK carries the answer; separate response: empty ACK then a later CON/NON
7. Duplicate CON must get the same ACK

## Gotcha
Aggressive retries on a congested LPWAN link make loss worse; follow the exponential backoff and NSTART.

## Verify
- [ ] Packet loss test retransmits at doubling intervals
- [ ] Duplicate suppressed by Message ID
- [ ] Response matched by token

## Checked

2026-11-03. Confirmed in RFC 7252: ACK_TIMEOUT 2 seconds, ACK_RANDOM_FACTOR 1.5, MAX_RETRANSMIT 4, NSTART 1, MAX_TRANSMIT_SPAN 45 s, MAX_TRANSMIT_WAIT 93 s. Nothing removed.
Method: documentation only; no commands were run.
