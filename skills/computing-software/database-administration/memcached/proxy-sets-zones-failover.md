---
id: computing-software.database-administration.memcached.proxy-sets-zones-failover
name: proxy-sets-zones-failover
category: computing-software
field: database-administration
product: memcached
tags: [zones, local-zone, pool-sets, failover, replication]
level: advanced
status: docs-checked
description: "Group pools into set_ sets, declare local_zone, and use route_failover for nearest-first failover and replication layouts."
sources:
  - https://docs.memcached.org/features/proxy/configure/
  - https://docs.memcached.org/features/proxy/examples/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Sets: a pool whose name starts with `set_` holds anonymous pools.
```
pools { set_main = { { backends = {"192.0.2.1"} }, { backends = {"192.0.2.2"} } } }
routes { route_failover{ children = "set_main", shuffle = true } }
```
Passing a set name equals passing the list of its pools.

Zones: label the pools by name inside a set and declare your zone:
```
local_zone("west")      -- or local_zone_from_env("ZONE") / local_zone_from_file(path)
pools { set_main = { west = {backends={...}}, east = {backends={...}} } }
```
`route_failover` tries the local zone first when a zoned set is supplied; the reference notes which handlers support zones.

Replication sample: `cmap = { get = route_failover{ children="set_main", miss=true, shuffle=true } }`, `default = route_allfastest{...}` to copy writes to all pools.

Test: stop one backend or mark it `_down_` and confirm hits continue.

## Checked

Confirmed against the configure and examples pages: set_ naming and equivalence to a pool list, local_zone, local_zone_from_env and local_zone_from_file, zone-labelled pools, route_failover zone preference, the replication example with cmap get failover and a default route_allfastest, and the _down_ marker. Removed the capacity-halving claim, which the pages do not state, and softened the route_allfastest zone claim.

Method: docs-checked 2026-11-09 against docs.memcached.org/features/proxy/configure/, /reference/ and /examples/ (HTML converted to text and read in full).
