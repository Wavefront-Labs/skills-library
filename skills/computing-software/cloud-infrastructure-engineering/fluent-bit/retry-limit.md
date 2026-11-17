---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.retry-limit
name: retry-limit
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, retry-limit, no-retries, no-limits, dead-letter-queue, outputs]
level: practitioner
status: docs-checked
description: "Cap, remove or disable retries per output with Retry_Limit and keep rejected chunks via the dead letter queue."
sources: ["https://docs.fluentbit.io/manual/administration/scheduling-and-retries"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Retry limits per output

The scheduler's `retry_limit` is set independently on each output:

| Value | Effect |
| --- | --- |
| integer N (N >= 1) | retry at most N times then discard; default `1` |
| `no_limits` or `false` | unlimited retries |
| `no_retries` | retries disabled; no second attempt after a failure |

When a chunk exhausts retries or retries are disabled, the data is discarded by default. To keep it for analysis, set `storage.keep.rejected` to `on` in the service section to enable the dead letter queue (see `computing-software.cloud-infrastructure-engineering.fluent-bit.dead-letter-queue`).

In v5.1.3 or later, if too many flush requests are in flight when a retry is due, Fluent Bit reschedules the retry without counting it against the limit.

```yaml
pipeline:
  outputs:
    - name: http
      host: 192.168.5.6
      port: 8080
      retry_limit: false
    - name: es
      host: 192.168.5.20
      port: 9200
      logstash_format: on
      retry_limit: 5
```

Here the HTTP output retries forever while Elasticsearch gives up after 5 attempts.

## Checked

2026-11-03. Confirmed on the Fluent Bit Scheduling and retries page: retry_limit values and default 1 with N >= 1, discard by default, `storage.keep.rejected`, v5.1.3 rescheduling, and the http / es example. Removed: an unsourced buffer-trade-off claim.

Method: documentation only; no commands were run.
