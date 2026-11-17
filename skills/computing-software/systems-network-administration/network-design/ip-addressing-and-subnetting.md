---
id: computing-software.systems-network-administration.network-design.ip-addressing-and-subnetting
name: ip-addressing-and-subnetting
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, ip-addressing, subnetting, cidr, ipv4, ipv6, rfc1918, private-ip, subnet-mask, vlsm, supernetting, route-summarisation, addressing-plan, ipam, vlan, slash-64, slash-48, slash-56, prefix-delegation, slaac, point-to-point, slash-31, cgnat, ipcalc, sipcalc, netbox]
level: practitioner
status: verified
description: "Plan IPv4/IPv6 addressing: CIDR subnet math with worked examples, RFC 1918 ranges, VLAN-per-subnet plans, reserved ranges, /64 per LAN and /48 or /56 per site."
sources:
  - https://www.rfc-editor.org/rfc/rfc1918
  - https://www.rfc-editor.org/rfc/rfc4632
  - https://www.rfc-editor.org/rfc/rfc6177
  - https://www.rfc-editor.org/rfc/rfc3021
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IP addressing and subnetting — do the math once, design so you never redo it

**Goal:** carve address space into subnets you can calculate in your head, summarise per
site, and grow without renumbering, for both IPv4 and IPv6.

## 1. CIDR math in four facts
1. A `/n` prefix leaves `32 − n` host bits: size = `2^(32−n)` addresses.
2. Usable IPv4 hosts = size − 2 (network and broadcast), except `/31` (2 usable, RFC 3021,
   point-to-point links) and `/32` (single host).
3. Subnets start on multiples of their size: a `/26` (64) starts at .0, .64, .128, .192.
4. The "interesting octet" block size = 256 − mask value in that octet.

| Prefix | Mask | Addresses | Usable |
|---|---|---|---|
| /30 | 255.255.255.252 | 4 | 2 |
| /29 | .248 | 8 | 6 |
| /27 | .224 | 32 | 30 |
| /26 | .192 | 64 | 62 |
| /24 | 255.255.255.0 | 256 | 254 |
| /23 | 255.255.254.0 | 512 | 510 |
| /22 | 255.255.252.0 | 1024 | 1022 |
| /16 | 255.255.0.0 | 65 536 | 65 534 |

## 2. Worked examples
**Which subnet is 10.20.37.130/22 in?** /22 → third-octet mask 252, block 4. 37 ÷ 4 → 36.
Network `10.20.36.0`, broadcast `10.20.39.255`, hosts `.36.1`–`.39.254`.

**Split 198.51.100.0/24 for 100, 50, 20 hosts and 2 links (VLSM, largest first):**
| Need | Prefix | Subnet | Usable range |
|---|---|---|---|
| 100 | /25 | 198.51.100.0/25 | .1–.126 |
| 50 | /26 | 198.51.100.128/26 | .129–.190 |
| 20 | /27 | 198.51.100.192/27 | .193–.222 |
| link | /31 | 198.51.100.224/31 | .224–.225 |
| link | /31 | 198.51.100.226/31 | .226–.227 |
Remaining: .228–.255 free for growth.

**Summarise 10.20.0.0/24 … 10.20.3.0/24:** four contiguous, aligned /24s = `10.20.0.0/22`.
Summaries only work when blocks are contiguous and aligned to the summary size.

Check with Python's `ipaddress` module (every table and worked example above was recomputed with it:
`ip_network('10.20.37.130/22', strict=False)` gives `10.20.36.0/22`, and `collapse_addresses` turns the four /24s into `10.20.0.0/22`).

## 3. Private and special ranges
- RFC 1918: `10.0.0.0/8`, `172.16.0.0/12` (172.16–172.31), `192.168.0.0/16`.
- Avoid `192.168.0.0/24` and `192.168.1.0/24` for corporate LANs: home routers use them,
  and VPN users then collide. Also avoid `100.64.0.0/10` (carrier-grade NAT, used by
  some VPN/overlay products), and check cloud VPC and container ranges before allocating. Docker's built-in pools
  (moby `ipamutils`) are `172.17.0.0/16` through `172.31.255.255` carved as /16s, then
  `192.168.0.0/16` carved as /20s, so Docker hosts can take both 172.16/12 and 192.168/16 space.
- Documentation-only: `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`, `2001:db8::/32`.

## 4. An addressing plan that scales
Hierarchy: **organisation → site → function**, so each site summarises to one route.
Example: `10.0.0.0/8` org; `10.<SITE>.0.0/16` per site (up to 256 sites); inside a site:
| Block | Use |
|---|---|
| 10.S.0.0/24 | Infrastructure / management (VLAN 99) |
| 10.S.1.0/24 | Network links (/31s) and loopbacks (/32s) |
| 10.S.10.0/23 | Users wired (VLAN 10) |
| 10.S.20.0/23 | Wi-Fi corporate (VLAN 20) |
| 10.S.30.0/24 | Voice (VLAN 30) |
| 10.S.40.0/24 | Servers (VLAN 40) |
| 10.S.50.0/24 | Printers / IoT (VLAN 50) |
| 10.S.128.0/17 | Reserved for growth |

Conventions that save time:
- **One VLAN = one subnet**; encode the VLAN ID in the third octet where possible.
- **Gateway at .1** (or the first usable) everywhere; .2–.3 for HSRP/VRRP peers.
- **Reserve a static range** in each subnet (e.g. .1–.20) and give DHCP the rest; servers
  and printers get DHCP reservations or statics from the reserved block.
- Size user subnets at ~2× current hosts: a /24 is 254 hosts; prefer /23 for big
  Wi-Fi rather than one huge broadcast domain (/22 and bigger: broadcast/ARP load and
  blast radius grow).
- Record everything in an IPAM (NetBox, phpIPAM, Infoblox), not a stale spreadsheet.

## 5. IPv6
- **/64 per LAN, always.** SLAAC and many features assume it. Do not use longer prefixes
  on host LANs even though space looks "wasted".
- **Per site:** /48 is the common enterprise recommendation; ISPs often give /56 to small
  sites/homes (RFC 6177 relaxed the /48 default). A /48 = 65 536 /64s; a /56 = 256.
- Encode structure in nibbles (4-bit boundaries) so addresses stay readable:
  `2001:db8:<SITE>:<VLAN>::/64`, e.g. VLAN 10 at site 0x12 → `2001:db8:12:10::/64`
  (hex digits mirroring the decimal VLAN number is a readable convention, not maths).
- Point-to-point links: /127 (RFC 6164), but often allocate a /64 per link and configure
  a /127 from it.
- ULA (`fd00::/8`, random 40-bit Global ID) only for internal-only needs.

## Verify
- [ ] Every subnet is aligned to its own size and no two subnets overlap (Python `ip_network` with the default `strict=True` rejects misaligned ones; IPAM check).
- [ ] Each site summarises to one prefix in the routing table.
- [ ] No corporate range collides with common home, VPN, CGNAT, cloud or Docker ranges.
- [ ] Each VLAN maps to one subnet with a documented gateway, static range and DHCP range.
- [ ] IPv6: every LAN is a /64 and each site holds a /48 or /56 with room to grow.
