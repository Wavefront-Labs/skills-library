---
id: computing-software.qa-testing-engineering.performance-testing.locust-custom-load-shapes
name: locust-custom-load-shapes
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [loadtestshape, locust, load-profile, spike-testing, step-load]
level: practitioner
status: verified
description: "Define custom Locust load profiles with LoadTestShape: tick() returning users and spawn rate, staged, step and spike shapes, per-user-class counts, and stopping the test."
sources:
  - https://docs.locust.io/en/stable/configuration.html#custom-load-shapes
  - https://docs.locust.io/en/stable/api.html#locust.LoadTestShape
  - https://github.com/locustio/locust/tree/master/examples/custom_shape
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom load shapes (Locust)

**Goal:** time-based load profiles (ramp, hold, spike, steps) defined in code instead of a fixed `-u`/`-r`.

## Staged shape
```python
from locust import LoadTestShape

class StagesShape(LoadTestShape):
    stages = [
        {"duration": 300,  "users": 200, "spawn_rate": 2},    # until t=300s ramp to 200
        {"duration": 1800, "users": 200, "spawn_rate": 2},    # hold until t=1800s
        {"duration": 1920, "users": 800, "spawn_rate": 50},   # spike
        {"duration": 2100, "users": 200, "spawn_rate": 50},   # recover
        {"duration": 2400, "users": 0,   "spawn_rate": 10},
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]
        return None          # returning None stops the test
```
Having a `LoadTestShape` subclass in the locustfile activates it automatically; `-u`, `-r`, `-t` are ignored (Locust logs a warning naming them, unless the shape class reads them itself). There is no `--shape` flag: with several shape classes use `--class-picker` and choose in the web UI, or keep each shape in its own file and pass only that file with `-f`. A base class meant only for subclassing needs `abstract = True`.
In a run of the staged shape (durations scaled to 3/6/8 s) the log showed "Shape test updating to 4 users", then 8, then 2, then "Shape test completed, shutting down" after `tick()` returned None.

## Step load (find the knee)
```python
class StepShape(LoadTestShape):
    step_users, step_time, max_users = 100, 300, 1000
    def tick(self):
        t = self.get_run_time()
        users = min(self.max_users, (int(t // self.step_time) + 1) * self.step_users)
        return (users, self.step_users) if t < self.step_time * (self.max_users // self.step_users + 1) else None
```

## Per user class (2.12+)
`return (200, 10, [Shopper, Admin])` restricts which user classes run in this stage (a `(4, 4, [A])` stage with classes A and B spawned `{"A": 4, "B": 0}`). Shapes can also call `self.get_current_user_count()` (documented) to wait until the previous stage's users are all spawned.

## Gotchas
- `spawn_rate` too high overloads the generator at spike start; check worker CPU.
- Shapes work in distributed mode; the master runs `tick()` (a master plus one worker ran the staged shape; the shape lines appear only in the master log).
- `get_run_time()` returns seconds since the test start and `reset_time()` sets the start back to 0 (API docs); call it deliberately.

## Verify
Users-over-time chart in the UI/CSV matches the stage table, and the test ends when tick returns None.

## Checked
Locust 2.47.0, Windows scratch venv, local HTTP server.
- Run: staged shape with scaled durations (log lines for 4, 8, 2 users and clean shutdown on None; `-u 100 -r 100 -t 4s` produced the warning "The following option(s) will be ignored: --users, --spawn-rate, --run-time"); step shape (2, 4, 6 users, ends after the last step); `(users, rate, [ClassA])` tuple spawned only ClassA; shape in distributed mode (master ticks, worker follows); `locust --help` has no `--shape` option, only `--class-picker`.
- Fetched: docs.locust.io configuration page (custom load shapes section, `abstract = True`, class picker), API page (`LoadTestShape.get_current_user_count`, `reset_time`, `tick` return values) and the changelog (shape user classes added in 2.12.0). The old `custom-load-shape.html` source URL returns 404 and was replaced.
