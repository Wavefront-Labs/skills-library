---
id: computing-software.data-engineering.apache-nifi.content-repository-archive
name: content-repository-archive
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, content-repository, archive, disk-usage, nifi-properties]
level: practitioner
status: docs-checked
description: "Content repository keys: FileSystemRepository, directory, appendable claim size 50 KB, archive retention 7 days, 50 percent usage cap, backpressure percentage, cleanup frequency."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Content repository

- `nifi.content.repository.implementation`: `org.apache.nifi.controller.repository.FileSystemRepository`
- `nifi.content.repository.directory.default`: `./content_repository` (more locations can be added with the `nifi.content.repository.directory.` prefix and a unique suffix, for example `directory.content1`)
- `nifi.content.claim.max.appendable.size`: 50 KB; many small FlowFiles are appended to one file up to this threshold (too small hurts performance, too large keeps data on disk longer because a file is deleted only when no FlowFile points to it)
- `nifi.content.repository.archive.enabled`: true
- `nifi.content.repository.archive.max.retention.period`: 7 days
- `nifi.content.repository.archive.max.usage.percentage`: 50%
- `nifi.content.repository.archive.backpressure.percentage`: when unset, derived as 2% greater than the max usage percentage; at this disk usage the repository refuses writes until the archive delete brings usage below the max usage percentage
- `nifi.content.repository.archive.cleanup.frequency`: 1 Second (lower not allowed)
- `nifi.content.repository.always.sync`: false

Archiving lets the provenance UI view or replay content that is no longer in a queue. Archived data is removed when the retention period passes or disk usage reaches the max usage percentage; if the archive is empty and usage is above that percentage, archiving is temporarily disabled until usage drops below it.

Verify: archive size stays under the configured percentage of the disk during a load test.

## Checked

Confirmed in the NiFi Administration Guide, File System Content Repository Properties: implementation class, directory.default and the directory prefix for extra locations, appendable claim size 50 KB, archive enabled by default, retention 7 days, max usage 50%, backpressure percentage and its derived default, cleanup frequency 1 Second with lower values not allowed, always.sync false. The unsupported statement about what happens to content when archiving is disabled was removed.

Method: docs-only read of cited pages, 2026-11-08
