---
id: computing-software.cloud-infrastructure-engineering.fluentd.failure-scenarios
name: failure-scenarios
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, failure-scenarios, data-loss, buf-memory, buf-file, logger-libraries]
level: advanced
status: docs-checked
description: "What happens to data when the app, forwarder, aggregator or storage destination fails in a Fluentd deployment, by buffer type."
sources:
  - https://docs.fluentd.org/deployment/failure-scenarios
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd failure scenarios
Assumes the forwarder/aggregator layout from `high-availability-forwarder-aggregator`.

**App cannot post to the local forwarder**: depends on the logger library. Memory buffering (Ruby, Java, Python, Perl libraries) holds logs while Fluentd is down and retries, but once the maximum buffer memory is reached most implementations write the data to disk or throw the logs away. Exponential backoff on reconnect exists in the Ruby and Java libraries.

**Forwarder or aggregator dies**:
- `buf_memory`: buffered data is completely lost. Lowering `flush_interval` reduces the exposure but increases transfers.
- `buf_file`: data stays on disk and is resent after recovery. It is lost if the buffer file breaks through I/O errors or if the disk is full.

**Storage destination down** (S3, MongoDB, HDFS ...): Fluentd keeps retrying; retry logic depends on the plugin. With `buf_memory` aggregators stop accepting new logs at their buffer limit; with `buf_file` they keep accepting until disk space runs out.

See also `buffer-retry-and-backoff`.

## Checked

2026-11-04. Confirmed against the Fluentd Failure Scenarios page (docs.fluentd.org/deployment/failure-scenarios): logger library buffering and backoff, buf_memory and buf_file loss conditions, storage destination outage. Corrected: memory-limit behaviour (the page says write to disk or discard). Removed: the list of mitigations (not on this page).

Method: documentation only; no commands were run.
