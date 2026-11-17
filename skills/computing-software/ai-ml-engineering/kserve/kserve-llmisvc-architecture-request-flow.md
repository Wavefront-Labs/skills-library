---
id: computing-software.ai-ml-engineering.kserve.kserve-llmisvc-architecture-request-flow
name: kserve-llmisvc-architecture-request-flow
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [gateway, epp, zmq, nixlconnector, kv-events-config, kv-transfer-config, kserve-infer-roce, vllm-additional-args, prefill-decode-flow, managed-gateway]
level: advanced
status: docs-checked
description: "LLMInferenceService control plane: managed vs referenced Gateway/HTTPRoute, EPP scoring weights, KV event ZMQ, NixlConnector via VLLM_ADDITIONAL_ARGS, request flows, P/D sizing."
sources: ["https://github.com/kserve/website/blob/main/docs/concepts/architecture/control-plane-llmisvc.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LLMInferenceService architecture and request flow

Managed Gateway (`router.gateway: {}`) creates `<name>-kserve-gateway` (default `gatewayClassName: eg`, Envoy Gateway, HTTP port 80). Referenced: `gateway.refs: [{name, namespace}]`. Managed route (`route: {}`) creates `<name>-kserve-route` whose backendRef is the InferencePool `<name>-inference-pool` (group `inference.networking.x-k8s.io`).

## Scheduler (EPP)
Scores endpoints with pluggable scorers: prefix cache scorer (weight 2.0), load-aware scorer (1.0), queue scorer (configurable). vLLM publishes `BlockStored` and `BlockRemoved` events over ZMQ; the EPP indexes `{ModelName, BlockHash}` to `{PodID, DeviceTier}`. Without a scheduler routing is a plain Kubernetes Service (round-robin, no cache awareness, no automatic pool selection); fine for dev.

```yaml
env:
  - name: VLLM_ADDITIONAL_ARGS   # KV events to scheduler
    value: "--kv-events-config '{\"enable_kv_cache_events\":true,\"publisher\":\"zmq\",\"endpoint\":\"tcp://scheduler:5557\",\"topic\":\"kv@${POD_IP}@model\"}'"
```
Prefill-decode KV transfer (RDMA over RoCE): set `KSERVE_INFER_ROCE=true` and `VLLM_ADDITIONAL_ARGS=--kv_transfer_config '{"kv_connector":"NixlConnector","kv_role":"kv_both"}'`.

## Prefill-decode flow
A new request is scored to a Decode pod; its routing container forwards the prompt to a Prefill pod, KV is transferred to the Decode pod via RDMA if needed, the response carries KV metadata, and the continuation request is routed straight to the Decode pod on KV match.

## Multi-node P/D sizing
Prefill `parallelism: {tensor: 4, data: 16, dataLocal: 8}` gives 2 LWS replicas of 8 GPUs; decode `{tensor: 4, data: 8, dataLocal: 4}` gives 2 replicas of 4 GPUs; total 24 GPUs (the page's own figures; its example sets `nvidia.com/gpu` limits of "8" per prefill container and "4" per decode container).

## Checked
Confirmed against the KServe LLMInferenceService Architecture Deep Dive page: managed and referenced Gateway and HTTPRoute, generated names and default gatewayClassName, scorer weights, the ZMQ BlockStored and BlockRemoved index, scheduler versus no-scheduler table, both VLLM_ADDITIONAL_ARGS snippets, KSERVE_INFER_ROCE, the prefill-decode flow and the multi-node sizing example.

Method: docs-only read of cited pages, 2026-11-08
