---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.output-workers
name: output-workers
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, multithreading, workers, outputs, concurrent-flushes, performance]
level: practitioner
status: docs-checked
description: "Tune the workers setting on an output to flush in parallel, or reduce it to use the main thread."
sources: ["https://docs.fluentbit.io/manual/administration/multithreading", "https://docs.fluentbit.io/manual/administration/networking"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Output workers

Outputs flush either in the main Fluent Bit thread or in dedicated threads called workers. Set the count with `workers`. Each output has a plugin-specific default of `0`, `1` or `2` workers, and each worker can handle multiple concurrent flushes. All outputs can run multiple workers.

Even if an output uses workers by default, you can safely reduce the count below the default or disable workers entirely.

```yaml
pipeline:
  outputs:
    - name: es
      match: '*'
      host: 192.168.5.20
      port: 9200
      workers: 4
```

Interactions to remember:
- **Connections.** `net.max_worker_connections` applies per worker. Five workers with a limit of 10 allow up to 50 connections (see `computing-software.cloud-infrastructure-engineering.fluent-bit.network-connection-limits`).
- **Filters** always run on the main thread, while **processors** run in the self-contained thread of their output, if applicable.

## Checked

Method: docs-checked 2026-11-09 against the Fluent Bit docs multithreading page and networking page (raw markdown, read in full).
