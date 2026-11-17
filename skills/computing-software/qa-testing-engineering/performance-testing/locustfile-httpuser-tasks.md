---
id: computing-software.qa-testing-engineering.performance-testing.locustfile-httpuser-tasks
name: locustfile-httpuser-tasks
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [locustfile, locust, httpuser, wait-time, load-testing]
level: practitioner
status: verified
description: "Write a Locust locustfile: HttpUser with host and wait_time, weighted @task methods, TaskSets, on_start login, catch_response validation and name grouping."
sources:
  - https://docs.locust.io/en/stable/writing-a-locustfile.html
  - https://docs.locust.io/en/stable/api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing a locustfile (HttpUser, tasks, wait_time)

```python
import random
from locust import HttpUser, task, between, tag

class Shopper(HttpUser):
    host = "https://staging.example.test"           # overridable with --host
    wait_time = between(2, 6)                        # think time between tasks; constant(1), constant_pacing(10), constant_throughput(0.5)
    weight = 3                                       # 3 shoppers per 1 admin when several user classes

    def on_start(self):                              # once per simulated user
        r = self.client.post("/api/login", json={"email": "load+%d@example.test" % id(self), "password": "pw"})
        self.client.headers["Authorization"] = f"Bearer {r.json()['token']}"

    @task(10)
    def browse(self):
        self.client.get("/api/products?page=1")

    @task(3)
    def view_product(self):
        pid = random.randint(1, 500)
        self.client.get(f"/api/products/{pid}", name="/api/products/:id")   # group in stats

    @tag("checkout")
    @task(1)
    def checkout(self):
        with self.client.post("/api/checkout", json={"sku": "SKU-1"}, catch_response=True) as r:
            if r.status_code != 201 or "orderId" not in r.text:
                r.failure(f"checkout failed: {r.status_code}")
            elif r.elapsed.total_seconds() > 2:
                r.failure("checkout too slow")

class Admin(HttpUser):
    weight = 1
    wait_time = between(5, 15)
    @task
    def report(self):
        self.client.get("/admin/api/reports/daily")
```

## Concepts
- `@task(weight)`: random task selection proportional to weights.
- `SequentialTaskSet` for ordered flows; `TaskSet` with `self.interrupt()` for nested behaviour.
- `self.client` is a requests-based session (cookies persist per user, as the docs state). `FastHttpUser` (geventhttpclient) can reach up to 5x-6x more requests per second on the same hardware (docs figure, best case).
- Tags: run subsets with `--tags checkout` / `--exclude-tags`.
- Events: `@events.test_start.add_listener` for global setup; `@events.request.add_listener` for custom logging.

## Run
```bash
locust -f locustfile.py            # web UI at http://localhost:8089
locust -f locustfile.py Shopper     # only one user class
locust -f locustfile.py -l          # list the User classes and exit
```
Without `import random`, the `view_product` task raises `NameError: name 'random' is not defined` on every call (the original snippet lacked the import).

## Gotchas
- Locust is single-core per process: use `--processes -1` (2.20+) or distributed workers for more load.
- Wait times model a closed workload; for fixed throughput use `constant_throughput` and watch whether it is achieved.
- Unique dynamic URLs without `name=` flood the stats table.

## Verify
Task ratios in the stats match intended weights, failures from catch_response show in the Failures tab, and URLs are grouped.

## Checked
Locust 2.47.0, Windows scratch venv, local HTTP server returning a token for `/api/login`, 201 with `orderId` for `/api/checkout`.
- Run: the full Shopper/Admin file (with host overridden to the local server and shorter waits): without `import random` every `view_product` call raised NameError; with it the run succeeded, `--tags checkout` ran only login plus checkout, `name="/api/products/:id"` grouped dynamic URLs, `catch_response` with `r.elapsed.total_seconds()` ran, `-l` listed `Shopper` and `Admin`, and `locust ... Admin` selects one class (positional class names, as used in other runs).
- Fetched: docs.locust.io writing-a-locustfile page (cookies kept, HttpSession like requests.Session, wait_time helpers `between`, `constant`, `constant_pacing`, `constant_throughput`) and increase-performance page (5x-6x).
