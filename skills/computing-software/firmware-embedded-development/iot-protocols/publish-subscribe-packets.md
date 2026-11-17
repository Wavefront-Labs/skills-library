---
id: computing-software.firmware-embedded-development.iot-protocols.publish-subscribe-packets
name: publish-subscribe-packets
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [publish-subscribe-packets, mqtt-packets, mqtt, publish, subscribe, suback, iot-protocols]
level: practitioner
status: docs-checked
description: "PUBLISH and SUBSCRIBE packets: Understand fixed header and packet identifiers so you can debug captures."
sources:
  - https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html
  - https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PUBLISH and SUBSCRIBE packets

**Goal:** Understand fixed header and packet identifiers so you can debug captures.

## Steps
1. Fixed header byte 1 high nibble is type (PUBLISH = 3, SUBSCRIBE = 8, requires flags 0b0010); remaining length uses 1-4 bytes of 7-bit varint, max 268435455
2. PUBLISH flags: DUP bit 3, QoS bits 2-1, RETAIN bit 0
3. Topic name is a 2-byte-length UTF-8 string; packet identifier (2 bytes, non-zero) only present when QoS above 0
4. SUBSCRIBE payload is topic filter plus requested QoS; SUBACK returns granted QoS per filter, 0x80 (3.1.1) means failure
5. v5 adds a property length varint before payload

## Gotcha
A packet identifier is a non-zero 16-bit value, so at most 65535 can be in flight; do not reuse one until its acknowledgement flow has completed.

## Verify
- [ ] A packet capture decodes with the fields above
- [ ] SUBACK has one return code per filter
- [ ] QoS 0 packets carry no identifier

## Checked

2026-11-03. Confirmed in the OASIS MQTT 3.1.1 and 5.0 specifications: packet type numbers, SUBSCRIBE reserved flags 0010, remaining-length encoding and maximum 268435455, PUBLISH flag bits, non-zero packet identifier, UTF-8 string length prefix, SUBACK return code 0x80, v5 property length. Removed: the Wireshark dissector check and the counter-wrap corruption claim.
Method: documentation only; no commands were run.
