---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.python-client-multiprocess-mode
name: python-client-multiprocess-mode
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, python-multiprocess-mode, gunicorn-metrics, prometheus-client-python, uvicorn, django, flask]
level: advanced
status: verified
description: "Make prometheus_client work under gunicorn/uvicorn workers: PROMETHEUS_MULTIPROC_DIR, MultiProcessCollector, gauge modes, worker exit hooks, and its limitations."
sources: ["https://prometheus.github.io/client_python/multiprocess/", "https://github.com/prometheus/client_python"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Python client multiprocess mode

Problem: with N gunicorn workers each process has its own registry; each scrape hits a random worker and
counters jump around. Multiprocess mode makes each worker write to mmap files that one collector aggregates.

## Setup
Set the variable from the start-up script, not from Python, and before `prometheus_client` is imported (the client picks its
storage class at import time).
```bash
export PROMETHEUS_MULTIPROC_DIR=$(mktemp -d)           # must exist, be empty at start, writable: a fresh directory per run
gunicorn -c gunicorn_conf.py app:app
```
```python
# gunicorn_conf.py
from prometheus_client import multiprocess
def child_exit(server, worker):
    multiprocess.mark_process_dead(worker.pid)       # clean up live-gauge files of dead workers
```
```python
# metrics endpoint (e.g. Flask route or separate port)
from prometheus_client import CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST, multiprocess
def metrics():
    registry = CollectorRegistry()                   # fresh registry per request, NOT the default one
    multiprocess.MultiProcessCollector(registry)
    return generate_latest(registry), 200, {"Content-Type": CONTENT_TYPE_LATEST}
```

## Gauges
Declare how to combine per-process values. The default is `all`: one series per process labelled `pid` (a plain `Gauge`
returned `gdefault{pid="..."}` three times in the test):
```python
Gauge("inflight_requests", "In flight", multiprocess_mode="livesum")   # sum of live processes
# all | liveall (per-pid series) | min | max | sum | livesum | mostrecent | livemostrecent
```

## Limitations
- No custom collectors / `*_created`, no exemplars, no `Info`/`Enum` metrics in multiprocess mode (creating them does not
  raise: they are silently absent from the output). Gauges cannot use `set_function`, and the Pushgateway cannot be used.
- Default process/platform collectors don't work (they'd report the scraping process only).
- `mark_process_dead` only deletes the `live*` gauge files of a dead worker; its counter, histogram and other gauge files stay on
  purpose (totals survive restarts), so the directory grows with worker churn. Wipe it at start.
- Any multi-process setup works the same way as long as every process sees the same directory (the test used
  `multiprocessing` spawn workers; gunicorn itself does not run on Windows).
- Alternative: run one worker per container and scale pods.

## Verify
- [ ] Repeated `curl /metrics` shows monotonically increasing counters (not jumping between workers).
- [ ] `ls $PROMETHEUS_MULTIPROC_DIR` contains `counter_<pid>.db` and `gauge_<mode>_<pid>.db` files; after a restart that wipes the directory only current workers' files exist.

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), prometheus_client 0.26.0 on Python 3.14, client_golang 1.25.0 on Go 1.26.
- Three spawned worker processes each created a Counter, Gauges (`livesum`, `max`, default), an Info and an Enum with `PROMETHEUS_MULTIPROC_DIR` set; a fresh `CollectorRegistry` plus `MultiProcessCollector` returned `reqs_total 6` (1+2+3), `inflight_requests 6`, `gmax 3`, one `gdefault{pid=...}` series per worker, and no Info/Enum or `_created` output, with no exception on creating them. The directory held `counter_<pid>.db`, `gauge_all_<pid>.db`, `gauge_livesum_<pid>.db`, `gauge_max_<pid>.db`.
- `multiprocess.mark_process_dead(pid)` for each pid removed only `gauge_livesum_*.db`; `livesum` disappeared from the output and counters stayed.
- Limitations list, the gunicorn `child_exit` hook, the 'set the variable from a start-up script' and 'wipe before startup' advice, and the Gauge mode list: client_python multiprocess documentation (docs/content/multiprocess in prometheus/client_python). Gunicorn was not run (no Linux host). `mktemp -d` ran in Git Bash. The storage class is chosen at import (`values.py`).
