---
id: computing-software.systems-network-administration.cisco-networking.nat-translation-troubleshooting
name: nat-translation-troubleshooting
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, nat, nat-translations, nat-troubleshooting, debug-ip-nat, order-of-operations]
level: practitioner
status: draft
description: "Troubleshoot IOS NAT: empty translation table, wrong inside/outside, ACL misses, order of operations with routing and ACLs, and safe debug ip nat."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/network-address-translation-nat/8605-13.html
  - https://www.cisco.com/c/en/us/support/docs/ip/network-address-translation-nat/6209-5.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NAT troubleshooting on IOS

## Order of operations (inside -> outside)
input ACL -> routing decision -> **NAT inside-to-outside** -> output ACL. On the way back
(outside -> inside): input ACL on outside -> NAT outside-to-inside -> routing.
So an inbound ACL on the outside interface sees **public** destination addresses, and
routing for return traffic uses the translated **inside** address.

## Checklist when "NAT does not work"
1. `show ip nat statistics`: are both interfaces listed under Inside/Outside? If not, `ip nat
   inside|outside` is missing (or on the wrong subinterface/SVI).
2. Hits zero: the ACL/route-map in the rule does not match the source. Test:
   `show access-lists NAT-INSIDE` counters.
3. Hits but no reply: the outside world has no route back to the public address, or the ISP
   filters it. Ping from the router sourced from the public IP.
4. Misses rising: pool exhausted or max-entries reached.
5. Return traffic arrives on a different router/interface (asymmetric), so no translation found.
6. Default route missing: NAT happens after routing; no route = no translation.

## See it happen
```
show ip nat translations verbose | include 10.1.1.50
clear ip nat translation inside 10.1.1.50 203.0.113.5 ! clear one dynamic entry
access-list 199 permit ip host 10.1.1.50 any
access-list 199 permit ip any host 10.1.1.50
debug ip nat 199 detailed           ! scope it with an ACL; never unscoped on a busy box
```
Debug output `NAT: s=10.1.1.50->203.0.113.5, d=8.8.8.8 [123]` means inside->outside worked;
missing `NAT*:` lines for replies means they never reached this router.
Use `undebug all` immediately after.

## IOS-XE platform checks
```
show platform hardware qfp active feature nat datapath stats
show ip nat translations total
```
Hardware NAT drops (e.g. ALG errors) show up only in the QFP stats.

## Verify
- [ ] Translation appears for the test host and replies are translated back (debug or counters).
