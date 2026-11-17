---
id: computing-software.ai-ml-engineering.mlops.ray-serve-deployments
name: ray-serve-deployments
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, ray-serve, model-serving, autoscaling, model-composition, dynamic-batching]
level: practitioner
status: docs-checked
description: "Serve models with Ray Serve: @serve.deployment replicas and fractional GPUs, autoscaling_config, @serve.batch, DeploymentHandle composition, multiplexing, RayService."
sources:
  - https://raw.githubusercontent.com/ray-project/ray/master/doc/source/serve/key-concepts.md
  - https://raw.githubusercontent.com/ray-project/ray/master/doc/source/serve/autoscaling-guide.md
  - https://raw.githubusercontent.com/ray-project/ray/master/doc/source/serve/advanced-guides/dyn-req-batch.md
  - https://raw.githubusercontent.com/ray-project/ray/master/doc/source/serve/model-composition.md
  - https://raw.githubusercontent.com/ray-project/ray/master/doc/source/serve/model-multiplexing.md
  - https://raw.githubusercontent.com/ray-project/ray/master/doc/source/serve/resource-allocation.md
  - https://raw.githubusercontent.com/ray-project/ray/master/doc/source/serve/production-guide/kubernetes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Ray Serve deployments

**Good fit:** Python-native serving with multi-model pipelines, fractional GPUs and autoscaling, on Ray clusters (often KubeRay).

## Concepts
A deployment holds business logic or a model; at runtime it is a number of replicas, each a copy of the class or function in a separate Ray Actor (process). An application is the unit of upgrade and has one ingress deployment that handles all inbound traffic. By default the ingress `__call__` receives a Starlette request and the response is serialised as JSON; Serve also integrates with FastAPI. Applications are called over HTTP at their `route_prefix` or in Python via a `DeploymentHandle`.

## Resources
`ray_actor_options` assigns hardware per replica; by default each replica reserves one CPU. Values can be fractional so two models share a GPU, for example `@serve.deployment(ray_actor_options={"num_gpus": 0.5})`; the same works for `num_cpus`. Custom resources go in `"resources"`.

## Autoscaling
```python
@serve.deployment(max_ongoing_requests=16,
                  autoscaling_config={"min_replicas": 1, "max_replicas": 8, "target_ongoing_requests": 4})
class Classifier: ...
```
- `target_ongoing_requests`: the average ongoing requests per replica that the autoscaler tries to maintain. Smaller values for longer requests or tighter latency goals.
- `max_ongoing_requests`: the maximum allowed per replica; not part of the autoscaling config, but set it relative to the target when autoscaling.
- `min_replicas`: the docs suggest 0 if there are long idle periods and extra tail latency on upscale is acceptable. `max_replicas`: the docs suggest about 20% above the expected peak need.
- `num_replicas="auto"` applies defaults including `max_replicas` of 100; configuring autoscaling manually without it has a base default `max_replicas` of 1, so autoscaling will not occur unless you set a higher value.

## Dynamic batching
```python
@serve.batch(max_batch_size=32, batch_wait_timeout_s=0.01)
async def predict_batch(self, texts: list[str]) -> list[dict]: ...
```
The decorated method receives a list and returns a list of equal length. `max_batch_size` default is 10; `batch_wait_timeout_s` default is 0.01 (10 ms) and is how long Serve waits for a batch after the first request arrives; on timeout the partial batch is sent. The docs say `max_batch_size` ideally is a power of 2 and that large batches cost memory and add latency for the first requests. Async generator functions can be decorated for streaming batched responses.

## Composition
Deployments passed as constructor arguments are converted to `DeploymentHandle`s at runtime, built with `.bind()`. `handle.method.remote(...)` returns a `DeploymentResponse` (a future): `await` it, or pass it to another handle call. Inside a deployment, avoid `.result()`: it blocks the deployment from running other code, so use `await`. Each stage scales and reserves resources independently.

## Multiplexing
`@serve.multiplexed` plus `serve.get_multiplexed_model_id()` serve many model variants from shared replicas; the client sends the `serve_multiplexed_model_id` request header. `max_num_models_per_replica` caps loaded models per replica; beyond it Serve evicts the least recently used model.

## Kubernetes
Use the KubeRay operator and a `RayService` custom resource, which encapsulates a multi-node Ray cluster and a Serve application in one manifest managed with `kubectl`. Set `serveConfigV2` (the output of `serve build` can be pasted in) and `rayClusterConfig` (the `spec` of a RayCluster). The controller creates the cluster, then deploys the application through the REST API, and creates a Kubernetes Service to route traffic.

## Verify
- [ ] A load test shows replicas scaling up and back down.
- [ ] Observed batch sizes are near `max_batch_size` under load.
- [ ] Cold-start latency is acceptable if `min_replicas` is 0.

## Checked
Date: 2026-11-09.
- Confirmed in the Ray Serve key-concepts, autoscaling, batching, composition, multiplexing, resource-allocation and Kubernetes pages (master branch docs): all items above, including the defaults quoted.
- Removed as unconfirmed: the model-loading code and `serve run` / `serve deploy` commands, the claim that RayService supports zero-downtime upgrades, GCS fault tolerance with Redis advice, the named Ray dashboard metrics, gRPC and streaming-response bullets, and the Ray Serve LLM / vLLM bullet.
Method: documentation only; no commands were run.
