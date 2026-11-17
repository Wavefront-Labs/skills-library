---
id: computing-software.web-development.hugo.template-performance-metrics
name: template-performance-metrics
category: computing-software
field: web-development
product: hugo
tags: [template-metrics, performance, cache-potential, debug-timer, virus-scanner]
level: practitioner
status: docs-checked
description: "Find slow templates with hugo build --templateMetrics and --templateMetricsHints: column meanings, cache potential caveats and other speed tips."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/troubleshooting/performance.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Run:

```sh
hugo build --templateMetrics --templateMetricsHints
```

Columns:

- cumulative duration: total time executing the template.
- average duration and maximum duration: per execution.
- cache potential: percentage; a partial at 100% is a candidate for `partialCached`.
- percent cached: cached executions divided by total.
- cached count and total count.
- template: path relative to `layouts`.

Pages build in parallel, so cumulative durations often sum to more than the build time.

Caveat: cache potential compares each run's output to the first run's. It cannot see side effects such as `warnf` or `errorf`, or logic depending on execution order such as `IsHome` conditions. A partial with no visible output but validation or context-based logic can show 100% and still be unsafe to cache; review it first. Extra arguments to `partialCached` create cached variants.

Other tips:

- Virus scanners can slow builds badly; with Microsoft Defender, times may rise 400% or more. Add the Hugo executable to the process exclusion list, with caution.
- Use `debug.Timer` to time a block of template code.
- Inefficient templates impede performance most.

## Checked

2026-11-04. Confirmed against the Hugo docs page Performance: the `hugo build --templateMetrics --templateMetricsHints` command, every column definition, the parallel-build note on cumulative durations, the cache potential warning about side effects, the virus-scanner slowdown of 400% or more with Microsoft Defender and the exclusion advice, and the caution. Nothing removed.

Method: documentation only; no commands were run.
