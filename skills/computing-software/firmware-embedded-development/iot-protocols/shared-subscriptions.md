---
id: computing-software.firmware-embedded-development.iot-protocols.shared-subscriptions
name: shared-subscriptions
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [shared-subscriptions, mqtt5-features, mqtt5, shared-subscription, load-balancing, iot-protocols]
level: practitioner
status: docs-checked
description: "MQTT shared subscriptions: Load-balance messages across consumers."
sources:
  - https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MQTT shared subscriptions

**Goal:** Load-balance messages across consumers.

## Steps
1. Subscribe to $share/<group>/<filter>, e.g. $share/workers/sensors/+/data
2. Broker delivers each message to one member of the group
3. The ShareName must be at least one character and cannot contain / + #
4. Retained messages are not sent to a shared subscription
5. Shared subscriptions are an MQTT 5 feature; check your broker's documentation for support

## Gotcha
The server chooses the receiving session message by message; if a consumer disconnects with an unacknowledged QoS 1 message, the server may wait for it or send the message to another member of the group.

## Verify
- [ ] N consumers each receive about 1/N
- [ ] Killing one rebalances
- [ ] Handlers idempotent

## Checked

2026-11-03. Confirmed in the OASIS MQTT 5.0 specification section 4.8.2: $share/{ShareName}/{filter}, one session receives each message, ShareName rules, no retained messages to shared subscribers, QoS 1 redelivery wording. Removed: the list of brokers supporting it and the EMQX $queue/ mention (not in the specification).
Method: documentation only; no commands were run.
