---
id: computing-software.networking-hardware-and-wireless.frrouting.bgp-neighbor-session-setup
name: bgp-neighbor-session-setup
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, bgpd, neighbor, remote-as, update-source, ebgp-multihop, ttl-security, md5-password, local-as]
level: practitioner
status: docs-checked
description: "Create FRR BGP neighbors: remote-as internal, external or auto, update-source, multihop, GTSM ttl-security, MD5 password, local-as, capabilities."
sources:
  - https://docs.frrouting.org/en/latest/bgp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP neighbor session setup
- `neighbor PEER remote-as ASN` must be the first neighbor command; `remote-as internal` denies a session if the peer ASN differs, `external` denies if it matches, `auto` learns the ASN from OPEN.
- `neighbor PEER update-source <IFNAME|ADDRESS>`; with an interface name zebra must be running.
- `neighbor PEER ebgp-multihop` for non-directly-connected eBGP; `neighbor PEER disable-connected-check` for directly connected eBGP peers on loopbacks.
- `neighbor PEER ttl-security hops NUMBER` enforces GTSM (RFC 5082); excludes `ebgp-multihop`.
- `neighbor PEER password PASSWORD` sets an MD5 password. `neighbor PEER port PORT`.
- `neighbor PEER description ...`.
- `neighbor PEER local-as AS-NUMBER [no-prepend [replace-as [dual-as]]]` (`replace-as` requires `no-prepend`; `dual-as` accepts the real ASN or the local-as).
- `neighbor PEER shutdown [message MSG...] [rtt (1-65535) [count (1-255)]]` keeps configuration; the rtt option shuts the peer down when round-trip time exceeds the given ms.
- `neighbor PEER tcp-mss (1-65535)` takes effect after a hard reset; the synced value is 12 to 14 bytes lower than configured (150 syncs as 138).
- Capabilities: `capability dynamic`, `capability fqdn` (default on), `capability software-version`, `strict-capability-match`, `dont-capability-negotiate`, `override-capability`.
- `neighbor PEER enforce-first-as`, `ip-transparent`, `extended-optional-parameters`.
- `neighbor PEER path-attribute discard|treat-as-withdraw (1-255)...`; ORIGIN, AS_PATH, NEXT_HOP, MULTI_EXIT_DISC, MP_REACH_NLRI, MP_UNREACH_NLRI, EXT_COMMUNITIES and OTC cannot be listed (for eBGP peers also LOCAL_PREF, ORIGINATOR_ID and CLUSTER_LIST).

Check with `show bgp neighbors <addr>`.

## Checked
2026-11-09. Partial read of docs.frrouting.org bgp.html (one large page): the neighbor command reference, ttl-security, disable-connected-check, capability fqdn, path-attribute discard and treat-as-withdraw, shutdown, and the tcp-mss section. Fixed: tcp-mss reduction (12 to 14 bytes) and the path-attribute exclusion list. Removed: show bgp summary and the eBGP-only restriction on local-as (not stated in the sources).
Method: documentation only; no commands were run.
