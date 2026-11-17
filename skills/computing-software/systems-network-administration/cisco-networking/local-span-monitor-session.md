---
id: computing-software.systems-network-administration.cisco-networking.local-span-monitor-session
name: local-span-monitor-session
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, local-span, monitor-session, port-mirroring, span, packet-capture]
level: practitioner
status: docs-checked
description: "Mirror switch ports or VLANs to a local analyser port with a Catalyst 9300 SPAN monitor session: source direction, VLAN filter, encapsulation, destination rules and limits."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/nmgmt/b_179_nmgmt_9300_cg/configuring_span_and_rspan.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Local SPAN (monitor session)

Scope: Catalyst 9300 IOS XE 17.9 configuration guide (Configuring SPAN and RSPAN).

```
no monitor session 1
monitor session 1 source interface gigabitethernet1/0/10 both
monitor session 1 filter vlan 20                      ! only when the source is a trunk
monitor session 1 destination interface gigabitethernet1/0/48 encapsulation replicate
```
- Direction is `both | rx | tx`; `both` is the default when none is given.
- Sources can be ports, port-channels or VLANs, but a session cannot mix source ports and source VLANs; a series of
  `source` commands can add several of the same kind. A session also cannot mix source VLANs and filter VLANs.
- `filter vlan` limits which VLANs of a monitored trunk are mirrored (all VLANs by default);
  `no monitor session N filter` goes back to all VLANs.
- `encapsulation replicate` sends the copy with the source's original headers (untagged, ISL or 802.1Q); without it
  packets leave in native (untagged) form.
- The destination must be a physical port (not an EtherChannel or VLAN), cannot be a source port, and cannot be the
  destination of two sessions. It stops being a normal port: only monitored traffic passes through it. The optional
  `ingress {dot1q vlan N | untagged vlan N | vlan N}` keyword lets the destination accept incoming traffic.
- Local SPAN uses the same session number for source and destination; a session does not start until the
  destination and at least one source are enabled.
- Limits: 66 sessions per device, of which at most 8 can be source sessions (local SPAN or RSPAN source); up to 64
  destination ports per stack.

## Capturing safely
- Each monitored packet is sent twice (normal and mirrored); an oversubscribed destination (the guide's example is a
  10 Mb/s port monitoring a 100 Mb/s port) drops packets.
- Entering SPAN commands does not remove earlier parameters: use `no monitor session N` (or `all | local | remote`)
  first, and again when the capture is done.
- Traffic routed into a source VLAN is not mirrored; traffic received on the source VLAN and routed out is.

## Check
`show monitor` displays the current SPAN, RSPAN, FSPAN or FRSPAN configuration.

## Checked
Date: 2026-11-08
Method: documentation only; no commands were run. Read the Catalyst 9300 17.9 "Configuring SPAN and RSPAN" chapter:
Restrictions, SPAN Configuration Guidelines, the local SPAN, trunk VLAN filter and monitoring tables and the local
SPAN example (sections read directly; the rest not needed for this skill). Corrected: the old example mixed a source
interface and a source VLAN in one session, which the guide forbids; session limit is 66 with 8 source sessions, not
"8 local/RSPAN sessions". Removed as unconfirmed: STP not running on the destination, editcap/tshark steps,
"do not use an uplink", `show monitor session 1 detail` and `show interfaces ... counters` checks (the guide lists
`show monitor`).
