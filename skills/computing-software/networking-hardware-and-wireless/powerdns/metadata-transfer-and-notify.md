---
id: computing-software.networking-hardware-and-wireless.powerdns.metadata-transfer-and-notify
name: metadata-transfer-and-notify
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, domain-metadata, allow-axfr-from, also-notify, axfr-source, slave-renotify, ixfr]
level: practitioner
status: docs-checked
description: "PowerDNS zone metadata for transfers and notify: ALLOW-AXFR-FROM, ALSO-NOTIFY, AXFR-SOURCE, IXFR, SLAVE-RENOTIFY."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/domainmetadata.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metadata for transfers and notification

With several backends, metadata is read and written in the first DNSSEC- or metadata-capable one.

- `ALLOW-AXFR-FROM`: subnet (v4 or v6) or `AUTO-NS`, one row per entry. To disallow every IP except those in metadata, add `allow-axfr-ips=` to `pdns.conf`.
- `ALSO-NOTIFY`: extra nameserver IP, optionally with port; repeatable.
- `AXFR-SOURCE`: source IP for AXFR/IXFR requests.
- `AXFR-MASTER-TSIG`: TSIG key for retrieving the zone (API read-only).
- `TSIG-ALLOW-AXFR`: key names allowed to AXFR.
- `IXFR`: `1` tries IXFR; otherwise AXFR only.
- `SLAVE-RENOTIFY`: `1` renotifies secondaries after an AXFR; unset falls back to `secondary-do-renotify` (since 4.3.0).
- `LUA-AXFR-SCRIPT`: script to edit incoming AXFRs; `NONE` cancels the global `lua-axfr-script`. API read-only.
- `X-*`: any extra metadata for outside applications; the name must start with `X-`.

Set with `pdnsutil metadata set <zone> KIND value ...`, which takes several values (`set-meta` before 5.0). Over the HTTP API, `AXFR-MASTER-TSIG` and `LUA-AXFR-SCRIPT` can only be read, not written.

## Checked

2026-11-08. Read in full: PowerDNS docs domainmetadata.rst. Confirmed the multi-backend warning, the API read-only list, ALLOW-AXFR-FROM rows and AUTO-NS, ALSO-NOTIFY with port, AXFR-SOURCE, AXFR-MASTER-TSIG, TSIG-ALLOW-AXFR, IXFR, SLAVE-RENOTIFY since 4.3.0 and its fallback setting, LUA-AXFR-SCRIPT with NONE, the X- prefix rule, and the pdnsutil metadata set command with its pre-5.0 name. Removed the per-kind API read/write claims the page does not state, the metadata add command, and the wrong default for allow-axfr-ips.

Method: documentation only; no commands were run.
