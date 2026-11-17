---
id: computing-software.software-engineering.typescript.node-diagnostics-inspect-and-profiling
name: node-diagnostics-inspect-and-profiling
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, node-inspect, cpu-prof, heap-snapshot, diagnostic-report, clinic-js, nodejs]
level: advanced
status: docs-checked
description: "Diagnose Node processes: --inspect with Chrome DevTools, --cpu-prof and --heap-prof, heap snapshots on signal or near OOM, diagnostic reports, and production-safe profiling."
sources:
  - https://nodejs.org/api/cli.html#--inspectporthostport
  - https://nodejs.org/api/cli.html#--cpu-prof
  - https://nodejs.org/api/cli.html#--heapsnapshot-signalsignal
  - https://nodejs.org/api/report.html
  - https://nodejs.org/api/v8.html#v8writeheapsnapshotfilenameoptions
  - https://nodejs.org/api/perf_hooks.html#perf_hooksmonitoreventloopdelayoptions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node diagnostics: inspect and profiling

**Goal:** turn "the Node service is slow / leaking / crashing" into a profile, snapshot
or report you can read.

## Attach a debugger / DevTools
```bash
node --inspect=127.0.0.1:9229 dist/server.js        # never bind 0.0.0.0 in prod: full RCE
node --inspect-brk test.js                          # pause on first line
kill -USR1 <pid>                                    # enable inspector on a running process (POSIX)
```
Attach Chrome DevTools or an IDE through the V8 inspector integration.

## CPU profiling
```bash
node --cpu-prof --cpu-prof-dir=/tmp/prof dist/server.js   # writes .cpuprofile on exit
```
Text summary: `node --prof` + `node --prof-process isolate*.log`.

## Memory
```bash
node --heapsnapshot-signal=SIGUSR2 dist/server.js    # kill -USR2 <pid> writes a .heapsnapshot
node --heapsnapshot-near-heap-limit=2 --max-old-space-size=1536 dist/server.js   # snapshots before OOM
node --heap-prof dist/server.js                       # sampling allocation profile
```
In code: `v8.writeHeapSnapshot()`. Snapshot creation is synchronous (it blocks the event loop) and needs memory about twice the heap size - take snapshots off-rotation.

## Diagnostic reports
```bash
node --report-on-fatalerror --report-uncaught-exception --report-on-signal --report-directory=/var/log/node app.js
```
JSON with JS and native stacks, heap stats, libuv handles, env, resource usage - first thing
to grab for crashes and hangs. `process.report.writeReport()` on demand.

## Event-loop health
```ts
import { monitorEventLoopDelay } from "node:perf_hooks";
const h = monitorEventLoopDelay({ resolution: 20 }); h.enable();
setInterval(() => { metrics.gauge("eventloop.p99_ms", h.percentile(99) / 1e6); h.reset(); }, 10_000);
```

## Production-safe practice
- Prefer sampling profilers and continuous profiling agents over attaching DevTools to live traffic.
- `--max-old-space-size` (MiB) sets the V8 old-space limit; its default depends on system configuration, so size it to the container and leave room for buffers and native memory.

## Verify
- [ ] Signal-triggered heap snapshot and diagnostic report work in the deployed container.
- [ ] Inspector never exposed on a public interface.

## Checked
Checked 2026-10-25 against the Node.js API docs (doc/api on main: cli, report, v8, perf_hooks, debugger). Confirmed: `--inspect[=[host:]port]` defaults to 127.0.0.1:9229 and binding to a public address enables remote code execution; `--inspect-brk`; `SIGUSR1` starting the inspector (documented through `--disable-sigusr1`); `--cpu-prof` and `--cpu-prof-dir` write a `.cpuprofile`; `--prof` and `--prof-process`; `--heapsnapshot-signal`, `--heapsnapshot-near-heap-limit`, `--heap-prof`; heap snapshots block the event loop and need about twice the heap in memory; `--report-on-fatalerror`, `--report-uncaught-exception`, `--report-on-signal`, `--report-directory`, `process.report.writeReport()`; `monitorEventLoopDelay` histogram values in nanoseconds. Removed unconfirmed claims about third-party profilers, DevTools snapshot views and cgroup behaviour.
Method: documentation only; no commands were run.
