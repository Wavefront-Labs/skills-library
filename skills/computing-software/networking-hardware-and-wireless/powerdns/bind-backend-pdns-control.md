---
id: computing-software.networking-hardware-and-wireless.powerdns.bind-backend-pdns-control
name: bind-backend-pdns-control
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, bind-backend, pdns-control, bind-add-zone, rediscover, bind-domain-status, reload]
level: practitioner
status: docs-checked
description: "Use the pdns_control commands specific to the BIND backend: bind-add-zone, bind-domain-status, bind-reload-now, bind-list-rejects, rediscover, reload."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/backends/bind.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BIND backend pdns_control commands

- `pdns_control bind-add-zone <domain> <filename>`: adds a zone from a file, loaded on first request. It does not edit the `bind-config` file, so the zone is lost on restart unless you add it there.
- `pdns_control bind-domain-status [domain ...]`: reports one of "seen in named.conf, not parsed", "parsed successfully at <time>", or "error parsing at line ... at <time>".
- `pdns_control bind-domain-extended-status [domain ...]`: detailed status per domain: loaded record count, primary or secondary role, primaries and timers (4.3.0+).
- `pdns_control bind-list-rejects`: lists zones with problems and the problem for each.
- `pdns_control bind-reload-now <domain>`: reloads that zone from disk immediately and reports the result.
- `pdns_control rediscover`: rereads `named.conf`. New zones are read and removed zones are dropped from memory. If parsing fails, the old configuration stays active and the error is reported.
- `pdns_control reload`: zones whose timestamp changed are reloaded when their next query arrives.

Related: with `bind-check-interval=0` no checks for changed zone files are performed until `pdns_control reload` is issued.

## Checked

2026-11-04. Read the pdns_control commands section of backends/bind.rst and confirmed each command, the 4.3.0 gate on extended status and the status strings. Replaced an over-strong claim that reload or bind-reload-now is the only way to pick up changes with the page's wording about check-interval 0.

Method: documentation only; no commands were run.
