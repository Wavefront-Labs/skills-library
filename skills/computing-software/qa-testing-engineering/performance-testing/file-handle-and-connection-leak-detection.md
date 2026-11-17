---
id: computing-software.qa-testing-engineering.performance-testing.file-handle-and-connection-leak-detection
name: file-handle-and-connection-leak-detection
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [resource-leaks, connection-leaks, dynamic-analysis, file-descriptors, connection-pools]
level: practitioner
status: draft
description: "Detect file handle, socket and DB connection leaks in tests and under load: ResourceWarning, open handle checks, fd counts, pool metrics and leak detectors."
sources:
  - https://docs.python.org/3/library/exceptions.html#ResourceWarning
  - https://github.com/brettwooldridge/HikariCP#frequently-used
  - https://jestjs.io/docs/cli#--detectopenhandles
  - https://github.com/uber-go/goleak
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# File handle and connection leak detection

**Goal:** catch resources opened but never closed before they exhaust limits ("Too many open files", pool timeouts) in production.

## In unit/integration tests
- **Python:** make leaks fail: `python -X dev -W error::ResourceWarning -m pytest`, or in config `filterwarnings = ["error::ResourceWarning", "error::pytest.PytestUnraisableExceptionWarning"]`. Unclosed files, sockets and subprocesses then raise.
- **Node/Jest:** `jest --detectOpenHandles` reports handles (servers, sockets, timers) keeping the process alive.
- **Go:** `defer goleak.VerifyNone(t)` (or `goleak.VerifyTestMain(m)`) detects leaked goroutines, which often hold connections.
- **JVM:** HikariCP `leakDetectionThreshold=2000` logs a stack trace for connections held longer than 2 s; enable in test profiles.

## Fd and connection counts as test assertions
```python
import psutil
def test_export_does_not_leak_fds(client):
    p = psutil.Process()
    before = p.num_fds()                       # POSIX; on Windows use num_handles()
    for _ in range(200):
        client.get("/export.csv")
    assert p.num_fds() - before < 5
```
For DB connections, check the pool: SQLAlchemy `engine.pool.checkedout() == 0` after a test; Postgres `SELECT count(*) FROM pg_stat_activity WHERE application_name = 'app'` before/after.

## Under load or soak
- Linux: `ls /proc/<pid>/fd | wc -l` or `lsof -p <pid>` sampled over time; growth with steady load = leak. `ss -tanp` for sockets stuck in CLOSE_WAIT (peer closed, app never closed).
- Pool metrics (Hikari `hikaricp_connections_active`, `pending`) exported to Prometheus; pending > 0 with active at max = exhaustion.
- Compare against limits: `ulimit -n`, DB `max_connections`.

## Common causes
Missing `with`/try-with-resources/`finally`, early returns and exceptions skipping close, HTTP clients created per request, streams not consumed, transactions not committed/rolled back returning dirty connections.

## Gotchas
- GC may eventually close leaked objects, hiding leaks in short tests; loop the operation.
- Connection leaks appear only on error paths; include failure-injection tests.

## Verify
Leak detectors are on in CI, and a soak test shows flat fd and active-connection counts.
