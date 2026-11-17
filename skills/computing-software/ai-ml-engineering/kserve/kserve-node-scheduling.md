---
id: computing-software.ai-ml-engineering.kserve.kserve-node-scheduling
name: kserve-node-scheduling
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [nodeselector, tolerations, node-affinity, kubernetespodspec-nodeselector, kubernetespodspec-affinity, kubernetespodspec-tolerations, config-features, nvidiacomgpu, extendedresourcetoleration, gpu-nodes]
level: practitioner
status: docs-checked
description: "Control InferenceService pod placement with nodeSelector, affinity, tolerations and related pod spec fields in the predictor, and verify scheduling on target nodes."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/node-scheduling/isvc-node-scheduling.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Node scheduling

nodeSelector, node affinity and tolerations go directly on a component (`predictor`, `transformer`) and are identical in both modes.

## Setup
- Standard mode: works out of the box (`serving.kserve.io/deploymentMode: Standard`).
- Knative mode: enable three Knative feature flags, either in the `KnativeServing` CR (`spec.config.features`) or by editing `kubectl edit configmap config-features -n knative-serving`:

```yaml
kubernetes.podspec-affinity: "enabled"
kubernetes.podspec-nodeselector: "enabled"
kubernetes.podspec-tolerations: "enabled"
```

## Usage
```yaml
spec:
  predictor:
    nodeSelector:
      k8s.amazonaws.com/accelerator: "nvidia-tesla-t4"
    tolerations:
      - key: "yourTaintKeyHere"
        operator: "Equal"
        value: "yourValue"
        effect: "NoSchedule"
    triton:
      storageUri: "gs://kfserving-examples/models/torchscript"
      runtimeVersion: 21.08-py3
      resources:
        limits: {nvidia.com/gpu: 1}
```

Combine selector/affinity (pull a pod to a node) with tolerations (allow it onto a tainted node) to dedicate node pools.

## GPU nodes
Taint GPU nodes with the conventional `nvidia.com/gpu`. A custom taint stops the nvidia-device-plugin from scheduling, so the node would expose no GPUs. The plugin tolerates `nvidia.com/gpu`, and the ExtendedResourceToleration admission controller adds that toleration automatically to pods that request GPUs, so a GPU predictor can omit it. Pods that request no GPU (for example a transformer pinned to the node) do not get it, which keeps CPU-only work from blocking GPU node scale-down. The ExtendedResourceToleration admission controller was added in Kubernetes 1.19.

## Checked

Checked 2026-11-08 against the KServe website page isvc-node-scheduling.md, read in full: the three Knative feature flags and both ways to set them, the Standard mode annotation, the nodeSelector and tolerations placement under predictor and transformer, the nvidia.com/gpu taint advice and the ExtendedResourceToleration behaviour (Kubernetes 1.19). Nothing removed; the toleration value in the example is a placeholder.

Method: docs-only read of cited pages, 2026-11-08
