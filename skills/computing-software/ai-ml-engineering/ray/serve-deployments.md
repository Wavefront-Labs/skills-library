---
id: computing-software.ai-ml-engineering.ray.serve-deployments
name: serve-deployments
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, serve-deployment, serve-run, ray-serve, serve-replicas]
level: practitioner
status: docs-checked
description: "Define Ray Serve deployments with @serve.deployment, num_replicas, ray_actor_options, bind, serve.run and the HTTP endpoint."
sources:
  - https://docs.ray.io/en/latest/serve/key-concepts.html
  - https://docs.ray.io/en/latest/serve/getting_started.html
  - https://docs.ray.io/en/latest/serve/configure-serve-deployment.html
  - https://docs.ray.io/en/latest/serve/http-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serve deployments

```python
from ray import serve
from starlette.requests import Request

@serve.deployment(num_replicas=2, ray_actor_options={"num_cpus": 1, "num_gpus": 0.5},
                  max_ongoing_requests=16)
class Model:
    def __init__(self, path: str):
        self.m = load(path)                       # load() is your own loader
    async def __call__(self, request: Request):
        body = await request.json()
        return {"y": self.m.predict(body["x"])}

app = Model.bind("<MODEL_PATH>")                  # constructor args go in bind()
serve.run(app, name="m", route_prefix="/predict")
```
```bash
serve run module:app          # CLI equivalent; import path is module:application
serve status
```

## Facts from the docs
- A deployment is a Python class or function; `bind` with optional constructor arguments defines an application, which `serve.run` (or `serve run`) deploys. The deployment passed to `serve.run` is the ingress deployment, exposed over HTTP.
- `ray_actor_options` accepts `accelerator_type`, `memory`, `num_cpus`, `num_gpus`, `object_store_memory`, `resources`, `runtime_env`. `num_gpus` and `num_cpus` may be fractions to pack replicas on a machine.
- `num_replicas` defaults to 1 (or `"auto"` for autoscaling). `max_ongoing_requests` defaults to 5 (changed from 100 in Ray 2.32.0). `max_queued_requests` defaults to -1 (no limit); past a set limit handles raise BackPressureError and HTTP returns 503.
- HTTP requests to the route go to `__call__` with a Starlette `Request`; return any JSON-serializable object or a Starlette `Response`. `route_prefix` (default `/`) can be set in `serve.run()` or the config file.
- The HTTP proxy port defaults to 8000 and host to `0.0.0.0` (set in the Serve config `http_options`).
- Health checks: define `check_health` on the class to raise when unhealthy; `health_check_period_s` defaults to 10 and `health_check_timeout_s` to 30.

## Verify
`serve status` shows the application and replicas `RUNNING`; a POST to the route returns predictions.

## Checked
2026-11-03. Confirmed in Ray repo docs `serve/key-concepts.md`, `getting-started.md`, `configure-serve-deployment.md`, `http-guide.md`, `production-guide/config.md`. Removed: `serve.start(http_options=...)` snippet, `serve shutdown -y`, `max_concurrent_queries` rename note, unconfirmed curl command, replica-per-actor and `__init__` once-per-replica commentary.
Method: documentation only; no commands were run.
