---
id: computing-software.qa-testing-engineering.performance-testing.locust-fasthttpuser
name: locust-fasthttpuser
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [fasthttpuser, geventhttpclient, locust-throughput, generator-efficiency]
level: practitioner
status: verified
description: "Use Locust FastHttpUser (geventhttpclient) for 4-6x more requests per core, its API differences from HttpUser, connection settings and when the requests-based client is better."
sources:
  - https://docs.locust.io/en/stable/increase-performance.html
  - https://docs.locust.io/en/stable/api.html#fasthttpuser-class
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FastHttpUser for high throughput

The default `HttpUser` wraps `requests` (feature-rich, slower). `FastHttpUser` uses `geventhttpclient`: Locust docs report sometimes as much as 5x-6x the requests per second on the same hardware (a best case of about 16000 vs 4000 requests/s per process on one core), which means fewer generator machines for the same load. FastHttpUser does not make individual requests faster. On this review machine, 20 users with no wait time against a local Python server for 8 s sent 40,033 requests with FastHttpUser vs 15,599 with HttpUser (about 2.6x; the server and Windows limit the ratio).

```python
from locust import FastHttpUser, task, between

class Shopper(FastHttpUser):
    wait_time = between(1, 3)
    connection_timeout = 10.0
    network_timeout = 30.0
    concurrency = 10          # max concurrent connections per user (for client.request in greenlets)
    insecure = False          # default True skips TLS certificate verification; False verifies

    @task
    def browse(self):
        with self.client.get("/api/products", catch_response=True, name="products") as r:
            if r.status_code != 200 or not r.json():
                r.failure(f"bad response {r.status_code}")

    @task
    def add_to_cart(self):
        with self.rest("POST", "/api/cart", json={"sku": "A1"}) as r:   # JSON helper with validation
            if r.js is None or "id" not in r.js:
                r.failure("no cart id")
```

## Differences from HttpUser
- Response object is `FastResponse`: `.status_code`, `.text`, `.content`, `.json()`, `.headers` (similar, not identical; no `requests` adapters/hooks).
- `self.rest(...)` context manager parses JSON into `r.js`, marks the request failed on invalid JSON or an exception inside the block, defaults `Content-Type` and `Accept` to JSON and sets `catch_response=True` (always use `with`). It is also available on `HttpUser`; the docs call it new and subject to change.
- Do not name a task `rest`: the method shadows `self.rest` and `self.rest("POST", ..., json=...)` raises `TypeError: ... unexpected keyword argument 'json'`.
- Some `requests` features (session adapters, certain auth plugins, streaming quirks) are missing.

## When to keep HttpUser
Low-volume tests where convenience wins, or flows relying on `requests` extensions (e.g. `requests-ntlm`).

## Generator sizing
Locust is single-core per process: use `--processes -1` (one per core) or workers. Watch the "CPU usage above 90%" warning: numbers past that point are generator-bound.

## Gotchas
- Mixed classes (HttpUser + FastHttpUser) run side by side in one test (both showed requests), but per-request overhead is uneven.
- Defaults on the class: `connection_timeout` 60 s, `network_timeout` 60 s, `concurrency` 10, `insecure = True`, `max_redirects` 30, `max_retries` 0 (installed source), so the values in the example override them.
- Many users x keep-alive = many open sockets: raise the OS open-file limit on the generator (the k6 large-test guide suggests `ulimit -n 250000` on Linux for very large tests).

## Verify
Same scenario at equal user count: CPU per generator drops markedly and RPS per core rises compared with HttpUser.

## Checked
Locust 2.47.0 (geventhttpclient 2.6.1), Windows scratch venv, local HTTP server.
- Run: the full snippet (with the task renamed) against a local server: `GET products` via `client.get(..., catch_response=True, name=...)` and `POST /api/cart` via `self.rest(...)` with `r.js` checks, 0 failures; the original task name `rest` produced the TypeError quoted above on every call; the same flow on `HttpUser` also ran (confirms `self.rest` exists there). HttpUser vs FastHttpUser 8 s comparison and a mixed-class run. Class attribute defaults read from `locust/contrib/fasthttp.py`.
- Fetched: docs.locust.io increase-performance page (5x-6x, 16000 vs 4000 requests/s figure, REST helper behaviour), API page (`FastHttpSession` `insecure=True` default), k6 running-large-tests page (`ulimit -n 250000`).
