---
id: computing-software.ai-ml-engineering.ray.serve-model-composition
name: serve-model-composition
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, deployment-handle, model-composition, serve-bind-graph, handle-remote]
level: practitioner
status: docs-checked
description: "Compose multiple Ray Serve deployments with bind() and DeploymentHandle, await or chain DeploymentResponse objects, and avoid blocking calls."
sources:
  - https://docs.ray.io/en/latest/serve/model-composition.html
  - https://docs.ray.io/en/latest/serve/multi-app.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Model composition

```python
from ray import serve
from ray.serve.handle import DeploymentHandle

@serve.deployment
class Preprocess:
    def run(self, text): return text.lower().split()

@serve.deployment(ray_actor_options={"num_gpus": 1})
class Embed:
    def __call__(self, tokens): return model(tokens)        # model is your own

@serve.deployment
class Ingress:
    def __init__(self, pre: DeploymentHandle, emb: DeploymentHandle):
        self.pre, self.emb = pre, emb                      # bound deployments arrive as handles
    async def __call__(self, request):
        text = (await request.json())["text"]
        tokens = await self.pre.run.remote(text)           # method call, then await the response
        return {"emb": await self.emb.remote(tokens)}      # call the deployment's __call__

app = Ingress.bind(Preprocess.bind(), Embed.bind())
serve.run(app)
```

## Facts from the docs
- Bound deployments passed into another's `bind()` become `DeploymentHandle`s at runtime, so each step scales and is configured independently.
- `handle.remote(...)` (or `handle.method.remote(...)`) returns a `DeploymentResponse`, a future. `await` it inside deployments. `.result()` works too but blocks the replica, so avoid it inside a deployment.
- A `DeploymentResponse` can be passed straight into another handle call as a top-level argument or keyword: Serve awaits it and passes the output (no `await` in between). Nested objects containing responses are no longer supported.
- Streaming: the method must be a generator and the caller uses `handle.options(stream=True)`; the call returns a `DeploymentResponseGenerator`, which cannot be passed to other handle calls.
- `serve.get_app_handle("<app name>")` returns a handle to another live application for calls without HTTP.

## Verify
`serve status` lists the three deployments; one request produces logs in each.

## Checked
2026-11-03. Confirmed in Ray repo docs `serve/model-composition.md` and `serve/multi-app.md`. Removed: `asyncio.gather` fan-out example (not in the docs), advice on replica counts per stage, "graph builds at deploy time, no dynamic additions" claim, `serve logs` claim, the unreferenced DeploymentHandle API page source.
Method: documentation only; no commands were run.
