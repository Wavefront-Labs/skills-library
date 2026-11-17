---
id: computing-software.database-administration.clickhouse.dictionaries-layouts-and-dictget
name: dictionaries-layouts-and-dictget
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, dictionary, dictget, layout, hashed-array]
level: practitioner
status: docs-checked
description: "Create ClickHouse dictionaries from a query source, choose a layout such as hashed_array, set LIFETIME and replace joins with dictGet."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/dictionary/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dictionaries layouts and dictget
A dictionary is an in-memory key-value structure refreshed from a source, used for fast lookups instead of JOINs.

```sql
CREATE DICTIONARY votes_dict
(
  PostId UInt64, UpVotes UInt32, DownVotes UInt32
)
PRIMARY KEY PostId
SOURCE(CLICKHOUSE(QUERY 'SELECT PostId, countIf(VoteTypeId = 2) AS UpVotes, countIf(VoteTypeId = 3) AS DownVotes FROM votes GROUP BY PostId'))
LIFETIME(MIN 600 MAX 900)
LAYOUT(HASHED());

SELECT dictGet('votes_dict', ('UpVotes', 'DownVotes'), toUInt64(11227902));
SELECT formatReadableSize(bytes_allocated) FROM system.dictionaries WHERE name = 'votes_dict';
```
LIFETIME(MIN, MAX) sets a random reload interval in seconds so replicas don't all reload at once.

Layouts: this example uses `HASHED()`. Look up the other `LAYOUT` options in the ClickHouse dictionary reference before choosing one.

Dictionaries are usually held in memory (`ssd_cache` is the exception), so watch their size. `LIFETIME(0)` prevents a dictionary from updating. Dictionaries also back the direct join algorithm for small, frequently changing datasets.

## Checked
2026-11-03. Confirmed against the ClickHouse docs page "Dictionary" (dictionary/index): CREATE DICTIONARY with a ClickHouse query source, `LIFETIME(MIN 600 MAX 900)` as a random reload interval, `LIFETIME(0)`, HASHED layout, `bytes_allocated` size check, in-memory caveat. Removed: the per-layout recommendations, max_array_size, the JOIN comparison and the duplicate-key and failed-reload gotchas, which no fetched page confirmed.
Method: documentation only; no commands were run.
