---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.interpreting-registry-key-last-write-times
name: interpreting-registry-key-last-write-times
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [key-last-write-time, windows-registry, registry, timeline, dfir]
level: advanced
status: draft
description: "Interpret registry key last-write timestamps correctly: what updates them, granularity, why they are key-level not value-level, and common misreadings."
sources: ["https://github.com/msuhanov/regf/blob/master/Windows%20registry%20file%20format%20specification.md", "https://www.sans.org/posters/windows-forensic-analysis/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Interpreting registry key last-write times

**Goal:** every registry key has one FILETIME (`LastWriteTime` in the key node) - often the only
timestamp available for an artefact. It is easy to over-interpret.

## What it records
- Updated when the key is created, when any **value** under it is added, changed or deleted,
  and when a **direct subkey** is created or deleted. It is not updated when a deeper descendant changes.
- Values have no timestamps of their own (except data that embeds times, like UserAssist or BAM).
- Precision is 100 ns, but Windows may lazily flush; the time is when the change was made in memory.

## Implications
- For MRU-type keys (RecentDocs, RunMRU, TypedPaths) the last-write time = time of the **most
  recent** entry (the first in the MRUList order), not of all entries.
- For keys with many values (Run key), last-write dates the latest change, which may not be the malicious value.
- A key last-write time can be updated by benign software rewriting the same data.
- Registry cleanup tools and some backup/restore operations update last-write times en masse.

## Timestomping keys
- `NtSetInformationKey` with `KeyWriteTimeInformation` can set arbitrary last-write times
  (SetRegTime tool). Detect via comparison with transaction log sequence and with times in the
  hive bins of surrounding keys, or with VSS copies of the hive.

## Practice
- Report as "the key was last modified at", not "the program ran at".
- Corroborate with value-embedded times (BAM, UserAssist, ShimCache in some versions), event logs, and file system times.
- Compare with the same key in older hives from VSS or `RegBack` to bracket when a value appeared.

## Gotchas
- Hive replay from transaction logs changes last-write times to the latest logged state: note which state you report.
- Some parsers display local time; normalise to UTC.

## Verify
Every timestamp in the report sourced from a key last-write is described as such and corroborated where possible.
