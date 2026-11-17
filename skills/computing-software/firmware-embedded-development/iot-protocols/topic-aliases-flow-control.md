---
id: computing-software.firmware-embedded-development.iot-protocols.topic-aliases-flow-control
name: topic-aliases-flow-control
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [topic-aliases-flow-control, mqtt5-features, mqtt5, topic-alias, receive-maximum, iot-protocols]
level: practitioner
status: docs-checked
description: "MQTT 5 topic aliases and flow control: Cut bytes and cap inflight load on constrained links."
sources:
  - https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MQTT 5 topic aliases and flow control

**Goal:** Cut bytes and cap inflight load on constrained links.

## Steps
1. Topic Alias Maximum in CONNECT/CONNACK sets how many aliases each side accepts
2. First publish carries topic plus Topic Alias N; later ones send empty topic with alias N
3. Aliases are per connection and not kept across reconnects
4. Receive Maximum (default 65535) limits unacked QoS 1/2 the peer may send
5. Maximum Packet Size lets a client refuse large packets

## Gotcha
Alias mappings last only for one network connection and a receiver must not carry them over to the next; reset the alias table on every connect and send the full topic with the alias first.

## Verify
- [ ] Capture shows zero-length topics after the first
- [ ] Inflight never above Receive Maximum

## Checked

2026-11-03. Confirmed in the OASIS MQTT 5.0 specification: Topic Alias Maximum (default 0), alias set with a topic name then reused with a zero-length topic, mappings not carried across connections, Receive Maximum default 65,535, Maximum Packet Size. Replaced the protocol-error claim with the stated rule.
Method: documentation only; no commands were run.
