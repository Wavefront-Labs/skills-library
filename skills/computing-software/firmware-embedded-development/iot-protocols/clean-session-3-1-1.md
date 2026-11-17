---
id: computing-software.firmware-embedded-development.iot-protocols.clean-session-3-1-1
name: clean-session-3-1-1
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [clean-session-3-1-1, mqtt-sessions, mqtt, clean-session, persistent-session, iot-protocols]
level: practitioner
status: docs-checked
description: "MQTT 3.1.1 clean session: Decide between transient and persistent sessions in 3.1.1."
sources:
  - https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html
  - https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MQTT 3.1.1 clean session

**Goal:** Decide between transient and persistent sessions in 3.1.1.

## Steps
1. CleanSession=1 discards state at connect and disconnect
2. CleanSession=0 keeps subscriptions and queued QoS 1/2 messages for the ClientId while offline
3. CONNACK session-present tells the client if state survived; resubscribe if 0
4. 3.1.1 has no Session Expiry Interval (MQTT 5 adds one), so the protocol never ends a stored session on its own
5. Queue limits are broker-specific and not set by the spec; look up your broker's setting

## Gotcha
A persistent session with a long-gone ClientId keeps its state on the broker indefinitely; plan an operational sweep.

## Verify
- [ ] Reconnect with session-present 1 receives queued messages
- [ ] Queue limit configured
- [ ] Stale sessions pruned

## Checked

2026-11-03. Confirmed in the OASIS MQTT 3.1.1 specification: CleanSession discard rule, session state contents, Session Present in CONNACK, re-send of unacknowledged QoS 1/2 messages on reconnect with CleanSession=0, and the absence of any session expiry. Removed: Mosquitto max_queued_messages default and the broker-memory claim (not in the specification).
Method: documentation only; no commands were run.
