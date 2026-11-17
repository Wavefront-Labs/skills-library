---
id: computing-software.database-administration.vitess.vitess-sequences
name: vitess-sequences
category: computing-software
field: database-administration
product: vitess
tags: [sequences, auto-increment, vschema, sharded-keyspace, unsharded-keyspace]
level: practitioner
status: docs-checked
description: "Replace auto_increment in a sharded Vitess keyspace with a sequence: backing table, VSchema wiring, cache block, direct access, mixed-insert limit."
sources:
  - https://vitess.io/docs/25.0/reference/features/vitess-sequences/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Keeping MySQL `auto_increment` semantics across shards is hard, so Vitess provides sequences. Each sequence is backed by a single-row table that must live in an unsharded keyspace, with the comment `vitess_sequence`:

```sql
create table user_seq(id bigint, next_id bigint, cache bigint, primary key(id)) comment 'vitess_sequence';
```

The columns are held as int64 in vttablet, so `bigint unsigned` is not supported. In the unsharded keyspace VSchema declare it with `"user_seq": {"type": "sequence"}`. In the sharded table VSchema add:

```json
"auto_increment": { "column": "user_id", "sequence": "user_seq" }
```

Then insert one row: `id` must be 0, `next_id` is the first value, and `cache` is how many IDs the primary vttablet reserves per block; the page suggests something like 1000, for example `insert into user_seq(id, next_id, cache) values(0, 1, 1000);`. A larger cache gives better latency and throughput but a tablet crash can lose the block, leaving an ID gap.

Omitting the column on insert makes VTGate fetch the next value. You can also run `select next value from user_seq;` or `select next 5 values from user_seq;` (reserves extra values).

Limitation: unlike MySQL, sequences do not track explicitly inserted values. After inserting ids 1,2,3 explicitly, a later insert without the id draws 1 from the sequence and fails with duplicate entry error 1062. Do not mix explicit and generated values. As with auto_increment, gaps are possible and strict ordering is not guaranteed. The page also notes sequential IDs can leak user counts.

## Checked

2026-11-08. Read in full: Sequences page (vitess.io docs 25.0, via the website repo markdown). Confirmed: motivation, backing table DDL and comment, int64 note, VSchema fragments, initialization row and cache guidance, direct access statements, shared auto_increment properties, the mixed-insert failure and the ID-leak note. Fixed: the opening claim that sharded tables cannot use auto_increment is now worded as the page states it.

Method: documentation only; no commands were run.
