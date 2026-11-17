---
id: computing-software.ai-ml-engineering.ray.serve-fastapi-ingress
name: serve-fastapi-ingress
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, serve-ingress, fastapi-serve, serve-http, serve-streaming]
level: practitioner
status: docs-checked
description: "Expose Ray Serve with FastAPI routes using @serve.ingress, route_prefix layering, StreamingResponse and client-disconnect cancellation."
sources:
  - https://docs.ray.io/en/latest/serve/http-guide.html
  - https://docs.ray.io/en/latest/serve/model_composition.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FastAPI ingress

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from ray import serve

api = FastAPI()

class Req(BaseModel):
    text: str

@serve.deployment(num_replicas=2)
@serve.ingress(api)
class Service:
    def __init__(self): self.m = load()           # load() is your own loader
    @api.post("/classify")
    async def classify(self, r: Req):
        return {"label": self.m(r.text)}
    @api.get("/stream")
    async def stream(self, q: str):
        async def gen():
            async for tok in self.m.generate(q): yield tok
        return StreamingResponse(gen(), media_type="text/plain")

app = Service.bind()
serve.run(app, route_prefix="/svc")               # routes are /svc/classify, /svc/stream
```

## Facts from the docs
- `@serve.ingress(app)` wraps a FastAPI app so a deployment gets its full feature set (variable routes, type validation, dependency injection). Put `@serve.deployment` outermost, `@serve.ingress` beneath it, as in the docs' examples.
- Serve's `route_prefix` still applies: with `route_prefix=/my_app` and `@app.get("/fetch_data")`, call `/my_app/fetch_data`.
- Without FastAPI, requests to the route reach `__call__` with a Starlette `Request`.
- Streaming over HTTP: return a `StreamingResponse` wrapping a generator, supported for `__call__` ingress and FastAPI. With an async generator, a client disconnect cancels it (`asyncio.CancelledError`), but only at an `await` inside the generator.
- Handle-level streaming (not HTTP): the method must be a generator and the caller sets `handle.options(stream=True)`, which returns a `DeploymentResponseGenerator`.
- Add middleware on the FastAPI app passed to `@serve.ingress`; `HTTPOptions.middlewares` is deprecated.
- A custom `check_health` method on the class raises when the replica is unhealthy.

## Verify
POST to `<route_prefix>/classify` with a JSON body and check the JSON reply.

## Checked
2026-11-03. Confirmed in Ray repo docs `serve/http-guide.md` (plus its `doc_code/http_guide/http_guide.py` decorator order) and `serve/model-composition.md`. Removed: the `/docs` Swagger claim, `/healthz` route, shared-app and `self` binding statements, gRPC `grpc_options` note, `serve.run` empty-arg remark.
Method: documentation only; no commands were run.
