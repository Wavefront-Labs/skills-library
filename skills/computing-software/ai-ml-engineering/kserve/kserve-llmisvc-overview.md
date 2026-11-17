---
id: computing-software.ai-ml-engineering.kserve.kserve-llmisvc-overview
name: kserve-llmisvc-overview
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [llmisvc, llminferenceservice, llm-d, vllm, genai, prefill-decode, multi-node, parallelism, gateway-api, dual-track]
level: intro
status: docs-checked
description: "What LLMInferenceService is: GenAI-first CRD on llm-d, why separate from InferenceService, deployment patterns, the four spec areas (model, workload, router, parallelism)."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/generative-inference/llmisvc/llmisvc-overview.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Understanding LLMInferenceService

`LLMInferenceService` (`serving.kserve.io/v1alpha1`) is a CRD for generative AI serving, built on the llm-d framework (vLLM engine, KV-cache aware scheduling, disaggregated prefill-decode, distributed inference). KServe runs a dual track: `InferenceService` for predictive ML, `LLMInferenceService` for LLMs. InferenceService can still serve LLMs but only basic single-node setups; prefill-decode separation, multi-node orchestration and intelligent scheduling are LLMInferenceService-only. Use it for 7B to 405B models, multi-GPU and high throughput; not for traditional ML.

Patterns: single-node (small models, under 7B parameters), multi-node with LeaderWorkerSet (medium-large models), prefill-decode separation (disaggregated serving for cost optimization), data plus expert parallelism for MoE models (Mixtral, DeepSeek-R1). The page's scenario table marks models under 70B as optional (either CRD works).

Spec areas:
- `spec.model`: `uri` (HuggingFace, S3 or PVC source; the example uses `hf://`), `name` (used in API requests), scheduling `criticality`, optional LoRA adapters.
- Workload: `spec.template` (single-node or decode), `spec.worker` (multi-node, triggers LeaderWorkerSet), `spec.prefill` (prefill-only pool).
- `spec.router`: `gateway`, `route` (HTTPRoute), `scheduler` (endpoint picker, EPP).
- `spec.parallelism`: tensor, data, expert.

```yaml
apiVersion: serving.kserve.io/v1alpha1
kind: LLMInferenceService
metadata: {name: llama-3-8b, namespace: default}
spec:
  model:
    uri: hf://meta-llama/Llama-3.1-8B-Instruct
    name: meta-llama/Llama-3.1-8B-Instruct
  replicas: 3
  template:
    containers:
      - name: main
        image: vllm/vllm-openai:latest
        resources:
          limits: {nvidia.com/gpu: "1", cpu: "8", memory: 32Gi}
  router: {gateway: {}, route: {}, scheduler: {}}
```

This creates 3 single-GPU pods, Gateway API ingress, the scheduler, and a storage initializer for model download.

## Checked
Confirmed against the KServe Understanding LLMInferenceService page: llm-d basis, dual-track strategy, the InferenceService limitation, deployment patterns, scenario table, the four spec areas, the quick example and its listed results. Removed the specific `s3://` and `pvc://` scheme prefixes, which the page does not give (it names HuggingFace, S3 and PVC only).

Method: docs-only read of cited pages, 2026-11-08
