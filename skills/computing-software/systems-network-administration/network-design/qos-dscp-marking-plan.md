---
id: computing-software.systems-network-administration.network-design.qos-dscp-marking-plan
name: qos-dscp-marking-plan
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, qos-design, dscp-plan, rfc4594, voice-requirements, video-requirements, wmm, wireless-qos, diffserv, ef, af41, cs6, scavenger, provider-class-mapping, end-to-end-qos, provider-qos-classes]
level: practitioner
status: gated
description: "Write an enterprise QoS policy: application classes and DSCP per RFC 4594, voice/video latency-jitter-loss budgets, mapping to WAN provider classes and Wi-Fi WMM access categories."
sources:
  - https://datatracker.ietf.org/doc/html/rfc4594
  - https://datatracker.ietf.org/doc/html/rfc8325
  - https://www.cisco.com/c/en/us/td/docs/solutions/Enterprise/WAN_and_MAN/QoS_SRND/QoS-SRND-Book/QoSIntro.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# QoS DSCP marking plan

## Targets that drive the design (one-way)
| Traffic | Latency | Jitter | Loss |
|---|---|---|---|
| Voice | <= 150 ms | <= 30 ms | <= 1% (gated: unconfirmed, source is paywalled or blocked) |
| Interactive video | <= 150-200 ms | <= 30-50 ms | <= 0.1-1% |
| Streaming video | 4-5 s (buffered) | n/a | <= 2% |
| Data | elastic | n/a | TCP recovers |

The targets above are the widely quoted Cisco/ITU-T G.114 figures; the sources are paywalled or blocked here, so confirm them in current vendor guidance.

## Class plan (RFC 4594-based, 8 classes is common)
RFC 4594 itself marks IP telephony signalling CS5 (40), broadcast video CS3 (24), real-time interactive CS4 (32), OAM CS2 and low-priority CS1; marking call signalling CS3 as below is a common vendor convention that departs from RFC 4594. All codepoint values were recomputed (AF class x 8 + drop x 2, CS n = 8n, EF = 46).
| Class | DSCP | Queueing |
|---|---|---|
| Network control (routing) | CS6 (48) | small guaranteed |
| Voice | EF (46) | strict priority (LLQ), capped so it cannot starve other classes |
| Interactive video / conferencing | AF41 (34) | guaranteed bandwidth, low drop |
| Call signalling | CS3 (24) here; RFC 4594 says CS5 (40) | small guaranteed |
| Network management (SSH, SNMP) | CS2 (16) | small guaranteed |
| Transactional / critical data | AF21 (18) | guaranteed, WRED |
| Bulk data (backup, sync) | AF11 (10) | guaranteed low, WRED |
| Scavenger (non-business) | CS1 (8) | minimal |
| Best effort | DF (0) | remainder, fair queue |
Fewer classes is fine (4-class model: realtime, control, critical data, best effort). Document
which applications map to each class and who marks them (endpoint, switch, NBAR).

## WAN provider mapping
MPLS carriers offer a few classes with their own DSCP expectations (take the count from your contract); build a table from your 8
classes to their classes and re-mark at the CE if they require it (e.g. AF41 -> AF31 for their
"video" class). Internet links do not honour DSCP; QoS only applies to your egress shaper.

## Wi-Fi (RFC 8325)
WMM has four access categories: Voice (AC_VO), Video (AC_VI), Best Effort (AC_BE), Background
(AC_BK). Per RFC 8325: EF -> AC_VO (UP 6), CS5/AF41/CS4/CS3 -> AC_VI, DF and AF11 -> AC_BE (UP 0), CS1 -> AC_BK (UP 1). Note AF11 is best effort, not background. Configure your controller's RFC 8325-style DSCP map (vendor-specific) and trust DSCP upstream.

## Verify
- [ ] Policy document: class table, application mapping, marking points, per-link queue allocations.
- [ ] Packet captures at the WAN edge show expected DSCPs per application.
- [ ] Voice MOS/latency measured under congestion within the targets.
