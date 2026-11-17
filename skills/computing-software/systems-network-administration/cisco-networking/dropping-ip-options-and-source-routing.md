---
id: computing-software.systems-network-administration.cisco-networking.dropping-ip-options-and-source-routing
name: dropping-ip-options-and-source-routing
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, ip-source-route, ip-options, ip-options-drop, infrastructure-security, device-hardening, rfc7126]
level: practitioner
status: docs-checked
description: "Harden IOS routers against IP options abuse: no ip source-route, ip options drop/ignore, ACL option filtering, and RFC 7126 per-option advice."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/access-lists/13608-21.html
  - https://datatracker.ietf.org/doc/html/rfc7126
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dropping IP options and source routing

## Why
The Cisco hardening guide gives two concerns: packets with IP options must be process-switched (elevated CPU load),
and options can alter the path a packet takes, which can subvert security controls. IP source routing uses the Loose
Source Route and Record Route options together, or Strict Source Route with Record Route, so the sender picks the path.

## Global commands (Cisco Harden IOS Devices page)
```
ip options drop
no ip source-route
```
- `ip options {drop | ignore}` was added in Cisco IOS Software Releases 12.3(4)T, 12.0(22)S and 12.2(25)S. `drop`
  drops every received packet carrying IP options. `ignore` ignores the options on the local device, but downstream
  devices could still be affected, so the guide highly recommends `drop`.
- Some protocols, for example RSVP, legitimately use IP options; this command affects them.
- With IP Options Selective Drop enabled, `show ip traffic` shows dropped packets in the forced drop counter.
- `no ip source-route` disables source routing, which is enabled by default in all IOS releases. Use it when options
  are not completely disabled by Selective Drop.

## ACL alternative (named extended ACLs, 12.3(4)T and later)
RSVP, MPLS Traffic Engineering, IGMP versions 2 and 3, and other protocols that use IP options cannot work if their
packets are dropped. Where they are in use, filter with an ACL instead of Selective Drop; if none are, Selective Drop
is the preferred method. The feature works only with named extended ACLs.
```
ip access-list extended ACL-TRANSIT-IN
 deny ip any any option any-options
 permit ip any any
```
Or deny specific options: `eool` (0), `record-route` (7), `timestamp` (68), `lsr` (131), `ssr` (137), each as
`deny ip any any option <keyword>` before `permit ip any any`. Apply with `ip access-group ... in`.

## RFC 7126 advice per option
- End of Option List and No Operation: SHOULD NOT drop packets because they contain these.
- LSRR, SSRR, Record Route: SHOULD have an option-specific knob (drop, forward as if the option were absent, or
  process per RFC 791), with default "drop", and the default documented.
- Stream Identifier, Internet Timestamp, Probe MTU, Reply MTU: SHOULD drop packets containing them.
- Router Alert: allow only in controlled environments; SHOULD ignore it by default and offer a setting to honor,
  ignore or drop.
- Overall the RFC treats each option separately, so check the section for any option you plan to filter.

## Checked
Checked 2026-11-08 against the Cisco "Harden IOS Devices" page (sections on IP options, source routing
and ACL option filtering) and RFC 7126 section 4 (per-option advice). Removed: the `router-alert` ACL keyword,
IPv6 routing header remarks, `ip options` behaviour on IGMP/PIM/MLD, `ignore` platform support, `show running-config`
verification, and the extended-ping test, which the sources do not state. The Cisco ACL-options feature page cited
earlier returned 404 and was dropped.
Method: documentation only; no commands were run.
