---
id: computing-software.systems-network-administration.kopia.kopia-tuning-cpu-memory-and-checkpoints
name: kopia-tuning-cpu-memory-and-checkpoints
category: computing-software
field: systems-network-administration
product: kopia
tags: [cpu-usage, memory-usage, max-parallel-file-reads, max-parallel-snapshots, checkpoints, incomplete-snapshots]
level: practitioner
status: docs-checked
description: "Reduce Kopia CPU and RAM use via parallelism policies and understand incomplete snapshots and checkpoints."
sources: ["https://kopia.io/docs/faqs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The two policy settings that most reduce CPU are parallelism limits; lowering them also reduces memory.

```console
kopia policy set --global --max-parallel-snapshots=2
kopia policy set --global --max-parallel-file-reads=2
kopia policy set /path/to/source --max-parallel-file-reads=2
```

`max-parallel-snapshots` limits snapshots running at once (irrelevant if you run one at a time). `max-parallel-file-reads` limits files uploaded simultaneously and defaults to the number of logical CPU cores; it can be set per policy or globally. Lower values lengthen snapshot time.

## Memory

Compression and parallelism are the two big memory consumers. Disabling compression lowers memory. If you keep it, benchmarks show s2, deflate and gzip are the most memory-friendly for small files; for large files all algorithms use similar memory.

## Incomplete snapshots

For large sources, Kopia writes checkpoints at a fixed interval. If a snapshot runs longer than the checkpoint interval, a temporary incomplete snapshot is created, which stops the work so far from being garbage-collected by maintenance. Kopia removes incomplete snapshots once a complete snapshot has been created. The checkpoint interval is documented in the command-line reference.

## Checked

2026-11-03. Confirmed against the fetched Kopia docs pages: FAQ (max-parallel-snapshots and max-parallel-file-reads behaviour and default, memory advice on compression and parallelism, incomplete snapshots and checkpoints). Removed or corrected: the 'resume cheaply' claim and the KopiaUI Upload tab location, neither on the page.
Method: documentation only; no commands were run.
