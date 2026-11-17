---
id: computing-software.web-development.node-express.node-debugging-and-profiling
name: node-debugging-and-profiling
category: computing-software
field: web-development
product: node-express
tags: [node, node-inspect, node-profiling, heap-snapshot, cpu-profile, memory-leaks, chrome-devtools, web-development]
level: practitioner
status: verified
description: "Debugging and profiling Node.js: --inspect with Chrome DevTools/VS Code, CPU profiles and flame graphs, heap snapshots for leaks, diagnostic reports and safe production use."
sources:
  - https://nodejs.org/en/learn/getting-started/debugging
  - https://nodejs.org/en/learn/diagnostics/memory/using-heap-snapshot
  - https://nodejs.org/api/cli.html#--cpu-prof
  - https://nodejs.org/api/report.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging and profiling Node.js

**Goal:** find the bug, the hot function or the leak with built-in tooling before guessing.

Ran on Node 24.22 (Windows) unless marked POSIX: `--inspect` and `--inspect-brk` print `Debugger listening on ws://127.0.0.1:9229/...`; `--inspect --watch` works together; `--cpu-prof --cpu-prof-dir` wrote a `.cpuprofile` on exit; `--trace-sync-io` warned "Detected use of sync API" only for the sync call made after the first tick; `--heapsnapshot-near-heap-limit=1` with `--max-old-space-size=60` wrote a `.heapsnapshot` just before the out-of-memory abort; `monitorEventLoopDelay()` reported a 200 ms block. The `SIGUSR1`/`SIGUSR2` signal commands below are POSIX features documented in the Node CLI docs and were not run on this Windows host.

## 1. Inspector
```bash
node --inspect server.js              # 127.0.0.1:9229
node --inspect-brk script.js          # pause on first line
node --inspect --watch server.js
kill -USR1 <pid>                      # enable inspector on a running process (POSIX)
```
Open `chrome://inspect` -> "Open dedicated DevTools for Node", or VS Code "JavaScript Debug Terminal" (auto-attaches to any node started there). Never bind `--inspect=0.0.0.0` on a reachable host - the inspector allows arbitrary code execution. Tunnel instead: `ssh -L 9229:localhost:9229 host`.

## 2. CPU: what's slow
```bash
node --cpu-prof --cpu-prof-dir=./prof server.js   # writes .cpuprofile on exit; load in DevTools Performance tab
npx 0x server.js                                   # flame graph HTML
```
Run a realistic load (`autocannon -c 50 -d 30 http://localhost:3000/x`) while profiling. Look for wide frames: JSON serialisation, regexes, sync crypto/zlib, logging.

## 3. Memory: what's leaking
```bash
node --heapsnapshot-signal=SIGUSR2 server.js       # kill -USR2 <pid> writes a .heapsnapshot
node --heapsnapshot-near-heap-limit=2 server.js    # auto snapshot before OOM
```
Take snapshot A, run traffic, force GC (DevTools trash icon), take B, compare "Objects allocated between snapshots" - sort by retained size and follow the retainer chain. Usual suspects: module-level Maps/arrays used as caches, event listeners added per request, closures in timers, unbounded queues.
Heap snapshots pause the process and can need a lot of extra memory - take them on a drained instance.

## 4. Event loop
`perf_hooks.monitorEventLoopDelay()` to measure lag; `--trace-sync-io` flags sync calls after the first tick.

## 5. Crashes and warnings
```bash
node --trace-warnings --trace-uncaught server.js
node --report-on-fatalerror --report-uncaught-exception --report-directory=/tmp/reports server.js
```
`--report-directory` must already exist: ran with a missing directory and no report was written (no error); with an existing directory `--report-uncaught-exception` and `--report-on-fatalerror` (heap OOM) both wrote `report.*.json`. Diagnostic reports (JSON) capture stack, heap stats, libuv handles and env - redact before sharing.

## 6. Production-friendly options
Continuous profiling (Pyroscope, Datadog, Grafana) via sampling agents; `clinic doctor` for a quick diagnosis on staging.

## Verify
- [ ] Profiling before/after a fix shows the hot function shrinking.
- [ ] Leak fix confirmed: heap after GC flat over a 30-minute load test.
- [ ] No inspector port exposed in production configs (`grep -rn "inspect" Dockerfile* deploy/`).
