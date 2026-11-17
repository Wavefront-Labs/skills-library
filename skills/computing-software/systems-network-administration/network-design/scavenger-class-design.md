---
id: computing-software.systems-network-administration.network-design.scavenger-class-design
name: scavenger-class-design
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, qos-design, scavenger-class, lower-effort-phb, cs1, bulk-traffic]
level: practitioner
status: docs-checked
description: "Design a scavenger (less than best effort) QoS class: what traffic goes in, CS1 vs LE DSCP 1, minimal bandwidth guarantees, and identifying traffic with NBAR or app-ID."
sources:
  - https://www.rfc-editor.org/rfc/rfc8622
  - https://www.rfc-editor.org/rfc/rfc4594
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scavenger class design

## Purpose
Traffic that should only use bandwidth nobody else wants: it yields to best effort under congestion
and uses spare capacity otherwise.

## Candidates
Backups and replication (unless they have deadlines), OS/app update downloads, peer-to-peer,
recreational video/streaming, cloud sync bulk, gaming on guest networks, traffic flagged as
anomalous by security.

## Marking
- Historically **CS1 (DSCP 8)** per RFC 4594.
- **RFC 8622 Lower-Effort PHB: DSCP 1 (codepoint '000001')** is the recommended codepoint, and
  RFC 8622 says existing implementations should move from CS1 to it where possible. Map both to
  the scavenger queue while both are in use.

## Queueing
- Give it a small **minimum** rather than zero so flows are not starved forever (TCP timeouts,
  broken backups).
- No priority, no shaping to zero; use WRED/drop aggressively under congestion.
Configure the class with your platform's QoS syntax: match DSCP CS1 and 1, give a small minimum
bandwidth, and drop early under congestion (vendor syntax was not confirmed, so none is shown).

## Identification
Application recognition (NBAR2 or similar), firewall app-ID
marking, or endpoint/application marking (backup software DSCP settings, Windows QoS policies by
executable).

## Verify
- [ ] Under induced congestion, scavenger traffic drops first while best effort and priority classes keep throughput; scavenger flows never fully stall.

## Checked

- Date: 2026-10-28
- Confirmed: RFC 4594 lists CS1 (001000, DSCP 8) for Low-Priority Data; RFC 8622 recommends codepoint 000001 for LE and says implementations should transition from CS1.
- Removed: the 802.1p mapping remark, the 1 percent figure, Cisco class-map and NBAR syntax and the Cisco worm-containment history (Cisco QoS SRND link is dead), the Cisco source.

Method: documentation only; no commands were run.
