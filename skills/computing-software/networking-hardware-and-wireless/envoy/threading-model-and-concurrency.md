---
id: computing-software.networking-hardware-and-wireless.envoy.threading-model-and-concurrency
name: threading-model-and-concurrency
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, threading-model, workers, concurrency, main-thread, worker-threads, file-flusher]
level: practitioner
status: docs-checked
description: "Envoy single-process multi-thread model: main thread, per-core workers, file flusher, and what --concurrency should be."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/intro/threading_model.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# threading model and concurrency
Envoy is one process with several threads, built to be non-blocking. Three components:
1. The main thread: coordination only, including xDS updates, stats flushing and the admin interface. It does not handle traffic.
2. Worker threads: set by `--concurrency`; they listen, filter and forward traffic. A connection lives on exactly one worker for its life.
3. A file flusher thread flushes access logs to disk so the data path is not blocked.

The docs recommend one worker per hardware thread to maximise CPU use without excess context switching.

```
envoy -c envoy.yaml --concurrency 8
```
Consequences worth remembering:
- Some state is per worker: Lua environments (no true globals) and connection pools (each worker keeps its own pools per cluster).
- By default there is no coordination between workers: all of them accept on each listener and rely on the kernel to balance. For a few very long-lived connections (for example mesh HTTP/2 or gRPC egress) a listener's `connection_balance_config` can force balancing between workers.
- Envoy is written to be non-blocking; the Lua docs say never to block.

Gotcha: when `--concurrency` is unset it defaults to the minimum of hardware threads, CPU affinity size and (on Linux) the cgroup CPU limit, so container limits are respected by default; `ENVOY_CGROUP_CPU_DETECTION=false` disables the cgroup part. A value of 0 still runs one worker. The `server.concurrency` stat can be read with `/stats?filter=^server.concurrency$`.

## Checked
2026-11-03. Confirmed against threading_model.rst and cli.rst (--concurrency). Removed or corrected: the claim that --concurrency ignores the cgroup CPU limit (the CLI page says it respects it), the UDP filter and local rate limit per-worker claims, and the 'confirm' note.
Method: documentation only; no commands were run.
