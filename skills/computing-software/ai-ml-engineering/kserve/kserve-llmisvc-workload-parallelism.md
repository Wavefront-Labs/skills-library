---
id: computing-software.ai-ml-engineering.kserve.kserve-llmisvc-workload-parallelism
name: kserve-llmisvc-workload-parallelism
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [workload, specworker, specprefill, spectemplate, parallelism, tensor, datalocal, expert-parallelism, leaderworkerset, labels, annotations, disaggregated]
level: advanced
status: docs-checked
description: "LLMInferenceService workloads: worker or prefill selection, tensor, data, dataLocal and expert parallelism, LeaderWorkerSet size, spec.labels propagation."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/generative-inference/llmisvc/llmisvc-configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LLMInferenceService workloads and parallelism

Selection: `spec.worker` present gives multi-node (LeaderWorkerSet); `spec.prefill` present gives prefill/decode separation; neither gives a plain Deployment.

## Parallelism
```yaml
spec:
  parallelism:
    tensor: 4        # split model across GPUs
    data: 8          # total data-parallel instances
    dataLocal: 4     # GPUs per node
    expert: true     # MoE expert parallelism
    dataRPCPort: 8001
```
Multi-node size = `data / dataLocal` (for example 16 / 8 = 2 LWS replicas); this overrides `replicas` if they differ. `template` is the leader pod spec and `worker` the worker spec; resources such as `nvidia.com/gpu: "4"` and `rdma/roce: "1"` go in container limits.

## Prefill-decode
Top-level `replicas` + `template` are the decode pool; `spec.prefill` has its own `replicas` and `template` (for example vLLM `--enable-chunked-prefill` on prefill and `--enforce-eager` on decode).

## Labels and annotations
`spec.labels` / `spec.annotations` go onto the workload Service `<name>-kserve-workload-svc`, Deployment pod template, and LWS leader/worker templates (not `metadata.labels`). `spec.prefill.labels` apply to prefill pods only. Controller-read routing annotations (`serving.kserve.io/model-based-routing-enabled`, `serving.kserve.io/model-based-routing-only`, `serving.kserve.io/lora-model-routing-strategy`) are not copied. Do not set `app.kubernetes.io/name`, `part-of` or `component` labels in `spec.labels`, because they would override the values KServe sets on the Service.

## Checked
Confirmed against the KServe LLMInferenceService configuration guide: workload selection logic, parallelism fields and the data / dataLocal size formula, prefill-decode layout, and the labels and annotations propagation rules. Dropped the unsupported "(instances)" gloss on dataLocal.

Method: docs-only read of cited pages, 2026-11-08
