---
id: computing-software.systems-network-administration.dns-dhcp.transfer-source-addressing
name: transfer-source-addressing
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, transfer-source, notify-source, bind, multihomed, zone-transfers]
level: practitioner
status: docs-checked
description: "Control which source address BIND uses for zone transfers and NOTIFY with transfer-source and notify-source on multihomed or anycast servers."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html#namedconf-statement-transfer-source
  - https://bind9.readthedocs.io/en/latest/reference.html#namedconf-statement-notify-source
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# transfer-source addressing

On multihomed or anycast servers, the kernel picks the outgoing address by routing. The primary's
`allow-transfer` ACL, firewall rules or TSIG-less IP trust then see an unexpected address and refuse.

## On a secondary
```
options {
    transfer-source 10.0.0.54;          // IPv4 source for SOA queries and AXFR/IXFR
    transfer-source-v6 2001:db8::54;
};
zone "example.com" {
    type secondary;
    primaries { 192.0.2.53; };
    transfer-source 10.0.0.54;          // per-zone override
};
```
A named list can also carry a source: `remote-servers "p" source 10.0.0.54 { 192.0.2.53; };` (grammar: `remote-servers <name> [port N] [source <addr>] [source-v6 <addr>] { ... }`). Run `named-checkconf` to validate.

## On a primary
```
options { notify-source 10.0.0.53; notify-source-v6 2001:db8::53; };
```
The `notify-source` address must appear in the secondary's primaries clause or in an `allow-notify` clause, so a NOTIFY from a different interface or the anycast address is not accepted. Both options can be overridden per zone or view.

## Anycast specifics
Do not source transfers from an anycast service address: replies can be routed to a different instance. Use a unique per-node unicast address, and list it in the primary's `allow-transfer`.

## Diagnose
```
grep -E "notify|transfer of" /var/log/named/*.log        # xfer-in, xfer-out and notify categories
```
A denied transfer is logged by the primary in the `security`/`xfer-out` categories with the client address it saw.

## Gotchas
- `transfer-source` binds TCP connections for inbound transfers and is also the source for refresh (SOA) queries and forwarded dynamic updates; if unset, the system chooses (usually the interface closest to the remote end). The address must be allowed by the remote end's `allow-transfer`.

## Verify
- [ ] Primary logs show transfers from the configured source and secondaries accept NOTIFY without refusals.

## Checked

Date: 2026-10-26. BIND 9 ARM and man-page sources in isc-projects/bind9 (main, 9.21 development line, latest tag v9.21.27; grammar cross-checked on bind-9.20), read on 2026-10-26. Confirmed: transfer-source/-v6 and notify-source/-v6 semantics and per-zone/view overrides, remote-servers grammar with source, transfers-in/out/per-ns defaults. Removed unconfirmed log message text, the port advice and start-up behaviour claim.

Method: documentation only; no commands were run.
