---
id: computing-software.qa-testing-engineering.performance-testing.locust-tasksets-and-weights
name: locust-tasksets-and-weights
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [taskset, sequentialtaskset, task-weights, user-behaviour-model, locust-tasks]
level: practitioner
status: verified
description: "Model user behaviour in Locust with task weights, TaskSet nesting, SequentialTaskSet ordered flows, interrupt(), on_start/on_stop and multiple weighted User classes."
sources:
  - https://docs.locust.io/en/stable/writing-a-locustfile.html#tasks
  - https://docs.locust.io/en/stable/tasksets.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TaskSets, SequentialTaskSet and task weights

## Weights on tasks
```python
class Shopper(HttpUser):
    wait_time = between(1, 5)
    @task(10)
    def browse(self): self.client.get("/products")
    @task(3)
    def view(self): self.client.get("/products/1", name="/products/:id")
    @task(1)
    def checkout(self): ...
```
Each loop picks a task randomly in proportion to weight (10:3:1). A 6 s run with these weights logged 235, 72 and 25 requests (10 : 3.06 : 1.06).

## Weights on User classes (mix of personas)
```python
class Browser(HttpUser):  weight = 8; ...
class Buyer(HttpUser):    weight = 2; ...
class Admin(HttpUser):    fixed_count = 1; ...    # exactly one, regardless of total users (a 20-user run still had one Admin)
```

## TaskSet (grouped behaviour)
```python
class Forum(TaskSet):
    @task(5)
    def read(self): self.client.get("/forum")
    @task(1)
    def leave(self): self.interrupt()        # return control to the parent
class Visitor(HttpUser):
    tasks = {Forum: 2, Shop: 1}
```
Without `interrupt()`, a user entering a TaskSet stays there forever (in a run, users that entered a TaskSet with no `interrupt()` kept hitting only its endpoint: 3,188 requests vs 151 for the sibling that could leave). `tasks` accepts a list or a dict of `{TaskSetOrFunction: weight}`.

## SequentialTaskSet (ordered journey)
```python
class Checkout(SequentialTaskSet):
    def on_start(self): self.client.post("/login", json=creds())
    @task
    def add(self): self.client.post("/cart", json={"sku": "A1"})
    @task
    def pay(self): self.client.post("/pay", json={...})
    @task
    def done(self): self.interrupt(reschedule=False)
class Buyer(HttpUser):
    tasks = [Checkout]
```
Tasks run in declaration order; `wait_time` applies between each. After the last task calls `interrupt(reschedule=False)` the TaskSet is entered again, so `on_start` (the login here) ran once per loop: 370 logins for 369 carts and 368 payments in a run.

## Mapping to a workload model
Derive weights from production analytics (page views per journey). Check the resulting request mix in Locust stats against the model; adjust.

## Gotchas
- Wait time between every task means a 6-step journey with `between(1,5)` takes ~18s plus response times: account for this when targeting RPS.
- `@task` on a method of `User` vs `TaskSet` share syntax but TaskSet methods reach the user via `self.user`.

## Verify
After a run, request counts per endpoint match the planned ratios within a few percent.

## Checked
Locust 2.47.0, Windows scratch venv, local HTTP server.
- Run: User classes `Visitor` (`tasks = {Forum: 2, Shop: 1}`, `weight = 8`), `Buyer` (`SequentialTaskSet` with `on_start` login, `add`, `pay`, `done` with `interrupt(reschedule=False)`), `Admin` (`fixed_count = 1`) and an abstract-base weighted class (`@task(10)`, `@task(3)` with `name="/products/:id"`, `@task(1)`) with 20 users for 6 s: request counts quoted in the body; `self.user.client` from inside a TaskSet worked; `name=` grouped the dynamic URL; the fixed_count class had a single user.
- Arithmetic: between(1,5) averages 3 s, so 6 tasks give about 18 s of waiting, as stated.
- Fetched: docs.locust.io tasksets and writing-a-locustfile pages (task weights, interrupt, SequentialTaskSet, `wait_time` helpers including `constant_pacing` and `constant_throughput`).
