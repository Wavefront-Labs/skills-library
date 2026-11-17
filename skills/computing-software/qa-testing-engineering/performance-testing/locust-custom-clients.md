---
id: computing-software.qa-testing-engineering.performance-testing.locust-custom-clients
name: locust-custom-clients
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [locust-custom-client, non-http-load-testing, grpc-locust, locust-user-class]
level: practitioner
status: verified
description: "Load-test non-HTTP systems with Locust by writing a custom User and client that fire request events: gRPC, databases, message queues, WebSockets, with gevent compatibility."
sources:
  - https://docs.locust.io/en/stable/testing-other-systems.html
  - https://docs.locust.io/en/stable/api.html#user-class
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing non-HTTP systems with custom User clients

Locust measures anything that reports timings via `events.request.fire`. Pattern: wrap the client, time each call, fire the event.

```python
import time
from locust import User, task, between, events
import sqlite3   # stand-in driver; swap in a gevent-friendly driver (see below)

class TimedDb:
    def __init__(self, dsn, env):
        self.conn = sqlite3.connect(dsn, check_same_thread=False)
        self.conn.execute("create table if not exists orders(user_id int, v int)")
        self.env = env

    def query(self, name, sql, *args):
        start = time.perf_counter()
        exc = None
        try:
            cur = self.conn.cursor()
            cur.execute(sql, args)
            rows = cur.fetchall()
        except Exception as e:
            exc, rows = e, []
        self.env.events.request.fire(request_type="sql", name=name,
                                     response_time=(time.perf_counter() - start) * 1000,
                                     response_length=len(rows), exception=exc, context={})
        return rows

class DbUser(User):
    abstract = False
    wait_time = between(0.5, 1)
    def on_start(self): self.db = TimedDb(self.host, self.environment)
    @task
    def orders(self): self.db.query("orders_by_user", "select * from orders where user_id=?", 42)
```
Run: `locust -f db_locust.py --headless -u 2 -r 2 -t 10s --host ":memory:"`; `--host` reaches `self.host` on a plain `User`. The stats table then shows a `sql` row per `name` (a deliberately bad query shows 100% failures through the `exception` argument). For PostgreSQL swap the driver: psycopg 3 uses `%s` placeholders and `psycopg.connect(dsn, autocommit=True)` (psycopg docs params page and the installed `Connection.connect(conninfo, *, autocommit=...)` signature confirm both).

## gevent compatibility (critical)
Locust runs users as greenlets. Blocking C-extension clients (many DB drivers, some gRPC builds) block the whole process: one slow call stalls all users and timings become meaningless. Options:
- Use libraries that support gevent monkey-patching (pure-Python sockets); the docs say C libraries doing their I/O in compiled code block the whole process, in practice limiting you to one User per worker process.
- `grpc` needs `grpc.experimental.gevent.init_gevent()` before use (`import grpc.experimental.gevent as grpc_gevent`, as in Locust's gRPC example; the function exists in grpcio 1.84).
- `psycopg2` + `psycogreen.gevent.patch_psycopg()` (psycogreen imports psycopg2, so it fails without it).
- psycopg 3 needs no psycogreen: gevent is supported automatically from psycopg 3.1.14 (psycogreen README).
- Otherwise run fewer users per process and more processes.

## Ready-made
Locust core documents gRPC, Socket.IO and MQTT examples (testing-other-systems page). `locust-plugins` adds users for Kafka, Playwright, Selenium/Webdriver and HTTP users that load embedded page resources; its README says its Socket.IO, MQTT and REST users were removed because they moved into Locust core.

## Gotchas
- Fire one event per logical operation; name with low cardinality.
- Connection per user (`on_start`) models clients realistically; a shared connection serialises users.

## Verify
With gevent patched correctly, doubling users roughly doubles throughput until the target saturates (not flat from the start).

## Checked
Locust 2.47.0 in a Windows scratch venv, plus fetched docs.
- Run: the TimedDb/DbUser pattern with `sqlite3` as the driver (no PostgreSQL available here): `sql` rows appeared in the stats table with `orders_by_user` succeeding and a deliberately bad query reported as failures through `events.request.fire(... exception=exc)`; `--host` populated `self.host`. Imported `grpc.experimental.gevent.init_gevent` (grpcio 1.84); `psycogreen.gevent` failed to import without psycopg2 as stated; psycopg 3.3.6 installed.
- Fetched: docs.locust.io testing-other-systems (gevent monkey-patching limits, psycogreen for psycopg2, gRPC/Socket.IO/MQTT sections), psycogreen README (psycopg 3 gevent support from 3.1.14), locust-plugins README (users list, removals).
- psycopg 3: `%s` placeholders confirmed on the psycopg3 params docs page and `autocommit` keyword confirmed in the installed signature; the query loop itself ran with sqlite3 because no PostgreSQL server exists here, so the body does not claim server-side behaviour.
