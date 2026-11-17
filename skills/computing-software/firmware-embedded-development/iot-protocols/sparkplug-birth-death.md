---
id: computing-software.firmware-embedded-development.iot-protocols.sparkplug-birth-death
name: sparkplug-birth-death
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [sparkplug-birth-death, sparkplug, nbirth, ndeath, bdseq, rebirth, iot-protocols]
level: practitioner
status: docs-checked
description: "Sparkplug birth and death certificates: Manage state with birth and death messages."
sources:
  - https://sparkplug.eclipse.org/specification/
  - https://github.com/eclipse-sparkplug/sparkplug/tree/master/specification/src/main/asciidoc/chapters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sparkplug birth and death certificates

**Goal:** Manage state with birth and death messages.

## Steps
1. The edge node sets an MQTT Will of topic `spBv1.0/<group_id>/NDEATH/<edge_node_id>` with QoS 1, retain false, and a Sparkplug protobuf payload holding one metric, `bdSeq`
2. bdSeq starts at 0 and increases by one on every new MQTT CONNECT
3. After connecting it publishes NBIRTH (QoS 0, retain false) with all metrics, `seq` 0, a timestamp, a `bdSeq` metric equal to the one in the Will, and a `Node Control/Rebirth` metric
4. Devices publish DBIRTH (QoS 0, retain false) after NBIRTH
5. `seq` is one greater than the previous message on NDATA, DBIRTH, DDATA and so on, and wraps from 255 to 0; NDEATH carries no seq
6. If a host sees an out-of-order seq it starts a timer, and if the missing message does not arrive it sends an NCMD with `Node Control/Rebirth`
7. Metrics may use an optional alias (unsigned 64-bit) tied to the name on birth to cut payload size
8. DDEATH marks a device offline and NDEATH marks the node offline

## Gotcha
A host application ignores an NDEATH whose bdSeq does not match the bdSeq of the latest NBIRTH, since a late Will can arrive after the node has already reconnected. A bdSeq mismatch between Will and NBIRTH therefore makes a real death look stale.

## Verify
- [ ] Killing the edge node produces NDEATH
- [ ] Rebirth command makes the node resend all metrics
- [ ] seq wraps from 255 to 0

## Checked

2026-11-03. Confirmed in the Eclipse Sparkplug specification source (Topics, Operational Behavior and Payloads chapters): Will topic, QoS 1 and retain false, bdSeq rules and matching, NBIRTH seq 0 and Node Control/Rebirth, QoS 0 and retain false for births and data, seq wrap at 255, NDEATH without seq, rebirth request after out-of-order timeout, and metric alias description. Nothing else removed.
Method: documentation only; no commands were run.
