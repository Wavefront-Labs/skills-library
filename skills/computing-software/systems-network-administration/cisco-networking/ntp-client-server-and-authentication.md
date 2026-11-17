---
id: computing-software.systems-network-administration.cisco-networking.ntp-client-server-and-authentication
name: ntp-client-server-and-authentication
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, ntp, ntp-authentication, ntp-access-group, ntp-master, time-sync]
level: practitioner
status: docs-checked
description: "Configure NTP on Cisco IOS XE: server and peer associations, MD5 authentication keys, source interface, access groups, ntp master caveats and the show commands."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/bsm/configuration/xe-16/bsm-xe-16-book/bsm-time-calendar-set.html
  - https://www.cisco.com/c/en/us/support/docs/availability/high-availability/19643-ntpm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NTP client/server and authentication on IOS XE

Scope: IOS XE 16 "Setting Time and Calendar Services" configuration guide; document 19643 for NTP design context.

## Concepts (from the guide)
- Stratum counts NTP hops from an authoritative source. NTP will never synchronise to a machine that is not itself
  synchronised, and compares several machines, so it does not synchronise to one whose time differs significantly
  from the others even if its stratum is lower.
- The Cisco implementation does not support stratum 1 service (no radio or atomic clock; some platforms can take a
  GPS device). Cisco recommends deriving network time from public NTP servers on the Internet.
- Limit direct peer and client-server associations; too many simultaneous polls can hurt performance. Broadcast mode
  is suggested for modest accuracy needs on a local network with more than 20 clients (broadcast server and clients
  on the same subnet; `ntp broadcast` on the server interface, `ntp broadcast client` on clients).

## Client config
```
ntp authenticate
ntp authentication-key 1 md5 <NTP_KEY>
ntp trusted-key 1
ntp source Loopback0
ntp server 192.0.2.11 key 1 prefer
ntp server 192.0.2.12 key 1
```
- Syntax: `ntp server ip-address [version number] [key key-id] [prefer]`; `ntp peer ip-address [normal-sync]
  [version number] [key key-id] [prefer]`; `ntp trusted-key key-number [- end-key]` (a range form exists).
- The guide's authentication-key syntax is `ntp authentication-key number md5 key`. Authentication uses MD5
  cryptographic checksums; packets without a matching trusted key are ignored.
- The guide warns NTP authentication is CPU-intensive and can degrade accuracy; use access lists instead when
  they give enough control. It also notes NTP peer authentication is a vulnerable configuration, not a workaround.
- `ntp source interface` sets the source address for all NTP packets; a per-association `source` keyword exists on
  `ntp server` and `ntp peer`.

## Access groups
`ntp access-group` types, scanned least to most restrictive: `ipv4`, `ipv6`, `peer` (time requests, control queries
and may synchronise to the source), `serve` (time requests and control queries, no synchronisation), `serve-only`
(time requests only), `query-only` (control queries only). If an address matches several, the first type wins. With no
access groups everything is allowed to everyone; once any is configured only the listed types are allowed.

## ntp master
`ntp master` makes the system an authoritative server even if unsynchronised. The guide cautions it is easy to
override valid time sources with it, especially at a low stratum, and several `ntp master` machines that disagree
cause instability.

## Show commands
`show ntp associations`, `show ntp associations detail` and `show ntp status` (example status:
"Clock is synchronized, stratum 8, reference is 127.127.1.1"). An unreachable configured server appears as
"configured, insane, invalid, unsynced, stratum 16" with reach 0 in the guide's detail output.

## Checked
Date: 2026-11-08
Method: documentation only; no commands were run. Read the IOS XE 16 Setting Time and Calendar Services chapter:
Information About NTP (stratum, access group, authentication, authoritative server paragraphs), the ntp server/peer
procedure, the NTP authentication procedure and the show ntp examples. Document 19643 was searched (not read end to
end) for falseticker, hmac, reach and ntp master text; it contains ntp master and ntp update-calendar in a design
example and the cntpPeersReach description, but not the removed claims below. Corrected: the old text used
`hmac-sha2-256` keys and "older IOS: md5 only"; the cited guide documents only md5. Removed as unconfirmed: the
three-source/falseticker rule, `ntp update-calendar` advice, `vrf` server form, standard-ACL requirement, `ntp master 8`
guidance, the association symbols legend, reach 377 meaning, ~1000 s step limit, UDP 123/CoPP notes, chrony key
compatibility and the Verify list.
