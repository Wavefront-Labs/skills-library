---
id: computing-software.systems-network-administration.coredns.coredns-auto-plugin
name: coredns-auto-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, auto, zone-files, directory, reload]
level: practitioner
status: docs-checked
description: "Load every zone file from a directory with auto, derive origins from file names by regex and rescan periodically."
sources:
  - https://coredns.io/plugins/auto/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick up new zone files without a restart.

Syntax:

```
auto [ZONES...] {
    directory DIR [REGEXP ORIGIN_TEMPLATE]
    reload DURATION
}
```

- `directory` loads zones from DIR. A file name that matches REGEXP gives the origin through ORIGIN_TEMPLATE, where `{1}` is the first match. Default: `db\.(.*)  {1}`, so `db.example.com` becomes origin `example.com`. REGEXP must not exceed 10000 characters and is unanchored; use `^` and `$` (e.g. `^(.*)\.zone$`) to avoid matching backups like `example.org.zone.bak`.
- `reload` is the interval at which the directory is scanned for added or removed files; default one minute; `0` disables scanning. 30s checks every 30 seconds and reloads zones whose serial changed.

New or changed zones are picked up only when the SOA serial changes. If zones are not updated via transfer, bump the serial manually.

Caveat: auto loads all zones found, even ones it is not authoritative for. With `auto example.org`, a file for example.COM is loaded but never queried.

All file plugin directives are supported. Use the root plugin for the zone location and transfer for outgoing transfers.

Example matching `www.db.example.org`:

```
org {
    auto {
        directory /path/to/zones/org www\.db\.(.*) {1}
        reload 45s
    }
}
```

## Checked

2026-11-03. Page read: https://coredns.io/plugins/auto/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: nothing.

Method: documentation only; no commands were run.
