---
id: computing-software.firmware-embedded-development.iot-protocols.topic-filters-wildcards
name: topic-filters-wildcards
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [topic-filters-wildcards, mqtt-topics, mqtt, wildcard, topic-filter, iot-protocols]
level: practitioner
status: docs-checked
description: "MQTT topic filters and wildcards: Write correct subscription filters."
sources:
  - https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html
  - https://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MQTT topic filters and wildcards

**Goal:** Write correct subscription filters.

## Steps
1. "/" separates levels; "+" matches exactly one level; "#" matches any remainder and must be last
2. sensors/+/temp matches sensors/a/temp not sensors/a/b/temp
3. "sensors/#" also matches "sensors" itself
4. Topics starting with "$" (like $SYS) are not matched by a leading + or #
5. Topic names cannot contain wildcards; max length 65535 bytes
6. Topics are case sensitive; a leading slash creates an empty first level

## Gotcha
Subscribing to "#" on a busy broker floods the client; use narrow filters.

## Verify
- [ ] Test matrix of publishes against filters
- [ ] $SYS not delivered by "#"
- [ ] No wildcard in publish topic

## Checked

2026-11-03. Confirmed in the OASIS MQTT 3.1.1 specification (section 4.7) and the HiveMQ topics article: level separator, single-level and multi-level wildcards, parent level matched by #, $ topics not matched by a leading wildcard, 65535-byte limit, case sensitivity, empty level from a leading slash, advice against subscribing to #. Nothing removed.
Method: documentation only; no commands were run.
