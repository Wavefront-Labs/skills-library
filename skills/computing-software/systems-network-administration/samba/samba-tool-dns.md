---
id: computing-software.systems-network-administration.samba.samba-tool-dns
name: samba-tool-dns
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, samba-tool-dns, zonecreate, dns-records, samba-tool, dns]
level: practitioner
status: docs-checked
description: "Manage Samba AD DNS with samba-tool dns: add, delete, query, update records, create and list zones, zoneoptions aging, and cleanup of a host's records."
sources:
  - https://www.samba.org/samba/docs/current/man-html/samba-tool.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# samba tool dns
Syntax (SERVER is a DC name or IP; add `-U Administrator` for credentials):
```
samba-tool dns add SERVER ZONE NAME A|AAAA|PTR|CNAME|NS|MX|SRV|TXT DATA [--allow-existing]
samba-tool dns delete SERVER ZONE NAME TYPE DATA
samba-tool dns update SERVER ZONE NAME TYPE OLDDATA NEWDATA
samba-tool dns query SERVER ZONE NAME TYPE|ALL
samba-tool dns zonecreate SERVER ZONE
samba-tool dns zonedelete SERVER ZONE
samba-tool dns zonelist SERVER
samba-tool dns zoneinfo SERVER ZONE
samba-tool dns serverinfo SERVER
samba-tool dns roothints SERVER [NAME]
samba-tool dns cleanup SERVER NAME
```
Examples:
- `samba-tool dns add dc1 samdom.test web A 10.0.0.25` (illustrative zone, host and address)
- `samba-tool dns cleanup dc1 computer.samdom.test.site` marks a host's records as deleted.

`dns zoneoptions SERVER ZONE` controls aging: `--aging=0|1`, `--refreshinterval=HOURS`, `--norefreshinterval=HOURS`, `--mark-old-records-static=YYYY-MM-DD`, `--mark-records-static-regex`, `--mark-records-dynamic-regex`, and `-n/--dry-run` to preview.

Reverse zones are created manually (`zonecreate ... 0.99.10.in-addr.arpa`) and PTRs added by hand.

Gotcha: the page lists no per-subcommand option details beyond these; run `samba-tool dns <cmd> --help` for the rest.

## Checked

2026-11-04. Confirmed against the samba-tool(8) manual page: every dns subcommand and record type list, --allow-existing, cleanup and its example, and all zoneoptions options including -n/--dry-run. Reverse-zone creation is by hand per the Samba wiki DC setup page (zonecreate and dns add PTR).
Method: documentation only; no commands were run.
