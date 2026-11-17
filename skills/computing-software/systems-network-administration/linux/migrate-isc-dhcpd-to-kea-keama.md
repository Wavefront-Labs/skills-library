---
id: computing-software.systems-network-administration.linux.migrate-isc-dhcpd-to-kea-keama
name: migrate-isc-dhcpd-to-kea-keama
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, keama, dhcp-migration, kea, isc-dhcp-eol, kea-dhcp4, lease-migration]
level: practitioner
status: docs-checked
description: "Migrate from end-of-life ISC dhcpd to Kea: translate dhcpd.conf with keama, review the output, carry over reservations and leases, and cut over without duplicate offers."
sources:
  - https://github.com/isc-projects/dhcp/blob/master/keama/keama.8
  - https://gitlab.isc.org/isc-projects/keama/-/blob/master/README.md
  - https://github.com/isc-projects/kea/blob/master/doc/sphinx/arm/classify.rst
  - https://github.com/isc-projects/kea/blob/master/doc/sphinx/arm/dhcp4-srv.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Migrate ISC dhcpd to Kea (keama)

ISC DHCP is end of life (4.4.3-P1, October 2022, is the final release). Kea is its replacement with JSON config, hooks and a REST control channel.

## 1. Translate with keama
```bash
keama -4 -i /etc/dhcp/dhcpd.conf -o kea-dhcp4.json      # -6 for dhcpd6.conf
```
Other options from keama(8): `-N` puts host reservations in the matching subnet instead of globally, `-r perform|fatal|pass` chooses what to do with hostnames, `-D` defines the ISC DHCP lifetime defaults; the man page's synopsis and option list disagree on the hook library path flag (`-l` or `-p`), so read the installed man page. The exit status is the number of conversion failures, and any parse warning in the input is fatal, so fix the dhcpd.conf first.
Where keama cannot translate something it inserts messages (referencing issues in the Kea GitLab) at that spot in the output. Read the whole file for them; those sections need manual work. Group and logic statements translate only when first converted to a class.

## 2. Review what usually needs hand work
| dhcpd feature | Kea equivalent |
|---|---|
| `class`/`match if` expressions | `client-classes` with `test` expressions (different syntax) |
| `on commit` execute scripts / DDNS hooks | `kea-dhcp-ddns` + `libdhcp_run_script.so` |
| `failover peer` | HA hook (`libdhcp_ha.so`) |
| `host` blocks in `group` | `reservations` per subnet (or global with `reservations-global`) |
| `option space` vendor options | `option-def` + `option-data` |
| `deny unknown-clients` | pool with `client-class "KNOWN"` |
Set `"valid-lifetime"`, `"interfaces-config"` and `"lease-database": {"type":"memfile","lfc-interval":3600}` explicitly.

## 3. Validate
```bash
kea-dhcp4 -t kea-dhcp4.json     # syntax and semantic check
```

## 4. Leases
Kea does not read `dhcpd.leases` directly. The companion tool `keama-leases` takes the lease file as its parameter and writes Kea memfile output (options `-v` print to stdout, `-d` debug, `-e` override expiration time); only the last entry per lease matters and other lease-file information is not migrated. ISC DHCP has no subnet IDs, so set `"lease-checks": "fix-del"` in the Kea `sanity-checks` so Kea corrects them. Alternatively let clients renew. The memfile default is `kea-leases4.csv` under the Kea `var/lib/kea` directory. Static reservations carry over via keama.

## 5. Cut over
1. Lower lease time on dhcpd a day ahead (e.g. 1 h) so clients renew soon after the change.
2. Stop and disable `isc-dhcp-server`; start `kea-dhcp4`. **Never** run both on the same segment: duplicate offers and conflicts.
3. Relays (`ip helper-address`) keep pointing at the same IP, or update them.
4. Watch `journalctl -u kea-dhcp4` for `DHCP4_LEASE_ALLOC` and `DHCP4_PACKET_DROP_*` messages.

## Verify
- [ ] `kea-dhcp4 -t` passes; reserved hosts receive their fixed addresses.
- [ ] `perfdhcp -4 -r 10 -R 100 <server>` or a test client gets offers with the right options (router, DNS, domain).

## Checked

Checked 2026-10-26 against keama.8 (isc-projects/dhcp keama/), the keama README on gitlab.isc.org, and the Kea ARM (isc-projects/kea master, last commit 2026-10-21). Confirmed: keama options (-4/-6, -i, -o, -N, -r, -D; the man page disagrees with itself on -l versus -p for the hook path), untranslatable constructs are marked in the output, keama-leases exists for lease conversion (so Kea can read converted leases), the ISC DHCP end-of-life notice, reservations-global, test expressions and KNOWN class, lfc-interval default, memfile default file name, kea-dhcp4 -t, perfdhcp -r and -R, DHCP4_PACKET_DROP_NNNN message names. Corrected: leases can be converted with keama-leases; removed the invented dhcp.isc.org web front end, grep for unsupported markers and CSV column list.

Method: documentation only; no commands were run.
