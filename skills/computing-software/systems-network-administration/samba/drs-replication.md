---
id: computing-software.systems-network-administration.samba.drs-replication
name: drs-replication
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, drs-replication, showrepl, kcc, samba-tool, replication, sites]
level: advanced
status: docs-checked
description: "Check and drive Samba AD replication with samba-tool drs showrepl, replicate, kcc and uptodateness, plus samba-tool sites and fsmo show."
sources:
  - https://www.samba.org/samba/docs/current/man-html/samba-tool.8.html
  - https://wiki.samba.org/index.php/Joining_a_Samba_DC_to_an_Existing_Active_Directory
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# drs replication
```
samba-tool drs showrepl [--json] [--summary]
samba-tool drs replicate DEST_DC SOURCE_DC NC
samba-tool drs kcc
samba-tool drs uptodateness [-H URL] [-p PARTITION] [--json] [--maximum] [--median] [--full]
samba-tool drs options
samba-tool drs clone-dc-database DNSDOMAIN --targetdir=DIR
samba-tool fsmo show
```
Examples:
- `samba-tool drs showrepl --summary`
- `samba-tool drs replicate dc2 dc1 CN=Schema,CN=Configuration,DC=samdom,DC=test`

After a new DC joins, confirm DomainDnsZones and ForestDnsZones show successful inbound replication; the KCC can take up to 15 minutes to build connections. Start BIND (DLZ) only after those partitions replicate.

Sites: `samba-tool sites list|view|create|remove`, `samba-tool sites subnet list|view|create|remove|set-site` (for example `sites subnet create SUBNET SITE`).

Checks: create a user on one DC and confirm it appears on another; `samba-tool ldapcmp` compares directories (the Samba wiki notes the attributes `msDs-masteredBy`, `msDS-NC-Replica-Locations` and `msDS-hasMasterNCs` have been changed).

FSMO: `samba-tool fsmo transfer` and `samba-tool fsmo seize` exist; the man page lists only their existence, so check `--help` for the role options.

## Checked

2026-11-04. Confirmed against the samba-tool(8) manual page: drs showrepl (--json, --summary), replicate, kcc, uptodateness options, options, clone-dc-database, fsmo show/transfer/seize, sites and sites subnet subcommands, ldapcmp. Confirmed against the Samba wiki join and troubleshooting pages: 15 minute KCC delay, verify DNS partitions before starting BIND, user-creation test, ldapcmp attribute note. Reworded the fsmo gotcha.
Method: documentation only; no commands were run.
