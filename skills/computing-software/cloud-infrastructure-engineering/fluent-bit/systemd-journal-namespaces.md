---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.systemd-journal-namespaces
name: systemd-journal-namespaces
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, systemd, journal-namespaces, libsystemd, db, cursor]
level: advanced
status: docs-checked
description: "Read a journald namespace with the systemd input and keep a separate cursor database per namespace."
sources: ["https://docs.fluentbit.io/manual/pipeline/inputs/systemd"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Journal namespaces

systemd can partition the journal into namespaces, where a separate `systemd-journald` instance keeps its own log storage for a set of units. Set `namespace` on the `systemd` input to read one instead of the default journal.

Rules:
- Only the named namespace is read. Entries in the default journal are not collected; to collect both, define a separate `systemd` input for each.
- `namespace` and `path` are mutually exclusive. Setting both logs `path and namespace are mutually exclusive` and Fluent Bit fails to start.
- The binary must be built against `libsystemd` 245 or later, where `sd_journal_open_namespace` was introduced. Otherwise it logs `namespace requires libsystemd >= 245` and fails to start; use `path` instead on those builds.
- When you use `db` to track the cursor, give each namespace its own database file. Reusing one makes a cursor the other namespace cannot seek to, and the plugin logs a `seek_cursor failed` warning and starts over.

```yaml
pipeline:
  inputs:
    - name: systemd
      tag: host.*
      namespace: logging
      db: /var/lib/fluent-bit/systemd-logging.db
  outputs:
    - name: stdout
      match: '*'
```

## Checked

Method: docs-checked 2026-11-09 against the Fluent Bit docs systemd input page (raw markdown, read in full).
