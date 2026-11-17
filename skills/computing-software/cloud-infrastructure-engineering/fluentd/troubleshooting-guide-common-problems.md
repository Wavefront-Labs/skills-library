---
id: computing-software.cloud-infrastructure-engineering.fluentd.troubleshooting-guide-common-problems
name: troubleshooting-guide-common-problems
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, troubleshooting, buffer-overflow, missing-data, retry, parsing, read-from-head]
level: practitioner
status: docs-checked
description: "Triage common Fluentd problems: output stalled by retry backoff, BufferOverflowError, missing data, and parsing mistakes."
sources:
  - https://docs.fluentd.org/troubleshooting-guide
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd troubleshooting guide
**Logs stopped reaching the backend**
- Waiting on retry backoff: cap it with `retry_max_interval`, flush manually through RPC (`plugins.flushBuffers`), or restart (a memory buffer then risks data loss).
- Backend unreachable: run Fluentd manually and check the connection.
- Source stopped: for example a rotated file under `tail`; check the input path (use `*` where appropriate) and test network inputs with `fluent-cat`.

**BufferOverflowError** (buffer full): check `flush_interval` is low enough for your rate; raise `workers` and `flush_thread_count`; move from memory to file buffer (the default memory buffer total is 512MB); raise `total_limit_size` and `chunk_limit_size`.

**Missing data**: verify the config (for `tail`, records from the start of a file need `read_from_head true`); search the log for BufferOverflowError; check unflushed chunks in the file buffer `path`; consider pending retries.

**Wrong parsing**: test regexes with Rubular or fluentular using a log sample (also validates Ruby time format); look for an existing built-in parser first; ensure multiline parsers have all required settings.

Help channels listed: Fluent Slack, GitHub Discussions, GitHub Issues.

## Checked

2026-11-04. Confirmed against the Fluentd Troubleshooting Guide page (docs.fluentd.org/troubleshooting-guide): the four problem areas, each suggestion, the 512MB versus 64GB buffer defaults, support channels. Nothing removed.

Method: documentation only; no commands were run.
