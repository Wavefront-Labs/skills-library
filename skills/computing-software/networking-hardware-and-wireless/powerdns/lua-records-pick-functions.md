---
id: computing-software.networking-hardware-and-wireless.powerdns.lua-records-pick-functions
name: lua-records-pick-functions
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, lua-records, pickrandom, pickwhashed, pickchashed, picknamehashed, closestmagic, view]
level: practitioner
status: docs-checked
description: "PowerDNS LUA selection without health checks: pickrandom, pickhashed, pickwhashed, pickchashed, pickclosest, closestMagic, view."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/lua-records/functions.rst
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/lua-records/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LUA pick functions

- `pickrandom(values)`: random element. `pickrandomsample(n, values)`: N random elements. `all(values)`: everything.
- `pickhashed(values)`: hash of `bestwho` picks one value.
- `pickwhashed(values)`: weighted hash of `bestwho`; values are `{weight, value}` pairs, so a given client keeps its answer while load spreads by weight.
- `pickchashed(values)`: like `pickwhashed` with consistent hashing: reordering is harmless and changing one weight moves only part of the distribution. Costs more CPU and memory; the cache cleans up every 1 h by default and drops entries unused for 24 h.
- `pickwrandom(values)`: weighted random per query.
- `picknamehashed(values)`: weighted hash of `qname`, so a name always gets the same answer; mainly for wildcards.
- `pickclosest(addresses)`: the address closest to `bestwho` (needs the geoip backend).
- `closestMagic()`: for wildcard A records; reads encoded IPs from `qname` such as `192-0-2-1.192-0-2-2.198-51-100-1.magic.v4.powerdns.org` and returns the closest to `bestwho`. No uptime checks.
- `view(pairs)`: `{ {netmasks}, {result} }` pairs; the result whose netmasks match the client is returned (the page example puts `0.0.0.0/0` last as the catch-all).

Variables: `who` (resolver), `ecswho` (ECS, unset if none), `bestwho` (ECS network if sent, else the resolver), `localwho`, `qname`, `zone`, `zoneid`, `tcp`, `dnssecOK`, `ednsPKTSize`, `dh`.

## Checked

2026-11-08. Read in full: PowerDNS docs lua-records/functions.rst and lua-records/index.rst. Confirmed each pick function and its hashing basis, the pickchashed cleanup defaults (1 h, 24 h), the closestMagic name format and lack of uptime checks, the geoip requirement for pickclosest, and the preset variable list. Removed the unsupported unweighted and first-match claims.

Method: documentation only; no commands were run.
