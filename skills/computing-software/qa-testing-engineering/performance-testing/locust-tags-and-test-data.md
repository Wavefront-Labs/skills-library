---
id: computing-software.qa-testing-engineering.performance-testing.locust-tags-and-test-data
name: locust-tags-and-test-data
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [locust-tags, locust-test-data, per-user-data, tag-filtering]
level: practitioner
status: verified
description: "Select Locust tasks with @tag and --tags/--exclude-tags, and give each simulated user unique test data via on_start, iterators and distributed-safe data assignment."
sources:
  - https://docs.locust.io/en/stable/writing-a-locustfile.html#tag-decorator
  - https://docs.locust.io/en/stable/running-distributed.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tags and per-user test data

## Tags
```python
from locust import HttpUser, task, tag

class Api(HttpUser):
    @tag("smoke", "read")
    @task
    def health(self): self.client.get("/health")

    @tag("write")
    @task
    def create(self): self.client.post("/orders", json={...})
```
```bash
locust -f api.py --tags smoke             # only smoke tasks
locust -f api.py --exclude-tags write     # everything except writes (e.g. against prod)
```
Tags on a TaskSet class apply to its tasks (`@tag("grp")` on a TaskSet ran with `--tags grp` and was filtered out by `--tags other`). Several tags after `--tags` select tasks that carry any of them, and an excluded tag always wins over an included one (writing-a-locustfile docs).

## Per-user data
```python
import csv, itertools, threading
from locust import HttpUser
with open("users.csv") as f:
    USERS = list(csv.DictReader(f))
_cycle = itertools.cycle(USERS)
_lock = threading.Lock()   # greenlets switch only on I/O, but keep it explicit

class Shopper(HttpUser):
    def on_start(self):
        with _lock:
            self.account = next(_cycle)
        self.client.post("/login", json={"user": self.account["email"], "pass": self.account["password"]})
```

## Distributed runs
Each worker loads the file independently, so worker 1 and worker 2 both start at row 0 and collide. Options:
- Partition by worker index: `self.environment.runner.worker_index` (set on a WorkerRunner). A worker has no `worker_count` attribute (only the master and local runner do), so have the master send the count with `runner.send_message("cfg", {"count": runner.worker_count})` and slice `rows[worker_index::count]` in the worker's handler (see the distributed-locust skill; with 2 workers they got even and odd rows).
- Master hands out data via custom messages (`runner.send_message("data", rows, client_id)`).
- Generate unique values instead (`uuid4()` emails) when the system allows sign-ups.

## Data volume
Total unique records needed ≈ users (for per-user identities) or rate x duration (for one-time-use records like coupons).

## Gotchas
- Reading a large CSV in every user's `on_start` multiplies memory: load once at module level.
- `--tags` with no matching tasks gives users with nothing to do: Locust logs "Api had no tasks left after filtering, instantiating it will fail!" and each user raises "No tasks defined on Api".

## Verify
Server logs show distinct accounts per user and no "already logged in" or duplicate-key errors across workers.

## Checked
Locust 2.47.0, Windows scratch venv, local HTTP server.
- Run: `--tags smoke` ran only `/health`, `--exclude-tags write` ran only `/health`, and the no-match case produced the two quoted messages. The CSV/`itertools.cycle` account assignment with a lock gave 4 users the accounts a, b, c, a; TaskSet-level `@tag`. Worker slicing via custom message across two workers (indexes 0 and 1) from the distributed run; `worker_count` absent on `WorkerRunner` and defined on the local runner in the installed source.
- Fetched: docs.locust.io running-distributed page (custom message API, `-f -`) and writing-a-locustfile page (tag selection rules); the changelog entry that added `worker_index` (2.11.0).
