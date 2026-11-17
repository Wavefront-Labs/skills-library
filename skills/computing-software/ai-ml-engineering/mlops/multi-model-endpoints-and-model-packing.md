---
id: computing-software.ai-ml-engineering.mlops.multi-model-endpoints-and-model-packing
name: multi-model-endpoints-and-model-packing
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, model-deployment, multi-model-endpoints, inference-components, model-packing, triton, sagemaker, vertex-ai]
level: practitioner
status: draft
description: "Host many models on shared inference capacity: SageMaker multi-model endpoints and inference components, Vertex co-hosting, Triton multi-model GPUs, and their latency costs."
sources:
  - https://docs.aws.amazon.com/sagemaker/latest/dg/multi-model-endpoints.html
  - https://docs.aws.amazon.com/sagemaker/latest/dg/realtime-endpoints-deploy-models.html
  - https://cloud.google.com/vertex-ai/docs/predictions/model-co-hosting
  - https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_management.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multi-model endpoints and model packing

**Goal:** serve hundreds of per-customer or per-region models, or several small models, without one idle instance each.

## SageMaker multi-model endpoints (MME)
- All models share one container and live under an S3 prefix; the endpoint loads a model on first request and evicts least-recently-used models when memory fills.
```python
from sagemaker.multidatamodel import MultiDataModel
mme = MultiDataModel(name="per-tenant", model_data_prefix="s3://bucket/models/", model=base_model)
pred = mme.deploy(initial_instance_count=2, instance_type="ml.m5.2xlarge")
pred.predict(payload, target_model="tenant-042.tar.gz")
```
- Add a model by copying its `tar.gz` to the prefix; no redeploy.
- First request per model (or after eviction) pays download + load latency. Watch `ModelCacheHit`, `ModelLoadingWaitTime` and `ModelUnloadingTime` in CloudWatch.
- Models must share a framework/container. GPU MMEs use Triton. Best for many small, similarly sized models with long-tail traffic.

## SageMaker inference components
For a few larger models (e.g. several LLMs) on one endpoint, create **inference components** each with its own `ComputeResourceRequirements` (accelerators, memory, CPU) and `CopyCount`. Each component scales independently and can scale to zero copies. This is "packing" rather than MME-style caching.

## Vertex AI
- Deploy several models to one endpoint with traffic splits (for A/B), each with dedicated resources.
- **Co-hosting**: a `DeploymentResourcePool` lets multiple models share the same VMs; models scale together on the pool.

## Triton on one GPU
Triton's model repository can hold many models; `--model-control-mode=explicit` with load/unload APIs (`POST v2/repository/models/<m>/load`) lets you manage which are resident. `instance_group` per model sets how many copies run on which GPUs. Several small models on one GPU raises utilisation; watch GPU memory and tail latency under concurrency.

## Gotchas
- Noisy neighbours: one hot model can starve others; set per-model concurrency limits or separate hot models onto dedicated capacity.
- Cache thrash: if the working set of models exceeds instance memory, every request becomes a cold load. Size instance memory to the hot set, or shard tenants across endpoints.
- Monitoring and drift checks must be per model; aggregate endpoint metrics hide a single failing model.

## Verify
- [ ] Cache-hit rate and p99 latency measured under realistic tenant traffic.
- [ ] Hot models identified and given dedicated capacity if needed.
- [ ] Adding/removing a model tested without endpoint downtime.
