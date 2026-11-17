---
id: computing-software.messaging-and-integration.redpanda.rpk-topic-trim-prefix-delete-records
name: rpk-topic-trim-prefix-delete-records
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [rpk, topic, trim-prefix, delete-records, log-start-offset, timestamps]
level: practitioner
status: docs-checked
description: "Delete records from the front of a topic with rpk topic trim-prefix by offset, timestamp or file, and avoid the timestamp-order trap."
sources:
  - https://docs.redpanda.com/streaming/current/reference/rpk/rpk-topic/rpk-topic-trim-prefix/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`rpk topic trim-prefix` (alias `rpk topic trim`) sets the partition LogStartOffset to a requested offset. All segments whose base offset is below it are deleted, and records before the offset can no longer be read.

**Flags**
- `-o, --offset`: the new start offset: `end`, a number such as `47`, or a timestamp prefixed with `@`.
- `-p, --partitions`: comma-separated partitions; defaults to all.
- `-f, --from-file`: a file of lines `[TOPIC] [PARTITION] [OFFSET]`, or the keyed JSON or YAML equivalent.
- `--no-confirm`: skip the prompt.

**Examples from the page**
```bash
rpk topic trim-prefix foo --offset 120 --partitions 1
rpk topic trim-prefix foo -o "@1622505600"
rpk topic trim-prefix --from-file /path/to/to_trim.json
```

**Timestamp warning.** With a timestamp, Redpanda advances the start offset to the first record whose timestamp is after the threshold. If record timestamps are not in order with respect to offsets, this can delete data unintentionally. Before using a timestamp, check that timestamps increase with offsets; the page suggests sampling:

```bash
rpk topic consume <topic> -n 50 --format '%o %d{go[2006-01-02T15:04:05Z07:00]} %k %v'
```

Use this when you need to reclaim space or remove old data from a topic without waiting for retention, and always confirm the offsets per partition first, since the operation is destructive.

## Checked

2026-11-08. Read the whole rpk topic trim-prefix page and confirmed the LogStartOffset semantics, the alias, all four flags, the file format, the examples (the file path is a placeholder) and the timestamp warning with the sampling command. The closing advice is an inference from the deletion behavior described.

Method: documentation only; no commands were run.
