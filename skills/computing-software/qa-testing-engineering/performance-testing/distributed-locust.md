---
id: computing-software.qa-testing-engineering.performance-testing.distributed-locust
name: distributed-locust
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [locust-distributed, locust, master-worker, kubernetes, load-generation]
level: practitioner
status: verified
description: "Scale Locust across cores and machines: --processes, master and worker nodes, expect-workers, data partitioning per worker, and running on Kubernetes with Helm."
sources:
  - https://docs.locust.io/en/stable/running-distributed.html
  - https://docs.locust.io/en/stable/running-in-docker.html
  - https://github.com/deliveryhero/helm-charts/tree/master/stable/locust
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Distributed Locust (master/workers, Kubernetes)

## One machine, all cores
```bash
locust -f locustfile.py --processes -1        # master plus one worker per logical core (Locust 2.19+)
```
`--processes` relies on `fork()`: it does not work on Windows. On Windows start the master and each worker yourself in separate terminals (below).

## Multiple machines
```bash
# master
locust -f locustfile.py --master --expect-workers 8 --headless -u 4000 -r 100 -t 30m --csv results
# each worker machine (same locustfile and dependencies)
locust -f locustfile.py --worker --master-host 10.0.0.5 --processes -1     # on Windows: omit --processes, run one worker per core
```
Ports: master listens on 5557 for workers and serves the web UI on 8089. Users are spread evenly over workers; master aggregates stats. With `--expect-workers N` and `--headless` the master waits for N workers before starting.
`-f -` on workers (2.23+, single locustfile only) fetches the locustfile from the master.

## Per-worker data
Avoid all workers using the same test accounts:
`worker_index` (0..n-1) exists on a `WorkerRunner`, but `worker_count` does not (it exists on the master and local runner only), so a worker cannot read the count itself. Have the master send it in a custom message:
```python
from locust import events
from locust.runners import MasterRunner, WorkerRunner

ALL = load_accounts()
MINE = []

def on_cfg(environment, msg, **kw):
    MINE[:] = ALL[environment.runner.worker_index::msg.data["count"]]

@events.init.add_listener
def on_init(environment, **kw):
    if not isinstance(environment.runner, MasterRunner):
        environment.runner.register_message("cfg", on_cfg)

@events.test_start.add_listener
def on_start(environment, **kw):
    if not isinstance(environment.runner, WorkerRunner):
        environment.runner.send_message("cfg", {"count": environment.runner.worker_count})
```
With 2 workers the accounts split into even and odd indexes. Messages without `client_id` go to all workers; a handler that runs over a second should be registered with `concurrent=True`.

## Kubernetes
```bash
helm repo add deliveryhero https://charts.deliveryhero.io/
kubectl create configmap my-locustfile --from-file=main.py=locustfile.py   # key must be main.py (chart default loadtest.locust_locustfile)
helm install locust deliveryhero/locust --set loadtest.locust_locustfile_configmap=my-locustfile \
  --set loadtest.locust_host=https://staging.example.test --set worker.replicas=10 \
  --set image.tag=<current-locust-release>     # chart 0.31.6 defaults to locustio/locust:2.15.1, too old for --processes and -f -
```
`helm template` with these values renders a master Deployment with `LOCUST_LOCUSTFILE=/mnt/locust/main.py` and a worker Deployment with 10 replicas that mount the ConfigMap. Or write a plain master Deployment/Service plus a worker Deployment; a Locust Kubernetes operator is also documented.

## Capacity planning for generators
- One worker process saturates ~1 core (the docs advise one worker per core); keep worker CPU well below 90%, where Locust logs a CPU warning (`CPU_WARNING_THRESHOLD = 90` in the source).
- `FastHttpUser` for high RPS.
- Network bandwidth and ephemeral ports on generators can limit before CPU.

## Gotchas
- Workers with different locustfile versions produce mixed behaviour; deploy them from one image.
- Locust percentiles are approximated from rounded response-time buckets (the console table is headed "approximated"); exact high percentiles need raw data from your own request listener.

## Verify
All expected workers connect before the run starts, worker CPU stays under the warning, and achieved RPS scales with worker count.

## Checked
Locust 2.47.0, Windows scratch venv, local stdlib HTTP server; Helm v3.15.2 and kubectl client only (no cluster).
- Run: master `--master --expect-workers 2 --headless -u 20 -r 20 -t 8s --csv` plus two separate `--worker` processes (one with `-f -`, which fetched the locustfile from the master): both connected, 481+ requests aggregated, workers got `worker_index` 0 and 1. `getattr(WorkerRunner, 'worker_count')` was missing and `worker_count` appears in the installed source only on the local runner and master; the message-based split above ran and gave workers the even and odd accounts. `CPU_WARNING_THRESHOLD = 90` read from the installed `locust/runners.py`.
- `helm repo add` (Helm config, cache and data dirs pointed at scratch), `helm search repo` (chart 0.31.6, app version 2.15.1, image.tag default 2.15.1; the Docker Hub tag you pick must be confirmed separately) and `helm template` with the exact `--set` values: ConfigMap name, `LOCUST_HOST`, `LOCUST_LOCUSTFILE=/mnt/locust/main.py`, 10 worker replicas. `kubectl create configmap --dry-run=client` accepted `main.py=<file>`. `helm install` itself needs a cluster.
- Fetched: docs.locust.io running-distributed page (`--processes` uses `fork()` and `-1` auto-detects cores, ports, `-f -` single-file limit, custom messages) and the changelog (`--processes` 2.19.0, locustfile distribution 2.23.0).
