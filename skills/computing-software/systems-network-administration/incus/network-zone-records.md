---
id: computing-software.systems-network-administration.incus.network-zone-records
name: network-zone-records
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, network-zone, dns-record, ttl, record-entry]
level: practitioner
status: docs-checked
description: "Add custom DNS records to an Incus network zone: record create, record entry add/remove with --ttl (default 300), and editing whole records."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/network_zones.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom zone records

```
incus network zone record create <zone> <record_name>
incus network zone record entry add <zone> <record_name> <type> <value> [--ttl <TTL>]
incus network zone record entry remove <zone> <record_name> <type> <value>
incus network zone record edit <zone> <record_name>
```

- Default TTL is 300 seconds.
- Entries cannot be edited in place: remove and re-add, or edit the whole record.
- Record properties: `name` (required), `description`, `entries`, `config` (`user.*` keys only).

## Checked

2026-11-04: confirmed against the Incus network zones how-to (record create, entry add/remove with `--ttl`, 300 second default, record properties, entries not editable except via record edit). Nothing removed.

Method: documentation only; no commands were run.
