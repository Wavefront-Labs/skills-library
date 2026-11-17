---
id: computing-software.systems-network-administration.pi-hole.blocking-modes-and-edns
name: blocking-modes-and-edns
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [blocking-mode, nxdomain-null-nodata, edns-blocked-code]
level: practitioner
status: docs-checked
description: "Choose how Pi-hole answers blocked queries (NULL, IP, NXDOMAIN, NODATA) and what EDNS block information it adds."
sources: ["https://docs.pi-hole.net/ftldns/blockingmode/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Blocking modes and EDNS

`dns.blocking.mode` decides the reply for a blocked domain. Default is `NULL`.

| Mode | Reply |
| --- | --- |
| `NULL` | The unspecified address (`0.0.0.0` or `::`); default and recommended |
| `IP` | The Pi-hole's own local IP addresses |
| `IP_NODATA_AAAA` | Local IPv4 addresses; blocked AAAA queries get NODATA, so clients only try the IPv4 address |
| `NX` | Empty response with status NXDOMAIN, meaning no such domain |
| `NODATA` | Empty response with status NODATA: the domain exists but has no record of that type |

In `NULL` mode blocked queries get the unspecified address (RFC 3513 section 2.5.2).

**Custom reply addresses.** Under `[dns.reply.blocking]`, `force4`/`IPv4` and `force6`/`IPv6` replace the interface address used in IP blocking mode and with the `;reply=IP` regex extension.

**EDNS.** `dns.blocking.edns` (default `TEXT`) enriches blocked replies: `NONE` adds nothing, `CODE` adds EDNS info-code BLOCKED (15), `TEXT` adds the code plus a text reason.

**TTL.** `dns.blockTTL` (default `2` seconds) is the TTL handed out for blocked answers. Large values may make whitelisting ineffective because clients cache the block.

**Temporarily off.** `dns.blocking.active` (default `true`) turns blocking on or off.

**Checklist**

1. `NULL` is the default and recommended mode.
2. Large `blockTTL` values may make allow-listing ineffective because clients cache the block.
3. Apply with `pihole-FTL --config dns.blocking.mode NX`.

## Checked

2026-11-03. Read the `dns.blocking.mode`, `dns.blocking.edns`, `dns.blocking.active`, `dns.blockTTL` and `[dns.reply.blocking]` sections of the FTL configuration reference: five modes and their replies, EDNS NONE/CODE/TEXT with info-code BLOCKED (15), blockTTL 2, force4/force6 and the `;reply=IP` regex extension. Removed the unsupported claim that clients stop quickly because connections are refused.

Method: documentation only; no commands were run.
