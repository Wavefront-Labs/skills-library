---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-scheduling-accelerators-and-pod-eni
name: karpenter-scheduling-accelerators-and-pod-eni
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [gpu, neuron, accelerators, device-plugin, pod-eni, security-groups-for-pods, reserved-enis]
level: advanced
status: docs-checked
description: "Scheduling GPUs, Neuron and Habana accelerators (device plugin DaemonSets, power-of-2 Neuron requests) and vpc.amazonaws.com/pod-eni with RESERVED_ENIS=1."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/scheduling.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Accelerators and Pod ENI scheduling

Accelerator resources Karpenter understands: `nvidia.com/gpu`, `amd.com/gpu`, `aws.amazon.com/neuron`, `aws.amazon.com/neuroncore`, `habana.ai/gaudi`. Request them in the container resources:

```yaml
resources:
  limits:
    nvidia.com/gpu: "1"
```

You must deploy the matching device plugin DaemonSet (NVIDIA, AMD, AWS Neuron, Habana). Without it the node never reports the resource and Karpenter does not see the node as initialized.

Neuron: the Neuron scheduler extension is required for pods that need more than one neuroncore or device but fewer than all on the node. Karpenter cannot see the extension's decisions, so to keep bin packing consistent use like-sized, power of 2 requests (1, 2, 4 and so on); otherwise pods may stay pending permanently.

Pod ENI (Security Groups for Pods): enable Pod ENI in the VPC CNI first, then request `vpc.amazonaws.com/pod-eni: "1"` in container limits. Because one ENI is reserved, set `RESERVED_ENIS=1` so `maxPods` matches real pod density. Not supported on Windows nodes.

GPU labels available: `karpenter.k8s.aws/instance-gpu-name`, `-gpu-manufacturer`, `-gpu-count`, `-gpu-memory`, `instance-accelerator-name`, `-accelerator-count`.

## Checked

2026-11-04. Confirmed against the Scheduling concept page (v1.13) (identifiers, defaults, limits and prose). Removed the unconfirmed tainted-NodePool GPU advice.

Method: documentation only; no commands were run.
