---
id: computing-software.qa-testing-engineering.performance-testing.locust-event-hooks
name: locust-event-hooks
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [locust-events, event-hooks, request-event, custom-listeners, locust-plugins]
level: practitioner
status: verified
description: "Extend Locust with event hooks: request events for custom logging/metrics, test_start/test_stop setup, init for web UI routes, quitting with a failure exit code on SLO breach."
sources:
  - https://docs.locust.io/en/stable/extending-locust.html
  - https://docs.locust.io/en/stable/api.html#event-hooks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event hooks and custom listeners

## Request event (every request, success or failure)
```python
import logging
from locust import events
from locust.runners import WorkerRunner

log = logging.getLogger(__name__)

@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, context, **kw):
    if exception:
        log.warning("FAIL %s %s %.0fms %s", request_type, name, response_time, exception)
```
`context` carries per-user data you set (`self.context()` in the User, or `context={...}` per request), e.g. tenant id, for tagging exported metrics.

## Lifecycle
```python
@events.test_start.add_listener
def on_start(environment, **kw):
    if not isinstance(environment.runner, WorkerRunner):   # only master / standalone
        seed_test_data()

@events.test_stop.add_listener
def on_stop(environment, **kw): cleanup()
```
`test_stop` fires on every process (master and each worker printed it in a distributed run), while `test_start` seeding guarded as above ran on the master only. `init` fires once per process: register web UI extensions (`environment.web_ui.app.route`, guarded with `if environment.web_ui:` because workers and headless runs have no web UI, per the docs), start background greenlets.

## Fail the run on SLO breach
```python
@events.quitting.add_listener
def slo_gate(environment, **kw):
    s = environment.stats.total
    if s.fail_ratio > 0.01 or s.get_response_time_percentile(0.95) > 800:
        log.error("SLO breached: fail %.2f%% p95 %sms", s.fail_ratio * 100, s.get_response_time_percentile(0.95))
        environment.process_exit_code = 1
```

## Custom (non-HTTP) timings into stats
```python
environment.events.request.fire(request_type="db", name="query_orders", response_time=ms,
                                response_length=0, exception=None, context={})
```

## Distributed notes
Request events fire on workers (a failing request was logged by the worker process and not by the master); aggregate stats arrive at the master, so the `quitting` SLO gate above runs on the master where `environment.stats.total` is complete. For custom messages between them: `environment.runner.send_message(...)` and `register_message(...)`.

## Gotchas
- Slow listeners (synchronous HTTP to a metrics backend) block greenlets and distort response times; batch and send in a background greenlet.
- `locust-plugins` provides ready listeners (its README lists a Timescale listener with Grafana dashboards and the checks `--check-rps`, `--check-fail-ratio`, `--check-avg-response-time`).

## Verify
A deliberately slow endpoint makes the run exit with code 1 via the quitting hook (run here with a 300 ms endpoint and a 200 ms p95 gate: log line "SLO breached: fail 55.81% p95 300ms", exit code 1).

## Checked
Locust 2.47.0, Windows scratch venv, local HTTP server with a 300 ms path and a 404 path.
- Run: all four snippets (request listener with `self.context()` returning `{'tenant': 'acme'}` appearing as `context`, `test_start`/`test_stop`, SLO gate on `fail_ratio` and `get_response_time_percentile(0.95)` setting `process_exit_code`) standalone and with a master plus one worker. Standalone: exit code 1 with the gate. Distributed: the FAIL log lines came from the worker only, SEED from the master only, CLEANUP from both, and the SLO error from the master. `StatsEntry.get_response_time_percentile(percent)` signature read from the installed source.
- Fetched: docs.locust.io extending-locust page (web route guard `if environment.web_ui`), locust-plugins README (listeners and `--check-*` flags). The `events.request.fire(...)` custom-timing call was exercised in the custom-clients skill's run.
