---
id: computing-software.systems-network-administration.samba.ad-dc-troubleshooting
name: ad-dc-troubleshooting
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, ad-dc-troubleshooting, dbcheck, join-errors, replication, dns]
level: advanced
status: docs-checked
description: "Diagnose Samba AD DC problems: process checks, interactive run, DNS zone errors during a join and the NONE-backend workaround, dbcheck, known errors."
sources:
  - https://wiki.samba.org/index.php/Samba_AD_DC_Troubleshooting
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ad dc troubleshooting
Basics:
- `ps axf | egrep "samba|smbd|winbindd"` (all children of one `samba`; no `nmbd` on a DC).
- `samba -i` runs interactively with output on screen.
- `samba-tool dbcheck --cross-ncs` corrects discrepancies in the creation of the partitions (used in the join workaround below).

Workaround for DNS zone errors during a join (order matters):
1. Join with `--dns-backend=NONE`.
2. `samba-tool drs replicate <local DC> <source DC> DC=ForestDnsZones,<base DN> --local --full-sync`; repeat for `DC=DomainDnsZones`.
3. Run `samba_upgradedns` against the new DC database.
4. `samba-tool dbcheck --cross-ncs`.
5. Optionally `samba-tool ldapcmp`.

Known errors:
- `WERR_DNS_ERROR_RCODE_NAME_ERROR` during join: known bug in 4.7+ (Bugzilla 13298).
- `WERR_DNS_ERROR_ZONE_DOES_NOT_EXIST`: often a domain migrated from Windows 2000/2003 with zones not moved correctly; only ForestDnsZones and DomainDnsZones are supported.
- Join fails on Rocky Linux 8 (likely RHEL/Alma): FIPS mode reported to block it; disable FIPS on all RHEL-based DCs, reboot, retry.
- After an update: read Notable Enhancements and Changes in the wiki's Updating Samba page.
- `net` cannot reach 127.0.0.1: see member troubleshooting (listen on loopback or pass `-I`/`-S`).

Raise logging with log-levels; check ports in ad-dc-ports.

## Checked

2026-11-04. Confirmed against the Samba wiki page Samba AD DC Troubleshooting: ps check and child-process rule, no nmbd on a DC, samba -i, the four-step order-sensitive workaround and optional ldapcmp, rcode name error (bug 13298, 4.7+), zone-does-not-exist cause, Rocky Linux 8 FIPS note, updating pointer, 127.0.0.1 net pointer. Narrowed the dbcheck line to what the page states.
Method: documentation only; no commands were run.
