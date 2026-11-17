---
id: computing-software.systems-network-administration.cisco-networking.cef-load-sharing
name: cef-load-sharing
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ios-xe, cef, cef-load-sharing, ecmp, per-destination, universal-id, polarization, exact-route]
level: practitioner
status: docs-checked
description: "Control how CEF spreads traffic over equal-cost paths: per-destination vs per-packet, the universal hash ID and polarisation, include-ports, and checking a flow with exact-route."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/express-forwarding-cef/116376-technote-cef-00.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipswitch_cef/configuration/xe-16/isw-cef-xe-16-book/isw-cef-load-balancing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CEF load sharing

With two or more equal-cost paths to a destination, CEF chooses a path with a hash. Load-balancing decisions are
made on the outbound interface, so per-destination or per-packet mode is configured on the outbound interface.

## Modes
| Mode | Behaviour | Use |
|---|---|---|
| per-destination (default once CEF is enabled) | packets for one source-destination host pair always take the same path | the method of choice for most situations |
| per-packet | round robin, successive packets take different paths | not recommended: can reorder packets (breaks VoIP-type traffic); not supported on the ASR 1000 and higher |

```
interface Gi0/1
 ip load-sharing per-destination
ip cef load-sharing algorithm include-ports source destination
```
- Per-destination sharing improves as the number of source-destination pairs grows, so a few large flows between
  the same pair do not spread. `include-ports` adds Layer 4 ports to the decision and helps streams between peer
  addresses that use different ports (for example RTP).
- `ip cef load-sharing algorithm {original | tunnel [id] | universal [id] | include-ports {source [id] | [destination] [id] | source [id] destination [id]}}`.
  `universal` is the default; `original` gives distorted sharing across routers; `tunnel` suits only a few
  source/destination pairs.

## Which path does this flow take?
```
show ip cef exact-route 10.1.1.10 10.9.9.20
show ip cef exact-route 10.1.1.10 src-port 51515 10.9.9.20 dest-port 443
```
The documented form is `show ip cef exact-route source-ip [src-port port] destination-ip [dest-port port]`
(`show ipv6 cef exact-route` for IPv6).

## Polarisation
If routers in a chain use the same hash algorithm and the same input (by default source and destination IP), the
second hop sees only flows that already hashed one way and sends them the same way, leaving other ECMP links idle.
Mitigations from the Cisco technote:
- Use the universal algorithm: it adds a 32-bit router-specific ID, random at boot, to the hash so the same
  source/destination pair hashes differently on different routers. Set a custom value with
  `ip cef load-sharing algorithm universal <id>`; use different IDs on different routers.
- Alternate default (source+destination) and full (plus Layer 4 ports) hash inputs at each layer, and alternate
  an even and odd number of ECMP links per layer.
- Catalyst 6500 only: `mls ip cef load-sharing [full] [simple]`; the `full` option does not include the universal
  ID, so using it at every layer can still polarise. This platform does not support per-packet sharing.
- The same behaviour applies whichever protocol installed the routes (OSPF and EIGRP behave alike).

## Verify
- [ ] `show ip cef exact-route` for a sample flow names the expected outbound link.
- [ ] Traffic is spread over the parallel links across many host pairs.

## Checked
Date: 2026-11-07. Both pages were read through their conceptual sections: the CEF polarization technote (116376,
about 10k characters) in full, and the IOS XE CEF load-balancing chapter (about 31k) for the per-destination,
per-packet, algorithm, include-ports and `ip cef load-sharing algorithm` sections; its GTP-U sections and the
feature history table were skimmed.
Confirmed: per-destination default and its properties, per-packet reordering and the ASR 1000 note, the algorithm
keywords and syntax, universal as default with the 32-bit boot-time ID and the custom `universal <id>` command,
polarisation mitigations, the Catalyst 6500 hash options, the `show ip cef exact-route` syntax (from the GTP-U text).
Removed: `protocol tcp` in exact-route (not in the syntax), `show ip cef <prefix> internal`, the Catalyst fed and
etherchannel load-balance commands, `show cef state`, the unequal-path claims (EIGRP variance, dmzlink-bw, SD-WAN),
and the elephant-flow, asymmetric-firewall and rehash gotchas (none are on the pages).
Method: documentation only; no commands were run.
