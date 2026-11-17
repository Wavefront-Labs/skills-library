---
id: computing-software.systems-network-administration.cisco-networking.erspan-gre-mirroring
name: erspan-gre-mirroring
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, erspan, port-mirroring, gre, span, packet-capture, catalyst-9300]
level: practitioner
status: docs-checked
description: "Mirror traffic across routed networks with ERSPAN on IOS-XE Catalyst 9300: source and destination sessions, erspan-id, origin IP, MTU truncation, header types, restrictions."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/nmgmt/b_179_nmgmt_9300_cg/configuring_erspan.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# ERSPAN

ERSPAN monitors traffic on ports or VLANs and sends it, in routable GRE-encapsulated form, to a destination session
(or an analyser) on another device. Source ports, source VLANs and destination ports can live on different devices.
Encapsulation and decapsulation happen in hardware, so CPU performance is not impacted. Type-II and Type-III headers
are supported, over IPv4 and IPv6. Checked against the Catalyst 9300 17.9 guide; other platforms differ, so read
their guide.

## Source session
```
monitor session 10 type erspan-source
 source interface Gi1/0/10 both
 filter vlan 20                     ! optional, only when the source is a trunk port
 destination
  erspan-id 10
  ip address 10.99.0.50             ! destination of the GRE envelope
  origin ip address 10.255.0.7      ! source of the GRE envelope
  mtu 1500
  exit
 no shutdown
```
- Session number range is 1 to 66; the number and session type cannot be changed afterwards (use `no monitor session`
  and recreate). Source and destination session IDs share one global ID space.
- Source: `source {interface ... | vlan ...} [, | - | both | rx | tx]`. A session has ports or VLANs as source, never
  both, and source VLANs and filter VLANs cannot be mixed in one session.
- Optional: `header-type 3` (default is Type-II), `ip dscp`, `ip ttl`, `vrf`, `description` (up to 240 characters,
  no special characters or spaces).
- `erspan-id` must also be entered in the destination session. `origin ip address` and `ip address` are the source
  and destination of the GRE envelope.
- `mtu`: any ERSPAN packet larger than the configured size is truncated to it. Range 176 to 9000 bytes, default
  9000. Setting 1500 therefore truncates mirrored large frames.
- By default ERSPAN monitors all traffic, including multicast and BPDU frames, and encapsulated packets up to 9180
  bytes are supported.

## Destination session (on the remote switch)
```
monitor session 11 type erspan-destination
 destination interface Gi1/0/48
 source
  erspan-id 10
  ip address 10.255.0.20
  exit
 no shutdown
```
The destination IP must be an address on a local or loopback interface and must match the address the source
session sends to. An ERSPAN destination interface can be in only one session. To avoid oversubscribing and dropping
management traffic on the destination device, configure and verify the destination session before the source
session.

## Restrictions worth knowing
- Disabling `ip routing` (IPv4) or `ipv6 unicast-routing` (IPv6) stops ERSPAN traffic flow.
- Source sessions do not copy ERSPAN GRE-encapsulated traffic, locally sourced RSPAN VLAN traffic, or DHCP-inject
  packets (DHCP packets modified by the CPU).
- Truncation works only for IPv4/IPv6 packets, not Layer 2 frames without an IP header.
- ERSPAN does not support QoS shaping and policing.
- Restoring a backup configuration recreates ERSPAN sessions in disabled state; enable them manually.
- Filter IP/IPv6/MAC/VLAN access-group and filter SGT cannot be configured together. Apply an ACL filter before the
  monitored traffic goes onto the tunnel.

## Verify
```
show monitor session 10
show monitor session erspan-source detail
show platform software monitor session 10
show capability feature monitor erspan-source
```
The detail output lists Destination IP Address, MTU, Destination ERSPAN ID, Origin IP Address, IP TTL and header
type. Confirm status Admin Enabled and that the analyser receives GRE from the origin IP.

## Checked
Checked 2026-11-08 against the Cisco Catalyst 9300 17.9 "Configuring ERSPAN" chapter (session limits, command
syntax, MTU range and default, restrictions, destination rules, verification commands). Removed: Wireshark display
filter, tcpdump capture line, "about 50 bytes" overhead figure, GRE protocol number, and ISR/ASR claims, none stated
on that page.
Method: documentation only; no commands were run.
