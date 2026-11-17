---
id: computing-software.cloud-infrastructure-engineering.fluentd.buffer-chunk-keys
name: buffer-chunk-keys
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, buffer, chunk-keys, timekey, timekey-wait, tag]
level: practitioner
status: docs-checked
description: "Fluentd buffer chunk keys: blank, tag, time with timekey and timekey_wait, record fields, nested fields, combined and empty keys."
sources:
  - https://docs.fluentd.org/configuration/buffer-section
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd buffer chunk keys
`<buffer ARG>` sits once under `<match>` of a buffered output. Chunk keys (comma-separated) decide how events are grouped into chunks.

- **Blank**: all events append to one chunk until it is full. Use for plain transfers (forward, http) or destinations that ignore keys (stdout).
- **tag**: one chunk set per tag.
- **time**: requires `timekey`; groups by `unix time / timekey`. Chunks flush after the range ends plus `timekey_wait` (default 600s). Also `timekey_use_utc` (default false) and `timekey_zone` (e.g. `-0700`, `Asia/Tokyo`).
- **Other keys**: record field names; `tag` and `time` are reserved. Nested fields use record_accessor syntax: `<buffer $.nest.field>`.
- **Combined**: `<buffer tag,time>`. No hard limit on key count, but many keys degrade I/O and resources.
- **Empty**: `<buffer []>` disables the output's default chunk keys; also prevents placeholders that need chunk metadata (timekey, `${tag}`).

```
<buffer time>
  timekey      1h
  timekey_wait 5m
</buffer>
```
With timekey 3600 and timekey_wait 10m, the 12:00-12:59:59 chunk flushes at 13:10.

`@type` defaults to the output plugin's buffer, else `memory`; the docs recommend `file` for normal workloads.

## Checked

2026-11-04. Confirmed against the Fluentd Config: Buffer Section page (docs.fluentd.org/configuration/buffer-section): chunk key kinds, timekey and timekey_wait behaviour and defaults, timekey_use_utc, timekey_zone, nested fields, empty keys, @type default and the flush-time table. Nothing removed.

Method: documentation only; no commands were run.
