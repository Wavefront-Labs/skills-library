---
id: computing-software.firmware-embedded-development.iot-protocols.session-expiry-v5
name: session-expiry-v5
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [session-expiry-v5, mqtt-sessions, mqtt5, clean-start, session-expiry-interval, iot-protocols]
level: practitioner
status: docs-checked
description: "MQTT 5 session expiry: Bound server state with MQTT 5 expiry controls."
sources:
  - https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MQTT 5 session expiry

**Goal:** Bound server state with MQTT 5 expiry controls.

## Steps
1. Clean Start flag discards any existing session at connect
2. Session Expiry Interval (seconds, property 0x11) sets how long state survives after disconnect; 0 = end at close, 0xFFFFFFFF = never
3. DISCONNECT may change the interval (but not from 0)
4. Message Expiry Interval on PUBLISH drops stale queued messages and is decremented by the broker
5. Receive Maximum caps unacked QoS 1/2 inflight

## Gotcha
0xFFFFFFFF means the session never expires, as in 3.1.1; choose a finite interval that fits your offline pattern.

## Verify
- [ ] Session gone after interval
- [ ] Expired message not delivered
- [ ] Server enforces Receive Maximum

## Checked

2026-11-03. Confirmed in the OASIS MQTT 5.0 specification: Clean Start, Session Expiry Interval property 0x11 and 0xFFFFFFFF never expires, DISCONNECT may not set a non-zero interval if the CONNECT value was zero, Message Expiry Interval reduced by time waiting, Receive Maximum. Reworded the gotcha.
Method: documentation only; no commands were run.
