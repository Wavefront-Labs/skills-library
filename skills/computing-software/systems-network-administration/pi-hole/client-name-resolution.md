---
id: computing-software.systems-network-administration.pi-hole.client-name-resolution
name: client-name-resolution
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [resolver-names, mac-names, refresh-names]
level: practitioner
status: docs-checked
description: "Control how Pi-hole turns client IPs into hostnames: PTR lookups, MAC-based names, network table fallback and refresh policy."
sources: ["https://docs.pi-hole.net/ftldns/configfile/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Client name resolution

Under `[resolver]`, FTL decides how to show names instead of bare IPs.

| Option | Default | Effect |
| --- | --- | --- |
| `resolveIPv4` | `true` | Try to resolve IPv4 addresses to hostnames |
| `resolveIPv6` | `true` | Same for IPv6 |
| `macNames` | `true` | Obtain names from the network table by MAC address; helps devices with several IPs but can be ambiguous when one MAC appears for many IPs (router/NAT or MAC reuse) |
| `networkNames` | `true` | Fallback: an IPv6 client without a name takes the name of another address with the same MAC |
| `refreshNames` | `IPV4_ONLY` | Hourly PTR re-checks |

**refreshNames values**

- `IPV4_ONLY`: IPv4 only; default since FTL v5.3.2 because short-lived IPv6 addresses created too many lookups.
- `ALL`: all addresses.
- `UNKNOWN`: only unknown names; known names never update.
- `NONE`: look a name up once, never again.

**Network table.** `database.network.parseARPcache` (default `true`) analyses the local ARP cache; turning it off stops client identification and the network table working reliably. `database.network.expire` (default `91`) removes addresses older than that many days.

**Checklist**

1. If names are wrong behind a router, disable `macNames`.
2. If names are missing, add a reverse server.
3. Use `UNKNOWN` to cut PTR traffic.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: FTL Configuration Reference (ftldns/configfile). Nothing needed removing.
Method: documentation only; no commands were run.
