---
id: computing-software.systems-network-administration.cisco-networking.flow-based-span
name: flow-based-span
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, catalyst-9000, flow-based-span, fspan, span-filter, monitor-session-filter, traffic-mirroring]
level: practitioner
status: docs-checked
description: "Mirror only matching traffic with flow-based SPAN (FSPAN/FRSPAN) on Catalyst 9300: ACL filters on a monitor session, the unattached-ACL blocking rule, and ERSPAN filters."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/nmgmt/b_179_nmgmt_9300_cg/configuring_span_and_rspan.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/nmgmt/b_179_nmgmt_9300_cg/configuring_erspan.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flow-based SPAN (FSPAN)

Scope: Catalyst 9300 IOS XE 17.9 configuration guides (SPAN and RSPAN; ERSPAN).

## Why
A normal SPAN session copies everything on the source. Attaching an ACL to the session limits the copy to matching
traffic, which helps with an oversubscribed destination.

## Config (local SPAN)
```
no monitor session 2
monitor session 2 source interface gigabitethernet1/0/1
monitor session 2 destination interface gigabitethernet1/0/2 encapsulation replicate
monitor session 2 filter ip access-group SPAN-FILTER
```
`SPAN-FILTER` is an ACL you define. The syntax is
`monitor session N filter {ip | ipv6 | mac} access-group {access-list-number | name}`. For FRSPAN the same filter
command is added to an RSPAN source session (`destination remote vlan N` plus `remote-span` on that VLAN).

## Rules from the guide
- FSPAN is enabled as soon as at least one FSPAN ACL is attached to the session.
- If you attach a non-empty ACL of one type (for example IPv4) but none of the other types (IPv6, MAC), FSPAN
  blocks the traffic those unattached ACLs would have filtered, so that traffic is not monitored. Attach an
  ACL for each type you want mirrored.
- VLAN filtering is a different feature: `monitor session N filter vlan vlan-id [, | -]` limits which VLANs of a
  monitored trunk are mirrored. A session cannot mix source VLANs and filter VLANs.
- Session limits are the SPAN ones: 66 sessions per device, at most 8 source sessions.
- Destination port is dedicated to monitored traffic.

## ERSPAN
In an ERSPAN source session (`monitor session N type erspan-source`) the optional `filter` command takes
`ip access-group`, `ipv6 access-group`, `mac access-group`, `sgt` or `vlan`. IP/IPv6/MAC/VLAN access-group filters and
the SGT filter cannot be configured at the same time, and SGT filtering is not allowed on an existing FSPAN or
VLAN-filter session. The guide says the ACL is applied before the traffic is sent into the tunnel.

## Check
`show monitor` displays the current SPAN, RSPAN, FSPAN or FRSPAN configuration.

## Checked
Date: 2026-11-08
Method: documentation only; no commands were run. Read the Catalyst 9300 17.9 SPAN and RSPAN chapter: FSPAN and FRSPAN
Configuration Guidelines, Configuring an FSPAN Session and Configuring an FRSPAN Session (command forms), the trunk VLAN
filter step and the monitoring table. In the ERSPAN chapter I found the `filter` command and the notes on combined
filters by searching only (matching lines, not the chapter end to end). Removed as unconfirmed: TCAM exhaustion and "check logs", "only one ACL per address family", "some
platforms ingress only", the "2 local sessions on some models" and 9500/9600 figures, the VoIP port-range ACL, the
`show interfaces ... | i output drops` check and the claim that ERSPAN filtering is meant to cut WAN bandwidth.
