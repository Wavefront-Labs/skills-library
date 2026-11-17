---
id: computing-software.cloud-infrastructure-engineering.fluentd.source-only-mode
name: source-only-mode
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, source-only-mode, with-source-only, sigwinch, source-only-buffer]
level: advanced
status: docs-checked
description: "Run Fluentd with only input plugins (since v1.18.0), buffer events in a temporary file buffer, cancel with SIGWINCH and recover leftover buffers."
sources:
  - https://docs.fluentd.org/deployment/source-only-mode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd Source Only Mode
Since v1.18.0 (not on Windows) only input plugins run; events go to a temporary file buffer (the `out_buffer` buffer). `SIGWINCH` to the supervisor cancels the mode: all plugins start and the buffer loads.

Launch with `--with-source-only` or `with_source_only` in `<system>`.

Buffer path default: `/tmp/fluent/source-only-buffer/{unique instance ID}`, logged at startup. Defaults match `out_buffer` except `path` is automatic and `overflow_action` is `drop_oldest_chunk`. Tune it in `<system><source_only_buffer>` (`flush_thread_count`, `flush_interval`, `chunk_limit_size`, `total_limit_size`, `compress`, `path`).

Recovery after Fluentd stops with buffer remaining (a warning logs the path; each run uses a new path otherwise):
1. Set the remaining path explicitly:
```
<system>
  <source_only_buffer>
    path /tmp/fluent/source-only-buffer/<instance-id>
  </source_only_buffer>
</system>
```
2. Start with source-only mode again.
3. Send `SIGWINCH` to the supervisor to load it.

## Checked

2026-11-04. Confirmed against the Fluentd Source Only Mode page (docs.fluentd.org/deployment/source-only-mode) and the System Configuration page (docs.fluentd.org/deployment/system-config, source_only_buffer section): v1.18.0, Windows exclusion, SIGWINCH, launch options, default buffer path, out_buffer defaults, the tunable options and the recovery steps. Nothing removed.

Method: documentation only; no commands were run.
