---
id: computing-software.data-engineering.apache-nifi.status-history-repository
name: status-history-repository
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, status-history, questdb, nifi-properties, monitoring]
level: practitioner
status: docs-checked
description: "Component status history storage: volatile in-memory default versus EmbeddedQuestDbStatusHistoryRepository, snapshot frequency, buffer size and persistence days."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Status history repository

- `nifi.components.status.repository.implementation`: default `org.apache.nifi.controller.status.history.VolatileComponentStatusRepository` (memory, lost on restart). `EmbeddedQuestDbStatusHistoryRepository` persists to disk.
- `nifi.components.status.snapshot.frequency`: 1 min
- `nifi.components.status.repository.buffer.size`: 1440 (in-memory option)
- `nifi.status.repository.questdb.persist.node.days`: 14
- `nifi.status.repository.questdb.persist.component.days`: 3
- `nifi.status.repository.questdb.persist.location`: `./status_repository`

At one snapshot per minute a 1440 entry buffer covers about a day (arithmetic on the defaults).

Verify: after restart with the QuestDB option, status history charts still show pre-restart points.

## Checked

Confirmed in the NiFi Administration Guide, Status History Repository table: implementation default and the QuestDB option, snapshot frequency 1 min, buffer size 1440, persist node days 14, component days 3, persist location. The claim about the UI showing 24 hours by default was removed because the guide does not state it.

Method: docs-only read of cited pages, 2026-11-08
