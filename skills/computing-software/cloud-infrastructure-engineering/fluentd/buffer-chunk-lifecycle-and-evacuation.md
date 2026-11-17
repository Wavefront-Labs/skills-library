---
id: computing-software.cloud-infrastructure-engineering.fluentd.buffer-chunk-lifecycle-and-evacuation
name: buffer-chunk-lifecycle-and-evacuation
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, buffer, stage, queue, evacuate-limit-size, chunk-backup, retry-timeout]
level: advanced
status: docs-checked
description: "How Fluentd chunks move from stage to queue, what happens when retries run out (evacuation to root_dir since v1.19.0), and recovering evacuated chunks."
sources:
  - https://docs.fluentd.org/buffer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd chunk lifecycle and evacuation
A buffer is a set of chunks (files for `buf_file`, memory blocks for `buf_memory`). New chunks start in the **stage**, being filled, then move to the **queue** to await sending.

Retries: exponential backoff waits 1, 2, 4, 8... seconds with defaults; intervals are randomised by a factor between 0.875 and 1.125 (`retry_randomize false` disables); `retry_max_interval` caps the wait; `retry_type periodic` disables backoff. Fluentd gives up after `retry_max_times` (default none) or `retry_timeout` (default 72h).

At give-up, before v1.19.0 all queued chunks were discarded. Options: `retry_forever`, or a `secondary` output. Since v1.19.0 `buf_file` and `buf_file_single` evacuate queued chunks to `${root_dir}/buffer/${plugin_id}/` (`root_dir` from `<system>`, else `/tmp/fluent/`). Recover by moving files back to the plugin's buffer directory and restarting. `buf_memory` cannot do this. Set `@id` on the output, or `${plugin_id}` may change on reload.

`evacuate_limit_size` (since v1.20.0) caps the evacuation directory; it is approximate and counts files directly under it. `0` discards without evacuating.

Unrecoverable errors (`Fluent::UnrecoverableError`, `TypeError`, `ArgumentError`, `NoMethodError`) skip retries: chunk goes to `secondary` if it is a different type, else to `${root_dir}/backup/worker${worker_id}/${plugin_id}/{chunk_id}.log`. Since v1.16.0 corrupted chunks found at startup are also moved to backup.

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/buffer and confirmed: stage and queue, backoff randomisation, evacuation directory, unrecoverable errors, backup path. Removed or reworded: nothing.

Method: documentation only; no commands were run.
