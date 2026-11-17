---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.s3-lifecycle-operator-config
name: s3-lifecycle-operator-config
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [walker, lifecycle-worker, delete-rate]
level: advanced
status: docs-checked
description: "Tune the s3_lifecycle worker in the Admin UI plugin config: cluster_deletes_per_second, burst, and walker_interval_minutes by cluster size."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/S3-Lifecycle-Operator-Guide
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# s3 lifecycle operator config

Keys are set in the admin UI's plugin config for the `s3_lifecycle` job.

| Key | Default | Use |
|---|---|---|
| `cluster_deletes_per_second` | 0 (unlimited) | Set positive when lifecycle deletes cause filer contention |
| `cluster_deletes_burst` | 0 (2x rate) | Raise if bursts overload the filer |
| `meta_log_retention_days` | 0 (unbounded) | Set only if you garbage-collect the meta-log yourself |
| `walker_interval_minutes` | 0 (every pass) | Throttle the bucket walk |

The walker lists bucket contents and evaluates rules; its cost scales with bucket size, not event rate. It always runs on a cold start and on rule changes, and otherwise at most once per `walker_interval_minutes`. Recommended values: 60 for small clusters (up to 1M objects, one bucket), 360 for medium (up to 100M), 1440 for large, 0 for testing. Negative values are rejected at worker start.

The shipped execution timeout and max runtime for `s3_lifecycle` are effectively unlimited, so there is no separate per-run cap knob.

With `walker_interval_minutes` at 0 the walker fires on every pass; the page says most production deployments should set a positive value.

## Checked

2026-11-04. Confirmed against the SeaweedFS wiki page S3 Lifecycle Operator Guide: the four keys and defaults, walker behaviour, recommended intervals by cluster size, negative-value rejection, unlimited execution timeout defaults. Removed the Verify line (head-object 404 is not on the page).
Method: documentation only; no commands were run.
