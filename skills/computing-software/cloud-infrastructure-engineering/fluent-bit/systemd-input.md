---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.systemd-input
name: systemd-input
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, systemd, journald, journal, systemd-filter, input]
level: practitioner
status: docs-checked
description: "Collect journald logs with the systemd input, filter by unit, and track the journal cursor."
sources: ["https://docs.fluentbit.io/manual/pipeline/inputs/systemd"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Systemd input

The `systemd` input reads log messages from the `journald` daemon on Linux.

| Key | Default | Meaning |
| --- | --- | --- |
| `db` | none | absolute path of a database file that keeps the journald cursor |
| `db.sync` | `full` | SQLite synchronisation method: `extra`, `full`, `normal` or `off` |
| `path` | none | journal directory; if unset, default local-only paths are used |
| `read_from_tail` | `false` | start reading new entries and skip those already stored in journald |
| `max_entries` | `5000` | maximum entries processed per round, to avoid delays and reduce memory use when the journal holds many entries at startup |
| `max_fields` | `8000` | maximum fields (keys) per record |
| `lowercase` | `false` | lowercase the journald field names |
| `strip_underscores` | `false` | remove the leading underscore, so `_PID` becomes `PID` |
| `systemd_filter` | none | match `KEY=VALUE` such as `_SYSTEMD_UNIT=docker.service`; may be specified multiple times |
| `systemd_filter_type` | `or` | `and` or `or` when `systemd_filter` is repeated: `and` needs all filters to match, `or` any |
| `threaded` | `false` | run this input in its own thread |

A wildcard in `tag` expands to the unit name (`_SYSTEMD_UNIT`), so `host.*` becomes `host.UNIT_NAME`, or `host.unknown` when the unit is absent.

```yaml
pipeline:
  inputs:
    - name: systemd
      tag: host.*
      systemd_filter: _SYSTEMD_UNIT=docker.service
      db: /var/lib/fluent-bit/systemd.db
  outputs:
    - name: stdout
      match: '*'
```

The same filter from the command line:

```shell
fluent-bit -i systemd -p systemd_filter=_SYSTEMD_UNIT=docker.service -p tag='host.*' -o stdout
```

For namespaces see `computing-software.cloud-infrastructure-engineering.fluent-bit.systemd-journal-namespaces`.

## Checked

Method: docs-checked 2026-11-09 against the Fluent Bit docs systemd input page (raw markdown, read in full).
