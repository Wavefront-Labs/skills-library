---
id: computing-software.networking-hardware-and-wireless.powerdns.pdnsutil-zone-management
name: pdnsutil-zone-management
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, pdnsutil, zone-create, zone-load, zone-edit, set-kind, create-secondary, check-all]
level: practitioner
status: docs-checked
description: "pdnsutil zone management commands: create, load, edit, copy, clear, delete, list, set-kind, create-secondary, check, increase-serial."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/manpages/pdnsutil.1.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pdnsutil zone management

Global options: `-v`, `-f`, `-q`, `-s`, `--config-name <NAME>`, `--config-dir <DIR>` (default `/etc/powerdns`).

- `zone create ZONE`: empty zone. `zone delete ZONE`: remove it.
- `zone load ZONE FILE`: replaces records atomically, or creates the zone.
- `zone edit ZONE`: edit in zonefile format in `$EDITOR`.
- `zone copy ZONE NEW-ZONE`: copies records, comments, metadata and keys within the same backend; options and catalog membership are not copied.
- `zone clear ZONE`: delete records but keep the zone and settings.
- `zone list ZONE`: show records; `-s` sorts by name (slow on large zones).
- `zone list-all [KIND]`: active zones of KIND (primary, secondary, native, producer, consumer); `-v` adds disabled or empty ones.
- `zone set-kind ZONE KIND`, `zone set-account ZONE ACCOUNT`.
- `zone check ZONE`, `zone check-all [exit-on-error]`.
- `zone increase-serial ZONE`: adds 1 via SOA-EDIT.
- `zone set-option ZONE [producer|consumer] [coo|unique|group] VALUE...`: empty value removes; `zone set-options-json ZONE JSONFILE` replaces all options.
- `zone zonemd-verify-file ZONE FILE`: validate ZONEMD.

Secondary zones (primaries are space-separated IPs with optional port):
- `zone create-secondary ZONE PRIMARY...`
- `zone change-primary ZONE PRIMARY...`

## Checked

2026-11-08. Read docs/manpages/pdnsutil.1.rst in full. Confirmed the global options, every zone and secondary-zone command with its argument form and behaviour. Removed the closing sentence listing pre-5.0 flat command names, which this page does not state. Description shortened.

Method: documentation only; no commands were run.
