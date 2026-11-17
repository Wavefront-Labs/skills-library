---
id: computing-software.ai-ml-engineering.ray.named-and-detached-actors
name: named-and-detached-actors
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, detached-actor, named-actor, get-actor, actor-lifetime]
level: practitioner
status: docs-checked
description: "Create named and detached Ray actors, look them up with ray.get_actor, control lifetime and namespaces, and clean up with ray.kill."
sources:
  - https://docs.ray.io/en/latest/ray-core/actors/named-actors.html
  - https://docs.ray.io/en/latest/ray-core/actors/actor-lifetime.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Named and detached actors

```python
Registry.options(name="registry", namespace="svc", lifetime="detached").remote()
# later, from any driver/job in the same cluster
h = ray.get_actor("registry", namespace="svc")
ray.get(h.register.remote("worker-1"))
ray.kill(h)                                  # detached actors must be killed explicitly

Registry.options(name="r2", get_if_exists=True).remote()   # get or create (idempotent)
```
- Named, non-detached: you can retrieve it only while the original driver is running; Ray still garbage-collects it when no handles exist.
- `lifetime="detached"`: survives the driver that created it and is not garbage-collected; destroy it with `ray.kill`, after which the name can be reused.

## Gotchas
- Names are unique within a namespace; creating a duplicate raises `ActorAlreadyExistsError` unless `get_if_exists=True` (then Ray returns the existing actor and ignores the constructor arguments).
- Without a namespace Ray uses an anonymous one per job; other jobs find the actor only by passing the same `namespace=` to `ray.init` or `ray.get_actor`.
- Detached actors are not garbage-collected and have no owner, so Ray keeps restarting them (if `max_restarts` is set) even after their creator dies.
- `ray.get_actor` raises `ValueError` if the named actor does not exist; it times out after 60 s (`RAY_gcs_server_request_timeout_seconds`).

## Verify
Start Python in a second process with `ray.init(address="auto", namespace="svc")` and `ray.get_actor("registry")` returns a working handle.

## Checked
2026-11-03: checked against the Ray docs source `core/actors/named-actors.md`, `core/actors/terminating-actors.md`, `core/fault-tolerance/actors.md` and the `ray.get_actor` docstring and actor-creation code in `python/ray/_private/worker.py` and `python/ray/actor.py`. Fixed: a duplicate name raises `ActorAlreadyExistsError`, not `ValueError`. Removed the unsourced `--filter` command and runtime-env claims.
Method: documentation only; no commands were run.
