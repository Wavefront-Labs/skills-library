---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.memory-limiter-processor
name: memory-limiter-processor
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, processors, memory-limiter, backpressure, oom]
level: practitioner
status: docs-checked
description: "Protect a Collector from running out of memory by placing the memory_limiter processor first in every pipeline."
sources:
  - https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/memorylimiterprocessor/README.md
  - https://opentelemetry.io/docs/collector/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The memory limiter checks memory usage periodically and refuses data and forces garbage collection when limits are exceeded. It uses a soft and a hard limit: `limit_mib` is the hard limit, and the soft limit is `limit_mib` minus `spike_limit_mib`.

```yaml
processors:
  memory_limiter:
    check_interval: 5s
    limit_mib: 4000
    spike_limit_mib: 500
```

Details from the README:

- Above the soft limit the processor returns non-permanent errors to the preceding component, which should retry or apply backpressure. If it does not retry, data is permanently lost.
- Above the hard limit it also forces GC. Normal operation resumes below the soft limit.
- Add it as the first processor in a pipeline so backpressure reaches receivers.
- `check_interval` defaults to 0s; 1 second is recommended. Set one of `limit_mib` or `limit_percentage`; `limit_mib` wins.
- `spike_limit_mib` defaults to 20% of `limit_mib` and should cover growth within one check interval.
- Use `limit_percentage` in containers (cgroups on Linux), for example 75% of 1GiB gives 750 MiB. Total process memory runs about 50MiB above `limit_mib`.
- Also set `GOMEMLIMIT` to 80% of the hard limit.
- Data arriving before rejection still uses memory.

## Checked

2026-11-03. Claims were read against these official pages:

- https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/memorylimiterprocessor/README.md
- https://opentelemetry.io/docs/collector/configuration/

Removed or reworded where the pages did not confirm them.

Method: documentation only; no commands were run.
