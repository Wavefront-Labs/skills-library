---
id: computing-software.cloud-infrastructure-engineering.fluentd.buffer-retry-and-backoff
name: buffer-retry-and-backoff
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, buffer, retry, exponential-backoff, retry-timeout, secondary, chunk-backup]
level: practitioner
status: docs-checked
description: "Control Fluentd flush retries: retry_type, retry_wait, backoff base and max interval, retry_timeout, retry_forever, secondary threshold, chunk backup."
sources:
  - https://docs.fluentd.org/configuration/buffer-section
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd retry parameters
- `retry_type`: `exponential_backoff` (default) or `periodic` (fixed `retry_wait`).
- `retry_wait`: default 1s, the constant factor of the backoff.
- `retry_exponential_backoff_base`: default 2.
- `retry_max_interval`: cap on the interval between retries (default none).
- `retry_randomize`: default true, randomises intervals to avoid burst retries.
- `retry_timeout`: default 72h; after this the queued chunks are discarded (before v1.19.0) or evacuated by the file buffers (since v1.19.0). The last retry is made at exactly this limit.
- `retry_max_times`: default none.
- `retry_forever`: default false; if true, ignores `retry_timeout` and `retry_max_times`.
- `retry_secondary_threshold`: default 0.8, the ratio of `retry_timeout` at which the `<secondary>` output is used (max 1.0).
- `disable_chunk_backup` (since v1.2.6, default false): discard unrecoverable chunks instead of keeping them in the backup directory.
- `evacuate_limit_size`: approximate size cap on chunks evacuated when the retry limit is reached; `0` discards queued chunks without evacuating, as before v1.19.0. Default nil (no limit).

Exponential backoff total retry time: `c*(b^k - 1) / (b - 1)` where c is `retry_wait`, b the base and k the retry count; with defaults this is `2^k - 1` seconds.

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/configuration/buffer-section, https://docs.fluentd.org/buffer and confirmed: retry parameter defaults, backoff formula, secondary threshold, disable_chunk_backup, evacuate_limit_size. Removed or reworded: nothing.

Method: documentation only; no commands were run.
