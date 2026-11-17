---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.backpressure-memory-buffering
name: backpressure-memory-buffering
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, backpressure, mem-buf-limit, memory-buffering, paused-inputs]
level: advanced
status: docs-checked
description: "Limit memory per input with mem_buf_limit, understand the permissive overshoot and the pause and resume log lines."
sources: ["https://docs.fluentbit.io/manual/administration/backpressure"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Backpressure with memory-only buffering

Backpressure appears when Fluent Bit ingests or creates data faster than it can flush it. Buffering absorbs some of it, but unbounded buffering eventually fills storage.

For inputs using memory-only buffering, set `mem_buf_limit` on the input. It does not affect inputs using filesystem buffering. When the limit is reached, Fluent Bit stops buffering from that source until enough chunks flush. Most plugins log `[warn] [input] <PLUGIN NAME> paused (mem buf overlimit)` on pause and `[info] [input] <PLUGIN NAME> resume (mem buf overlimit)` on resume.

**The limit is permissive.** Example: limit 1MB, the input appends 700KB, the output backend is down, the scheduler retries in 10 seconds, and the input then appends 500KB. The engine allows that append, so 1.2MB is buffered; one write past the capacity is allowed. Then it blocks local buffers for the input and invokes the plugin's `pause` callback. The plugin keeps its own state and decides what to do while paused. When the flush succeeds or retries give up, memory is released, counters drop to 500KB, and the `resume` callback runs.

**Warning:** some inputs lose data after `mem_buf_limit` is reached with memory-only buffering. Use filesystem buffering if loss is unacceptable.

**HTTP-based inputs** (`http`, `splunk`, `elasticsearch`, `opentelemetry`, `prometheus_remote_write`) pause their shared listener: connections are accepted then closed immediately and in-flight requests dropped, so senders must retry on connection failure.

## Checked

2026-11-03. Confirmed on the Fluent Bit Backpressure page: mem_buf_limit behaviour, pause and resume log lines, the 1 MB / 700 KB / 500 KB permissive example, data-loss warning, and HTTP-based input pause behaviour.

Method: documentation only; no commands were run.
