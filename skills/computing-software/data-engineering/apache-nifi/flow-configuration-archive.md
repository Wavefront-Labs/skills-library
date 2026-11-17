---
id: computing-software.data-engineering.apache-nifi.flow-configuration-archive
name: flow-configuration-archive
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, flow-json, flow-archive, nifi-properties, backup]
level: practitioner
status: docs-checked
description: "NiFi flow persistence keys: flow.json.gz location, legacy flow.xml.gz, archive enabled, directory, max time (30 days) and max storage (500 MB), plus related defaults."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flow configuration and archive

- `nifi.flow.configuration.json.file`: `./conf/flow.json.gz`
- `nifi.flow.configuration.file`: `./conf/flow.xml.gz` (legacy; used only if the JSON file is absent)
- `nifi.flow.configuration.archive.enabled`: true
- `nifi.flow.configuration.archive.dir`: `./conf/archive`
- `nifi.flow.configuration.archive.max.time`: unset, falls back to 30 days
- `nifi.flow.configuration.archive.max.storage`: unset, falls back to 500 MB
- `nifi.flow.configuration.archive.max.count`: no default stated; if set, only the latest N archives are kept
- `nifi.flowcontroller.autoResumeState`: true
- `nifi.flowcontroller.graceful.shutdown.period`: 10 secs
- `nifi.flowservice.writedelay.interval`: 500 ms
- `nifi.templates.directory`: `./conf/templates`

NiFi names automatic archives with an ISO 8601 style timestamp prefix before the original filename and cleans only files matching that pattern; to keep a particular archive, copy it under a different filename pattern.

Verify: after a flow change a new timestamped file appears in the archive directory.

## Checked

Confirmed in the NiFi Administration Guide, Core Properties: flow.json.gz and legacy flow.xml.gz behaviour, archive enabled/dir/max.time/max.storage/max.count with the 30 days and 500 MB fallbacks, autoResumeState, graceful shutdown period 10 secs, write delay 500 ms, templates directory. The unsupported advice to back up the conf directory was removed.

Method: docs-only read of cited pages, 2026-11-08
