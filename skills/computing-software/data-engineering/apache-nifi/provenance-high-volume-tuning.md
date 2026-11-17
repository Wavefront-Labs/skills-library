---
id: computing-software.data-engineering.apache-nifi.provenance-high-volume-tuning
name: provenance-high-volume-tuning
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, provenance-repository, write-ahead, tuning, bootstrap]
level: advanced
status: docs-checked
description: "Switch provenance to WriteAheadProvenanceRepository and tune shard size, index threads and rollover size for high volume, with the G1 bootstrap note and no-rollback warning."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/user-guide.html
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# High-volume provenance tuning

The user guide's Write Ahead Provenance Repository section lists these changes when moving off `org.apache.nifi.provenance.PersistentProvenanceRepository` (the admin guide now makes Write Ahead the default and calls Persistent deprecated):
- Set the implementation to `org.apache.nifi.provenance.WriteAheadProvenanceRepository`.
- The guide cites defaults of 24 hours for `max.storage.time` and 1 GB for `max.storage.size` (the admin guide lists 30 days and 10 GB; check your version's file).
- `index.shard.size`: raise from 500 MB to 4 GB (the admin guide advises 4 to 8 GB for production and says it should be no more than half of `max.storage.size`).
- `index.threads`: raise from 2 to 4 or 8.
- `rollover.size`: raise from 100 MB to 1 GB if processing a high volume of events.
- `concurrent.merge.threads` defaults to 2; `warm.cache.frequency` blank (disabled).
- `journal.count` does not apply to Write Ahead.
- In bootstrap.conf the guide recommends commenting out `java.arg.13=-XX:+UseG1GC` (it says Java 8 bugs may surface more often with Write Ahead and G1).

Warning: once switched to Write Ahead you cannot go back to Persistent without first deleting the data in the Provenance Repository. Restart NiFi after the property changes.

Verify: provenance searches stay responsive under load and the old repository data decision was made before the switch.

## Checked

Confirmed in the NiFi User Guide section Write Ahead Provenance Repository (implementation class names, backwards compatibility warning, bootstrap.conf line, journal.count not relevant, merge threads 2 and warm cache blank, max.storage.time 24 hours and max.storage.size 1 GB as cited there, shard size 500 MB to 4 GB, index threads 2 to 4 or 8, rollover size 100 MB to 1 GB) and in the Administration Guide Write Ahead properties (30 days, 10 GB, 4 to 8 GB shard advice, Write Ahead as default). No claims were removed.

Method: docs-only read of cited pages, 2026-11-08
