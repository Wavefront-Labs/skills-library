---
id: computing-software.web-development.eleventy.build-performance-analysis
name: build-performance-analysis
category: computing-software
field: web-development
product: eleventy
tags: [build-performance, benchmark, cpu-prof, speedscope, slow-build]
level: advanced
status: docs-checked
description: "Find Eleventy build bottlenecks with the 8 percent warnings, DEBUG=Eleventy:Benchmark aggregate output and Node CPU profiling viewed in SpeedScope."
sources:
  - https://www.11ty.dev/docs/debug-performance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Warnings.** By default Eleventy warns when a piece takes longer than 8% of total build time: filters and JavaScript functions, shortcodes, data files. Watch dependency resolution only warns above 500ms (not part of build time). The list is not exhaustive.

**Benchmarks**: show measurements for everything, not just the slow ones.

```sh
DEBUG=Eleventy:Benchmark* npx @11ty/eleventy
# Windows cmd.exe
set DEBUG=Eleventy:Benchmark* & npx @11ty/eleventy
```

Aggregate lines report totals per category, for example:

```
Benchmark (Aggregate): Template Write took 2088ms (27.6%, called 312x, 6.7ms each)
```

Categories include file system search, Data File, Template Read, Passthrough Copy File, Template Compile, Template Render and Template Write. Percentages can exceed 100% because tasks are asynchronous (passthrough copy especially).

**CPU profiling** with Node's built-in profiler (Node v12+):

```sh
npx --node-options="--cpu-prof" @11ty/eleventy --quiet
# or
node --cpu-prof ./node_modules/.bin/eleventy --quiet
```

It writes a `CPU.***.cpuprofile` file in the current directory. View it in SpeedScope; the docs recommend the Left Heavy and Sandwich views.

## Checked

2026-11-04. Confirmed against the Eleventy page Analyzing Build Performance: the 8% warning rule and its list, the 500ms watch-dependency exception, the DEBUG=Eleventy:Benchmark* commands for macOS/Linux and Windows, the aggregate benchmark categories and the over-100% note, `--cpu-prof` usage (Node v12+) and the CPU.***.cpuprofile output, SpeedScope Left Heavy and Sandwich. Removed the unconfirmed 0.11.0+ version gate and the speedscope.app URL.

Method: documentation only; no commands were run.
