---
id: computing-software.systems-network-administration.dns-dhcp.isc-dhcp-to-kea-with-keama
name: isc-dhcp-to-kea-with-keama
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, kea, isc-dhcp, isc-dhcp-migration, keama, keama-convert, migration-gaps, dhcpd-conf, kea-dhcp4, kea-migration-assistant, end-of-life, failover-to-ha, host-declarations, dhcp-cutover]
level: practitioner
status: gated
description: "Migrate ISC DHCP (EOL) to Kea: convert dhcpd.conf with keama, read its warnings, rework failover/classes/OMAPI/hooks by hand, and plan a parallel cutover."
sources:
  - https://www.isc.org/blogs/isc-dhcp-eol/
  - https://kb.isc.org/docs/migrating-from-isc-dhcp-to-kea-dhcp-using-the-migration-assistant
  - https://github.com/isc-projects/dhcp/tree/master/keama
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# ISC DHCP to Kea with keama

ISC announced in 2022 that it no longer maintains ISC DHCP (dhcpd); the ISC DHCP README calls it
end-of-life with 4.4.3 the final planned release. Kea is ISC's replacement with a JSON config,
REST control API, database backends and HA via hooks.

## Convert
```
keama -4 -i /etc/dhcp/dhcpd.conf -o kea-dhcp4.json      # -6 for dhcpd6.conf
keama -4 -N -i dhcpd.conf -o kea-dhcp4.json              # -N: host reservations go in the matching subnet, not global
kea-dhcp4 -t kea-dhcp4.json                              # syntax/semantic check
```
keama was not built or run here (no Windows binary and no ISC DHCP build), so the invocations above
are unconfirmed (gated: unconfirmed, source is paywalled or blocked) and everything below comes from the keama(8) man page, the keama
README and ISC's knowledge base article.

Options in the keama(8) man page: `-4` or `-6` (run it once per protocol), `-D` (define ISC DHCP
builtin min/default/max lifetimes), `-N`, `-r perform|fatal|pass` (what to do with hostnames:
resolve to their first address, fail, or pass them silently), hook-library path (the man page option list says `-p`, its synopsis says `-l`; for example
flex-id), `-i` input file and `-o` output file (stdin and stdout when omitted). The exit status is
the number of conversion failures, and any parsing warning or error in the input is fatal, so fix
the dhcpd.conf first.
The README calls keama experimental; it uses a subset of the ISC DHCP parser with many sanity checks
removed, so it can mishandle (even crash on) an invalid dhcpd.conf. For every feature it cannot
translate it emits a comment pointing at a Kea GitLab issue in the "ISC DHCP Migration"
milestone: search the output for those comments and handle each one. keama handles configurations
with multiple include files and its output is more verbose than the original. It does **not**
convert lease files (ISC's separate experimental keama-leases tool does) and does not convert host
reservations created in the lease file or through OMAPI. ISC also offers an online version at
https://dhcp.isc.org/ and a keama package in ISC's Cloudsmith repository (per the ISC knowledge
base article).

## Where the gaps are
The table below lists the usual differences; keama's comments tell you which apply to your file.

| dhcpd feature | Kea approach |
|---|---|
| `failover peer` | HA hook (`libdhcp_ha.so`) load-balancing or hot-standby; different protocol, not compatible |
| `class` with `match if` expressions | `client-classes` with Kea expression syntax (`substring(option[60].hex,0,9) == 'PXEClient'`; see isc-dhcp-class-to-kea-expression) |
| `subclass` / `spawn with` classes | Kea template classes (`template-test`, since 2.3.3 development / 2.4 stable), a flex-id reservation, or client classes per value |
| `on commit` / `execute()` scripts | Kea hooks (run_script hook) or the REST API/lease events |
| OMAPI / omshell host changes | `host_cmds` hook with a hosts database (MySQL/PostgreSQL) over the control channel; see replacing-omapi-with-kea-control-channel |
| `ddns-update-style interim` | Kea DHCP-DDNS (D2) server (separate daemon) |
| `allow/deny unknown-clients` | client classes with `KNOWN`/`UNKNOWN` built-in classes |
| `authoritative` | Kea's DHCPv4 `authoritative` setting defaults to false: by default it follows dhcpd and stays silent for INIT-REBOOT requests it knows nothing about; set `"authoritative": true` (global, shared-network or subnet) to NAK them |
| Option definitions (`option space`, vendor options) | `option-def` and `option-data` with space names |

## Cutover plan
1. Convert, rework, validate (`kea-dhcp4 -t`), review option-by-option with a diff of what clients receive.
2. Lab test with real client types (Windows, Linux, phones, PXE, VoIP phones, APs using option 43).
3. Migrate leases (see dhcp-lease-migration-to-kea; keama itself does not convert them) so clients keep their addresses.
4. Cutover window: stop dhcpd, start Kea (same IPs, or update relays' helper addresses), watch logs.
5. Keep dhcpd config and binary available for rollback for a defined period.

## Verify
- [ ] `kea-dhcp4 -t` passes with no keama comments left unresolved.
- [ ] Test clients of every class get identical options to before (capture DHCP ACKs and compare).
