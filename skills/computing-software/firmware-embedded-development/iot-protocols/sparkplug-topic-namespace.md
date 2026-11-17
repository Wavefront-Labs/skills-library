---
id: computing-software.firmware-embedded-development.iot-protocols.sparkplug-topic-namespace
name: sparkplug-topic-namespace
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [sparkplug-topic-namespace, sparkplug, spb, topic-namespace, group-id, iot-protocols]
level: practitioner
status: docs-checked
description: "Sparkplug topic namespace: Use the Sparkplug B topic structure."
sources:
  - https://sparkplug.eclipse.org/specification/
  - https://github.com/eclipse-sparkplug/sparkplug/tree/master/specification/src/main/asciidoc/chapters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sparkplug topic namespace

**Goal:** Use the Sparkplug B topic structure.

## Steps
1. Format `spBv1.0/<group_id>/<message_type>/<edge_node_id>[/<device_id>]`; device_id is present only for device message types
2. Message types: NBIRTH, NDEATH, NDATA, NCMD, DBIRTH, DDEATH, DDATA, DCMD and STATE; device_id must not appear with NBIRTH, NDEATH, NDATA, NCMD or STATE
3. A Host Application publishes its STATE birth on `spBv1.0/STATE/<sparkplug_host_id>` with QoS 1 and retain true; its payload is JSON with an `online` key
4. Birth, death and data payloads are Sparkplug B protobuf with metrics (name, alias, datatype, timestamp, value)
5. NBIRTH, NDATA, DBIRTH and DDATA are published with QoS 0 and retain false

## Gotcha
group_id, edge_node_id and device_id must be valid UTF-8 strings but must not contain `+`, `/` or `#`, which are reserved for MQTT topic syntax.

## Verify
- [ ] Host sees correct birth messages
- [ ] Topic validates against the grammar
- [ ] STATE retained

## Checked

2026-11-03. Confirmed in the Eclipse Sparkplug specification source (Principles, Topics and Payloads chapters): topic format and namespace spBv1.0, message types, device_id rule, reserved characters, STATE topic, QoS 1 and retain true for the host birth, QoS 0 and retain false for births and data, protobuf payload, the `online` JSON key. Removed: the Eclipse Tahu reference-implementation claim and the "confirm per spec version" hedge on QoS.
Method: documentation only; no commands were run.
