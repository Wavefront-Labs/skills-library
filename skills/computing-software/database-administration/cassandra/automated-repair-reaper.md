---
id: computing-software.database-administration.cassandra.automated-repair-reaper
name: automated-repair-reaper
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, cassandra-reaper, repair-scheduling, subrange-repair, nosql, wide-column, cql]
level: practitioner
status: draft
description: "Reaper and scheduling"
sources: ["https://cassandra.apache.org/doc/latest/", "https://docs.datastax.com/en/cql/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Automated repair scheduling

Goal: automate repair.
- Cassandra Reaper schedules subrange repairs by segment and intensity (confirm project status).
- Complete a full pass within `gc_grace_seconds` minus a margin to prevent zombie data.
- Pause during peaks; watch pending compactions.
- Built-in automatic repair is in development for 5.x (confirm).
Verify: Reaper reports all ranges repaired within window.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
