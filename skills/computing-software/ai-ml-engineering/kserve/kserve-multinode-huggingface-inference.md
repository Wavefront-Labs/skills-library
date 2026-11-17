---
id: computing-software.ai-ml-engineering.kserve.kserve-multinode-huggingface-inference
name: kserve-multinode-huggingface-inference
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [workerspec, tensorparallelsize, pipelineparallelsize, kserve-huggingfaceserver-multinode, ray, autoscalerclass, gpu-resource-types, recreate, multi-node, multi-gpu]
level: advanced
status: docs-checked
description: "Multi-node multi-GPU vLLM on InferenceService via workerSpec with kserve-huggingfaceserver-multinode: restrictions, PVC RWX, parallel sizes, GPU types, Recreate strategy, probes."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/generative-inference/multi-node/multi-node.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multi-node / multi-GPU with the Hugging Face vLLM runtime

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: huggingface-llama3
  annotations:
    serving.kserve.io/deploymentMode: Standard
    serving.kserve.io/autoscalerClass: none
spec:
  predictor:
    deploymentStrategy: {type: Recreate}   # optional, avoids needing double the GPUs
    model:
      modelFormat: {name: huggingface}
      runtime: kserve-huggingfaceserver-multinode
      storageUri: pvc://llama-3-8b-pvc/hf/8b_instruction_tuned
    workerSpec:
      pipelineParallelSize: 2
      tensorParallelSize: 1
```
`workerSpec: {}` in the InferenceService is what enables multi-node, even though the runtime already carries `workerSpec`.

## Restrictions
- Standard mode only; autoscaler must be `none`; storage must be `pvc://` on an RWX PVC; exactly one head pod.
- Do not set `TENSOR_PARALLEL_SIZE` or `PIPELINE_PARALLEL_SIZE` env vars; use `workerSpec.tensorParallelSize` / `pipelineParallelSize` (runtime defaults 1 and 1, overridable).
- Allowed GPU types: `nvidia.com/gpu` (default), `intel.com/gpu`, `amd.com/gpu`, `habana.ai/gaudi`; others via annotation `serving.kserve.io/gpu-resource-types: '["nvidia.com/mig-1g.5gb"]'`. Do not mix GPU types; a type differing from the runtime gets both assigned. vLLM distributed supports nccl only.

## Sizing
Total GPUs = tensorParallelSize x pipelineParallelSize; Ray nodes = ceil(total / `workerSpec.resources.requests.gpu`); worker GPUs = total / nodes - 1; head GPUs = total - 1. Parameters shard weights and layers; they do not map 1:1 to GPUs or nodes. Changing pipelineParallelSize can disrupt the running service (it sets how many nodes run the model; it is not an autoscaling concept) and the page advises against changing it in production. Without the Recreate strategy, delete the InferenceService and create a new one; the same advice applies to tensorParallelSize. The runtime does not work with Triton. Multi-node needs at least two nodes, and the setup is built on vLLM.

Large models need long probes (consider raising initialDelaySeconds for the liveness, readiness and startup probes); the default startupProbe in the ServingRuntime is failureThreshold 40, periodSeconds 30, successThreshold 1, timeoutSeconds 30, initialDelaySeconds 60. Multi-node setups typically use RollingUpdate, which needs more than twice the resources, so Recreate suits development.

## Checked
Confirmed against the KServe multi-node/multi-GPU inference page: restrictions and key validations, GPU types and annotation, one head pod, sizing formulas, default startup probe, Recreate strategy and workerSpec behaviour. Corrected the RollingUpdate and recreate advice.

Method: docs-only read of cited pages, 2026-11-08
