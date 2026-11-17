---
id: computing-software.systems-network-administration.network-design.special-purpose-ipv4-ranges
name: special-purpose-ipv4-ranges
category: computing-software
field: systems-network-administration
product: network-design
tags: [ipv4, special-purpose-addresses, bogons, rfc6890, documentation-prefixes, link-local, multicast-range]
level: practitioner
status: verified
description: "Know the special-purpose IPv4 blocks (RFC 6890 registry): loopback, link-local, documentation, benchmarking, shared, multicast, reserved, and how to use them in bogon filters."
sources:
  - https://www.rfc-editor.org/rfc/rfc6890
  - https://www.iana.org/assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml
  - https://www.rfc-editor.org/rfc/rfc5737
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Special-purpose IPv4 ranges

## The registry (IANA IPv4 Special-Purpose Address Registry, RFC 6890)
| Block | Purpose | Routable on internet |
|---|---|---|
| 0.0.0.0/8 | "this network"; 0.0.0.0 as source during DHCP | no |
| 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 | private (RFC 1918) | no |
| 100.64.0.0/10 | shared address space for CGNAT (RFC 6598) | no |
| 127.0.0.0/8 | loopback | no |
| 169.254.0.0/16 | link-local / APIPA; also cloud metadata 169.254.169.254 | no |
| 192.0.0.0/24 | IETF protocol assignments (192.0.0.0/29 DS-Lite and IPv4 service continuity, 192.0.0.8 IPv4 dummy address, 192.0.0.170/171 NAT64/DNS64 discovery; 192.0.0.9 and .10 are globally reachable anycast) | mostly no |
| 192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24 | documentation (TEST-NET-1/2/3, RFC 5737) | no |
| 192.88.99.0/24 | deprecated 6to4 relay anycast | no |
| 198.18.0.0/15 | benchmarking (RFC 2544) | no |
| 224.0.0.0/4 | multicast | special |
| 240.0.0.0/4 | reserved (class E) | no |
| 255.255.255.255/32 | limited broadcast | no |

## Practical uses
- Use 192.0.2.0/24 etc in documentation, examples and lab configs that might leak; never real
  third-party addresses.
- 198.18.0.0/15 for lab/test networks and some VPN/proxy products' internal ranges (expect clashes
  with tools that already use it, e.g. some SD-WAN and secure web gateways).
- 100.64.0.0/10 only for CGNAT/carrier use; Tailscale uses it for its node addresses (its docs call it the CGNAT range), so avoid
  it in enterprise designs.

## Bogon filtering at the edge
Drop these as sources inbound from the internet and as destinations outbound (plus your own
public prefixes as inbound sources). Match each prefix and anything more specific inside it:
```
0.0.0.0/8       10.0.0.0/8       100.64.0.0/10   127.0.0.0/8
169.254.0.0/16  172.16.0.0/12    192.0.0.0/24    192.0.2.0/24
192.88.99.0/24  192.168.0.0/16   198.18.0.0/15   198.51.100.0/24
203.0.113.0/24  224.0.0.0/3 (multicast plus class E, which also covers 255.255.255.255)
```
Checked against the IANA registry CSV: every entry that is not globally reachable falls inside this
list; the only registry blocks left out are the globally reachable 192.31.196.0/24 (AS112),
192.52.193.0/24 (AMT) and 192.175.48.0/24 (AS112 delegation). Note 192.0.0.0/24 also contains
the globally reachable 192.0.0.9 and 192.0.0.10, so drop it only if you do not use those
anycast services. Express the list in your platform's prefix-list or ACL syntax (look that up
in the vendor documentation; it is not reproduced here) and use it as a deny in BGP inbound
policy and as an ACL source list. Full bogons (unallocated space)
change; consume Team Cymru's bogon feed rather than hard-coding.

## Gotchas
- 240.0.0.0/4 is unusable on some OS stacks: a ping to 240.0.0.1 on Windows 11 failed with `General failure` before sending, and Google Cloud's VPC docs say some operating systems do not support the range.
- 169.254.169.254 is the AWS instance metadata address (IPv4; AWS also offers `fd00:ec2::254` on Nitro instances in IPv6 subnets) and must stay reachable from cloud instances; do not route it elsewhere.

## Verify
- [ ] Edge filters include the table above and logs show hits only from spoofed or misconfigured
  sources.
