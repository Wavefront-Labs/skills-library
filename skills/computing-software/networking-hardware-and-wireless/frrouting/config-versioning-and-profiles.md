---
id: computing-software.networking-hardware-and-wireless.frrouting.config-versioning-and-profiles
name: config-versioning-and-profiles
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, frr-version, frr-defaults, traditional, datacenter, upgrade]
level: advanced
status: docs-checked
description: "Understand FRR frr version and frr defaults traditional or datacenter, which defaults depend on profile or version, and why saved config pins behaviour across upgrades."
sources:
  - https://docs.frrouting.org/en/latest/basic.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Config versioning and profiles
- `frr version <X>` sets the version whose defaults apply. It is loaded from config and sticky across upgrades.
- `frr defaults traditional|datacenter` sets the profile. The `-F` option presets it, but any `frr defaults` statement in config takes precedence. All daemons must use the same profile.
- Saving config does not change the active version; restarting does, because it reloads the written `frr version`.

Profile-dependent defaults: BGP timers, `bgp default show-hostname`, `bgp deterministic-med`, `log-adjacency-changes` in ospfd and ospf6d, and zebra NHT settings. Example BGP timers from the page:
- `timers bgp` keepalive 60 s traditional, 3 s datacenter.
- Hold time 180 s traditional, 9 s datacenter.
- `neighbor ... timers connect` 30 s traditional, 10 s datacenter.

Version-dependent defaults: `bgp suppress-duplicates` (7.6), `bgp graceful-restart notification` (8.3), `bgp hard-administrative-reset` (8.3), `bgp enforce-first-as` (9.1). Some BGP defaults depend on both (`ebgp-requires-policy`, `network import-check`).

Also useful: `allow-reserved-ranges` permits reserved ranges such as 127.0.0.0/8 and 0.0.0.0/8 (default off; 240.0.0.0/4 is allowed by default).

## Checked

2026-11-04. Confirmed against the FRR Basic Commands page: frr version and frr defaults behaviour, profile table, version-dependent defaults, and allow-reserved-ranges. Nothing changed.
Method: documentation only; no commands were run.
