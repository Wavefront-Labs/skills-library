---
id: computing-software.systems-network-administration.cisco-networking.infrastructure-acl-edge
name: infrastructure-acl-edge
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, acl, infrastructure-acl, iacl, edge-security, anti-spoofing, control-plane-protection]
level: practitioner
status: draft
description: "Build an infrastructure ACL on internet edge interfaces: deny spoofed and bogon sources, protect router and link addresses, permit what is needed, deploy log-first."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/access-lists/43920-iacl.html
  - https://www.rfc-editor.org/rfc/rfc3704
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Infrastructure ACL at the edge

An iACL on interfaces facing the internet or untrusted peers stops traffic aimed at your
infrastructure (router loopbacks, link addresses, management) while transit traffic to customers
and services passes.

## Structure (inbound on the edge interface)
```
ip access-list extended IACL-IN
 remark --- anti-spoofing: our own space and bogons as source ---
 deny   ip 198.51.100.0 0.0.3.255 any log          ! our public block arriving from outside
 deny   ip 10.0.0.0 0.255.255.255 any
 deny   ip 172.16.0.0 0.15.255.255 any
 deny   ip 192.168.0.0 0.0.255.255 any
 deny   ip 127.0.0.0 0.255.255.255 any
 deny   ip 224.0.0.0 31.255.255.255 any
 remark --- required to the infrastructure ---
 permit tcp host 203.0.113.1 host 203.0.113.2 eq bgp            ! BGP peer
 permit tcp host 203.0.113.1 eq bgp host 203.0.113.2
 permit icmp any 198.51.100.0 0.0.0.255 echo-reply
 permit icmp any 198.51.100.0 0.0.0.255 time-exceeded
 permit icmp any 198.51.100.0 0.0.0.255 unreachable          ! PMTUD needs this
 remark --- block everything else to infrastructure addresses ---
 deny   ip any 198.51.100.0 0.0.0.255 log                    ! infra block (loopbacks, p2p links)
 remark --- transit traffic ---
 permit ip any any
interface GigabitEthernet0/0/0
 ip access-group IACL-IN in
```
Allocate infrastructure addresses from one contiguous block so one deny line protects them all.

## Deploy safely
1. Build with `permit ... log` instead of the infrastructure deny; run for a week.
2. Review hits (`show access-lists IACL-IN`, syslog) for legitimate flows you missed (NTP from
   providers, IPsec peers on UDP 500/4500 and ESP, monitoring probes).
3. Switch to deny. Keep the change window short and have console access.

## Complements
- CoPP protects the control plane from what the iACL lets through.
- uRPF loose/strict mode for anti-spoofing at scale instead of long source lists.
- IPv6 equivalent: deny bogons, permit required ICMPv6 (ND only if link-local, PTB, echo).

## Gotchas
- Order: anti-spoofing first, infrastructure protection next, transit permit last.
- ACL logging is punted to the CPU; use `log` sparingly on high-hit lines or rate-limit
  (`ip access-list logging interval`).
- Provider-assigned link addresses (/30 from ISP space) are not in your block; add them explicitly.

## Verify
- [ ] From an external host, ping/SSH to a loopback fails and is logged, while transit services
  work and BGP stays up.
