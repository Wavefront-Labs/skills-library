---
id: computing-software.ai-ml-engineering.ray.debugging-and-logs
name: debugging-and-logs
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, ray-logs, ray-debugger, worker-logs, log-to-driver, state-api]
level: practitioner
status: docs-checked
description: "Find and read Ray logs with ray logs, the state CLI, log_to_driver, LoggingConfig, log dedup and session_latest paths, and use breakpoint() with pdb."
sources:
  - https://docs.ray.io/en/latest/ray-observability/user-guides/cli-sdk.html
  - https://docs.ray.io/en/latest/ray-observability/user-guides/configure-logging.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging and logs

```bash
ray logs cluster                         # list log files
ray logs gcs_server.out --node-id <id>   # glob names; head node by default, not a dead node
ray logs raylet.out --node-ip <ip> --follow
ray logs actor --id <ACTOR_ID> --follow
ray logs worker --pid <PID> --follow
ray list tasks -f state=RUNNING           # -f/--filter; also ray list actors, add --detail
ray get tasks <TASK_ID>
ray summary tasks
ls /tmp/ray/session_latest/logs/         # worker-*.out/err, raylet.out, gcs_server.out ...
```
```python
ray.init(log_to_driver=False)            # stop routing worker logs to the driver (large-scale runs)
ray.init(logging_config=ray.LoggingConfig(encoding="JSON", log_level="INFO"))   # TEXT is the default encoding
```
Debugging:
```python
@ray.remote
def f(x):
    breakpoint()                          # Ray integrates with pdb; see the Ray Debugger docs to attach
```
`ray.init(local_mode=True)` is no longer supported; use the Ray debugger for interactive debugging.

## Gotchas
- `ray logs` cannot read the logs of a dead node, and prints the head node's by default; without `--tail` output is truncated to the last 1000 lines.
- Worker output reaches the driver with a prefix such as `(f pid=1574323)` or `(Actor pid=480956)`; `RAY_DISABLE_WORKER_LOG_PREFIX=1` removes it.
- Ray deduplicates repeated worker lines (`[repeated Nx across cluster]`); `RAY_DEDUP_LOGS=0` turns it off, `RAY_DEDUP_LOGS_ALLOW_REGEX` and `RAY_DEDUP_LOGS_SKIP_REGEX` select lines. Set `RAY_DEDUP_LOGS=0` too when you want line-oriented structured logs.
- Ray usually clears the temp directory when machines reboot, so logs are lost when nodes stop; persist them if you need them later (see the Ray log persistence docs).
- `RayTaskError` wraps the task's exception; read `e.cause` for the original.

## Verify
`ray logs worker --pid <PID> --tail 50` prints the task's output and `ray list tasks -f state=FAILED` lists failed tasks.

## Checked
2026-11-03: checked against the Ray docs source `ray-observability/user-guides/cli-sdk.md`, `configure-logging.md` and `debug-apps/debug-failures.md`, and the `ray.init` docstring in `python/ray/_private/worker.py`. Fixed: `ray logs actor` takes `--id`, not `--actor-id`; `local_mode` is no longer supported. Removed the unsourced `ray debug`, `RAY_DEBUG_POST_MORTEM`, `f._function`, `traceback_str` and Kubernetes claims.
Method: documentation only; no commands were run.
