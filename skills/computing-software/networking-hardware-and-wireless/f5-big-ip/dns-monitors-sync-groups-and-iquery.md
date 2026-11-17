---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.dns-monitors-sync-groups-and-iquery
name: dns-monitors-sync-groups-and-iquery
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, iquery, gtm-sync-group, bigip-monitor]
level: practitioner
status: draft
description: "Link BIG-IP DNS and LTM devices via iQuery, set the GTM sync group and use the bigip monitor, with port and certificate checks."
sources:
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-dns-services-implementations.html
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-device-service-clustering-administration.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GTM monitors, sync groups and iQuery

```
tmsh run gtm gtm_add          # older: bigip_add / gtm_add script, run on the peer
tmsh modify gtm global-settings general synchronization yes synchronization-group-name sync_dns
tmsh modify gtm global-settings general synchronization-time-tolerance 10
tmsh create gtm monitor bigip mon_bigip aggregate-dynamic-ratios average-nodes
tmsh show gtm iquery
tmsh list gtm server srv_east monitor
```
- iQuery: BIG-IP DNS devices connect to every BIG-IP in the configured servers on `TCP 4353` (SSL-authenticated); this lets them pull virtual server status and performance. Firewalls between data centers must allow it, and self IPs must allow `tcp:4353`.
- `gtm_add` (or `bigip_add`) exchanges the trust certificates; in newer versions device trust takes care of it (confirm).
- GTM sync group: all DNS devices with `synchronization yes` and the same group name share the wide IP/pool configuration. Changes propagate if the most recent timestamp wins within `time-tolerance` - a unit with an older clock can overwrite newer config. Keep NTP healthy.
- The `bigip` monitor uses iQuery status from LTM virtual servers, so no additional probes are sent. Pair with a protocol monitor for the application itself.
- Gotcha: if `show gtm iquery` shows `not-connected`, check routing for return traffic to 4353 and mismatched certificates (self-signed cert expiry on one device).

Verify: `tmsh show gtm iquery` shows all peers `connected`, and `tmsh show gtm server` shows virtual servers with `available` status.
