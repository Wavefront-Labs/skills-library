---
id: computing-software.networking-hardware-and-wireless.powerdns.autoprimary-autosecondary
name: autoprimary-autosecondary
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, autoprimary, autosecondary, supermaster, notify, pdnsutil]
level: practitioner
status: docs-checked
description: "Let PowerDNS create secondary zones automatically: enable autosecondary, register autoprimaries with pdnsutil, NOTIFY requirements, account field and caveats."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/modes-of-operation.rst
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/backends/bind.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Autoprimary and autosecondary

Previously called supermaster (before 4.5.0). Enable `autosecondary` in `pdns.conf`.

Register a trusted primary: `pdnsutil autoprimary add` (`add-autoprimary` before 5.0), or insert into the database table directly.

A NOTIFY for an unknown zone is accepted only if:
- the autoprimary answers with an SOA for the domain;
- its IP is in the secondary's `supermasters` table with a name that appears in the zone's NS set;
- the NS set retrieved from it includes that name;
- if the NOTIFY is TSIG signed, that key is used for retrieval; with `allow-unsigned-autoprimary` off, NOTIFYs must be signed.

The optional `account` field is for tracking; if several autoprimaries match by name their accounts must be identical.

Caveats:
- The bootstrap SOA and NS queries are non-recursive and must reach the authoritative server directly, not via a recursor (dnsdist forwarding is fine).
- Removing a zone must be done on each secondary; the primary cannot signal it.
- If the primary is PowerDNS with DNSSEC, rectify after every change, or the SOA requirement fails.
- BIND backend autoprimary support is experimental (the settings were named `bind-supermasters`, `bind-supermaster-config` and `bind-supermaster-destdir` before 4.9.0). `bind-autoprimaries` is a file with one IP and account per line that the backend only reads, and it checks only the primary's IP. `bind-autoprimary-config` receives a zone entry written by the backend for each new zone, so `bind-config` should `include` it. `bind-autoprimary-destdir` receives each new zone's file and must be writable.

## Checked

2026-11-04. Read the autoprimary section of modes-of-operation.rst and the autoprimary settings of backends/bind.rst. Confirmed the NOTIFY acceptance conditions, account behaviour, non-recursive bootstrap queries, removal note and rectify warning. Corrected the BIND backend caveat: only bind-autoprimaries is read-only; bind-autoprimary-config is written by the backend and bind-autoprimary-destdir receives zone files. Added the BIND backend page to sources.

Method: documentation only; no commands were run.
