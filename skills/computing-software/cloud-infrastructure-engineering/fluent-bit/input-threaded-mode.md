---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.input-threaded-mode
name: input-threaded-mode
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, multithreading, threaded-inputs, event-loop, performance]
level: practitioner
status: docs-checked
description: "Move an input off the main event loop with threaded true and know which inputs are always threaded."
sources: ["https://docs.fluentbit.io/manual/administration/multithreading", "https://docs.fluentbit.io/manual/administration/performance"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Threaded inputs

Fluent Bit has one event loop in the main thread. It manages timers, internal messages, flush scheduling and retries. To free that thread, run an input in its own self-contained thread with the `threaded` setting.

```yaml
pipeline:
  inputs:
    - name: tail
      path: '/var/log/containers/*.log'
      threaded: true
```

All inputs can run threaded. These always run threaded regardless of configuration:
- Kubernetes Events
- Node Exporter Metrics
- Process Exporter Metrics
- Windows Exporter Metrics

Inputs are not aware of multithreading; Fluent Bit manages the thread.

Where work runs:
- **Filters** always run in the main thread.
- **Processors** run in the self-contained thread of their input or output, if applicable.

By default most inputs share the main event loop thread; threaded mode lets you take advantage of other CPU cores. Output parallelism is a separate setting, covered in `computing-software.cloud-infrastructure-engineering.fluent-bit.output-workers`.

## Checked

Method: docs-checked 2026-11-09 against the Fluent Bit docs multithreading page and performance tips page (raw markdown, read in full).
