---
id: computing-software.systems-network-administration.dns-dhcp.bind-primaries-lists
name: bind-primaries-lists
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, bind, primaries-statement, secondary-zones, notify, also-notify]
level: practitioner
status: verified
description: "Use BIND primaries lists (formerly masters) to define reusable groups of primary servers with ports and TSIG keys for secondaries and notify targets."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://github.com/isc-projects/bind9/blob/main/lib/isccfg/namedconf.c
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# primaries lists

`primaries` replaces the older `masters` keyword (still accepted). The documented top-level statement for a reusable named list is `remote-servers`; the parser also still accepts a top-level `primaries "name" { ... };` (and `masters`) as an undocumented alias, so prefer `remote-servers` in new configs. A named list avoids repeating server addresses and keys in every zone.

## Definition
```
key "xfr-key" { algorithm hmac-sha256; secret "base64..."; };

remote-servers "dc1-primaries" {
    192.0.2.53 key "xfr-key";
    2001:db8::53 key "xfr-key";
};
remote-servers "all-primaries" { "dc1-primaries"; 198.51.100.53 port 5353; };
```
Lists can nest other lists and set `port`, `key` and `tls` per entry (`remote-servers <name> [port N] [source ...] { ... }`). TLS to primaries is unauthenticated unless the referenced `tls` block sets `remote-hostname` or `ca-file`.

## Use in zones
```
zone "example.com" { type secondary; primaries { "all-primaries"; }; file "sec/example.com.db"; };
```
The `primaries`, `also-notify` and `parental-agents` options all accept a list name. Catalog zones can set `default-primaries`.

## Notify targets
`also-notify { "list-name"; };` accepts a named list too, reusing the same definitions for the primary's NOTIFY destinations (default is an empty list).

## Order and failover
The primary servers are queried in turn; named moves to the next server if it gets no valid response or the primary returns the same or a smaller SOA serial than the secondary is serving. Put the preferred server first.

## Gotchas
- Key per entry must also be allowed on the primary (`allow-transfer { key "xfr-key"; };`).
- A list entry that is unreachable delays failover to the next entry; order matters.

## Verify
- [ ] `rndc retransfer example.com` succeeds and logs show the transfer from the expected primary with the expected key.

## Checked

Date: 2026-10-26. BIND 9 ARM sources in isc-projects/bind9 (main, 9.21 development line, latest tag v9.21.27, plus the bind-9.20 branch grammar), read on 2026-10-26. Confirmed in reference.rst, doc/misc/options and lib/isccfg/namedconf.c (main and bind-9.20): remote-servers grammar (port, source, key, tls), primaries/masters kept as undocumented aliases, also-notify accepting named lists, primaries query order, default-primaries in catalog-zones. The skill previously claimed a 9.20 `template` statement; it exists on main (9.21) only and is not in the 9.20 grammar, so the claim was removed.

Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container (BIND 9.20.30): `remote-servers` lists with `key` and `port` entries and a nested list accepted by named-checkconf; a secondary with `primaries { "all-primaries"; };` transferring over TSIG from the second entry after the first (a dead address) failed; the undocumented top-level `primaries "legacy" { ... };` alias accepted and used for a transfer; `also-notify { "list"; };` accepted; AXFR without the key refused, with the key succeeding. Not run: `tls` entries, `source`, catalog `default-primaries`, NOTIFY delivery, retransfer logs.
