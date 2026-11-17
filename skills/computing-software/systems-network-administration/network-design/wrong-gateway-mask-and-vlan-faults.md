---
id: computing-software.systems-network-administration.network-design.wrong-gateway-mask-and-vlan-faults
name: wrong-gateway-mask-and-vlan-faults
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, network-services-troubleshooting, incorrect-gateway, wrong-subnet-mask, vlan-mismatch, apipa, duplicate-ip, ip-conflict, pool-exhaustion, client-ip-parameters, ipconfig, ip-addr, host-misconfiguration]
level: practitioner
status: gated
description: "Diagnose host addressing faults by symptom: wrong gateway, wrong mask, wrong VLAN, APIPA 169.254, duplicate IPs and exhausted DHCP pools, with commands that prove each."
sources:
  - https://www.comptia.org/certifications/network
  - https://datatracker.ietf.org/doc/html/rfc3927
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wrong gateway, mask, VLAN and other host addressing faults

## Read the host first (gated: unconfirmed, source is paywalled or blocked)
```
Windows: ipconfig /all ; route print ; arp -a ; Get-NetIPConfiguration
Linux:   ip -br addr ; ip route ; ip neigh ; resolvectl status
macOS:   ifconfig ; netstat -rn ; scutil --dns
```

## Symptom -> fault
| Symptom | Likely fault | Proof |
|---|---|---|
| Address 169.254.x.x (IPv4 link-local, RFC 3927; APIPA) | no DHCP answer: wrong VLAN, relay missing, pool exhausted, port blocked by 802.1X | DHCP capture shows DISCOVER without OFFER; switch port VLAN |
| Local subnet works, nothing remote | wrong/missing default gateway | `ip route` default points elsewhere; ping gateway fails or gateway IP not on subnet |
| Some local hosts unreachable, some fine | **wrong mask**: host thinks part of its subnet is remote (mask too long) or a remote network is local (mask too short; ARPs for remote hosts, fails) | compare mask with the design; `arp -a` shows incomplete for remote IPs |
| Gets an address from the wrong subnet | port in wrong VLAN, or rogue DHCP | `show interfaces Gi1/0/x switchport`, DHCP server ID in `ipconfig /all` |
| Intermittent connectivity, "address conflict" warning | duplicate IP (static host inside DHCP range, or two statics) | ARP table shows two MACs alternating; switch logs; DHCP conflict log |
| New clients fail, existing fine | DHCP pool exhausted | DHCP server utilisation 100%, NAK/no offer in logs |
| Name fails, IP works | DNS settings wrong (see DNS troubleshooting) | `nslookup` vs ping by IP |

## Fixes
- Statics: keep them outside DHCP ranges and in IPAM; use reservations instead where possible.
- Exhausted pool: shorten leases, widen the scope, check for MAC-randomising
  clients consuming many leases, remove stale leases.
- VLAN: fix the access VLAN; if 802.1X assigns VLANs, check the RADIUS result.
- Duplicate IP: find both MACs (trace-host-to-switch-port), change the wrong one; enable DHCP
  conflict detection (ping before offer).

## Verify
- [ ] Host has correct IP/mask/gateway/DNS matching the subnet design.
- [ ] Ping gateway, a remote host and a name all succeed.
- [ ] No conflict events in the DHCP server or switch logs afterwards.

## Checked

- Date: 2026-10-28
- Confirmed: RFC 3927: IPv4 link-local addressing uses ARP probes and announcements to detect address conflicts.
- Removed: lease-time range, arping option.
- Gated: the host and switch command lines in the Read-the-host block and Proof column (CompTIA page gave no detail).
Method: documentation only; no commands were run.
