---
id: computing-software.systems-network-administration.network-design.ipv6-multihoming-and-nptv6
name: ipv6-multihoming-and-nptv6
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, ipv6-multihoming, nptv6, pi-space, provider-aggregatable, ipv6-design]
level: practitioner
status: docs-checked
description: "Multihome IPv6 sites: PI space with BGP, PA prefixes from two ISPs with source-address problems, and NPTv6 prefix translation as a stateless middle ground."
sources:
  - https://www.rfc-editor.org/rfc/rfc6296
  - https://www.rfc-editor.org/rfc/rfc7157
  - https://www.rfc-editor.org/rfc/rfc8678
  - https://www.ripe.net/publications/docs/ripe-738/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IPv6 multihoming and NPTv6

## Options
| Approach | How | Trade-offs |
|---|---|---|
| PI space + BGP | own PI prefix (from the RIR), announce to both ISPs | cleanest failover; needs ASN/BGP skills and meeting the RIR's PI criteria |
| Multiple PA prefixes | each ISP delegates a prefix; hosts get an address from each | hosts must pick the right source for the exit, else ingress filtering (BCP 38) drops packets |
| NPTv6 (RFC 6296) | internal prefix translated 1:1 to each ISP prefix at the edge | stateless, checksum-neutral, no port translation; still address translation, so read RFC 6296 for what it does not solve |

## Multiple PA prefixes problems (RFC 7157, RFC 8678)
- Source address selection on hosts does not know which uplink is up; a failed ISP leaves hosts
  using its prefix until RAs deprecate it.
- The router must do source-based routing so packets with ISP-A source exit via ISP-A.
- On failure, deprecate the dead prefix via RA (preferred lifetime 0) quickly.

## NPTv6 notes
- Prefix lengths: RFC 6296 section 3 has separate rules for a /48 or shorter prefix and a /49 or longer one;
  plan the internal and external prefix lengths with them.
- Translation is stateless, so asymmetric routing is fine.
- Implementations exist in Linux and in commercial firewalls and routers; check the platform documentation.
- Inbound services need DNS records for each external prefix or a primary one.

## Recommendation
Enterprises with real multihoming needs: PI + BGP. Small sites wanting failover without BGP:
NPTv6 with ULA inside, or accept single-ISP IPv6 with v4 failover.

## Verify
- [ ] Pull each uplink in turn: v6 sessions re-establish (new ones at least) within the target time and no packets leave with the dead ISP's source.

## Checked

2026-10-28: Confirmed: RFC 6296 (NPTv6 is stateless, transport-agnostic, checksum-neutral and does not map ports; section 3 has separate /48-or-shorter and /49-or-longer cases), RFC 7157 and RFC 8678 (source address selection and ingress filtering, BCP 38, drop packets with the wrong ISP source), RIPE-738 (IPv6 Provider Independent assignment section). Removed: the /48 PI size, RIR fee claim, ULA-inside wording, the same-length prefix rule, and the Linux/IOS-XE/SRX/PAN/FortiGate command and feature names.
Method: documentation only; no commands were run.
