---
id: computing-software.systems-network-administration.network-design.binary-and-subnet-mask-arithmetic
name: binary-and-subnet-mask-arithmetic
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, binary-conversion, subnet-mask, wildcard-mask, ipv4-addressing, subnetting]
level: practitioner
status: verified
description: "Convert between dotted decimal, binary and prefix length fast and exactly: octet values, block sizes, wildcard masks, and AND-ing an address with a mask by hand."
sources:
  - https://www.rfc-editor.org/rfc/rfc4632
  - https://www.rfc-editor.org/rfc/rfc950
  - https://www.cisco.com/c/en/us/support/docs/ip/routing-information-protocol-rip/13788-3.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Binary and subnet mask arithmetic

## Octet place values
`128 64 32 16 8 4 2 1`. 200 = 128+64+8 = `11001000`. 37 = 32+4+1 = `00100101`.

## Mask octets (memorise)
| Bits set | Value | Block size |
|---|---|---|
| 1 | 128 | 128 |
| 2 | 192 | 64 |
| 3 | 224 | 32 |
| 4 | 240 | 16 |
| 5 | 248 | 8 |
| 6 | 252 | 4 |
| 7 | 254 | 2 |
| 8 | 255 | 1 |

Block size = 256 - mask octet. Prefix -> mask: /22 = 8+8+6 -> `255.255.252.0`.

## Finding network, broadcast and range
Address 172.16.45.130/22:
1. Interesting octet = third (bits 17-24), mask 252, block 4.
2. Network = largest multiple of 4 <= 45 -> 44 -> `172.16.44.0`.
3. Broadcast = next network - 1 -> `172.16.47.255`.
4. Hosts `172.16.44.1`-`172.16.47.254`, count 2^(32-22) - 2 = 1022.

Formal version: network = address AND mask; broadcast = network OR (NOT mask).

## Wildcard (inverse) masks
Wildcard = 255.255.255.255 - mask. /22 -> `0.0.3.255`. Used in Cisco ACLs and OSPF `network`
statements. Non-contiguous wildcards (`0.0.254.255`) match patterns such as odd third octets;
legal in ACLs, confusing in reviews, so comment them.

## Tools to check your work
```
python -c "import ipaddress as i;n=i.ip_interface('172.16.45.130/22').network;print(n,n.broadcast_address,n.hostmask,n.num_addresses-2)"
python -c "print(format(200,'08b'), format(37,'08b'))"
```
The first prints `172.16.44.0/22 172.16.47.255 0.0.3.255 1022`, the second `11001000 00100101`
(both run with Python 3.14). Do not rely on `bc` or `ipcalc` being installed; neither is on a stock
Git Bash or Windows.

## Verify
- [ ] Hand calculations for network/broadcast/host count match Python `ipaddress` for a set of random addresses and prefixes /8 to /30.
- [ ] A wildcard such as `0.0.254.255` matches the base's low bit of the third octet only (checked: base `10.1.1.0` matches third octets 1, 3 and 255, not 2).
