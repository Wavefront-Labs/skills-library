---
id: computing-software.data-engineering.apache-nifi.provenance-repository-settings
name: provenance-repository-settings
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, provenance-repository, retention, indexing, nifi-properties]
level: practitioner
status: docs-checked
description: "Provenance repository keys and defaults: WriteAheadProvenanceRepository, 30 days / 10 GB retention, rollover size, index threads and shard size, indexed fields, attribute length."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Provenance repository

Defaults listed in the admin guide:
- `nifi.provenance.repository.implementation`: `org.apache.nifi.provenance.WriteAheadProvenanceRepository`
- `.directory.default`: `./provenance_repository`
- `.max.storage.time`: 30 days; `.max.storage.size`: 10 GB
- `.rollover.size`: 100 MB; `.rollover.time`: 10 mins (persistent implementation only)
- `.query.threads` 2; `.index.threads` 2; `.concurrent.merge.threads` 2
- `.index.shard.size`: 500 MB
- `.compress.on.rollover`: true; `.always.sync`: false
- `.indexed.fields`: EventType, FlowFileUUID, Filename, ProcessorID
- `.indexed.attributes`: blank (add attributes you search often)
- `.max.attribute.length`: 65536
- `.warm.cache.frequency`: blank (disabled)
- `.journal.count` 16 (persistent only); `.buffer.size` 100000 (volatile only)

Verify: the provenance search in the UI returns recent events and disk use stays within max.storage.size.

## Checked

Confirmed in the NiFi Administration Guide Provenance Repository sections (Write Ahead, Persistent and Volatile property tables): default implementation, directory.default, max.storage.time 30 days and size 10 GB, rollover size 100 MB, rollover.time 10 mins and journal.count 16 in the Persistent table, query/index/merge threads 2, shard size 500 MB, compress.on.rollover, always.sync, indexed fields and attributes defaults, max.attribute.length 65536, warm cache blank, and buffer.size 100000 in the Volatile table. Nothing was removed.

Method: docs-only read of cited pages, 2026-11-08
