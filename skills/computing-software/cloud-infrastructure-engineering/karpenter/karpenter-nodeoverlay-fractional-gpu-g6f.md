---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-nodeoverlay-fractional-gpu-g6f
name: karpenter-nodeoverlay-fractional-gpu-g6f
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [nodeoverlay, g6f, fractional-gpu, nvidia, vgpu, gpu-memory, describeinstancetypes]
level: advanced
status: docs-checked
description: "Using a NodeOverlay to schedule on g6f fractional GPU instances: why DescribeInstanceTypes hides the GPU, the overlay and NodePool pair, and GPU memory sizes per size."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodeoverlays.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Fractional GPU instances (g6f) with NodeOverlay

g6f instances present a slice (1/8 to 1/2) of an NVIDIA L4 as one logical vGPU. EC2 `DescribeInstanceTypes` reports `Count=0` for these GPUs, so Karpenter never sees GPU capacity and pods requesting `nvidia.com/gpu` are never scheduled to g6f.

Overlay telling the simulation each g6f has one GPU (requires the `NodeOverlay` feature gate):

```yaml
apiVersion: karpenter.sh/v1alpha1
kind: NodeOverlay
metadata:
  name: g6f-fractional-gpu
spec:
  requirements:
    - {key: karpenter.k8s.aws/instance-family, operator: In, values: ["g6f"]}
  capacity:
    nvidia.com/gpu: "1"
```

Matching NodePool:

```yaml
spec:
  template:
    spec:
      nodeClassRef: {group: karpenter.k8s.aws, kind: EC2NodeClass, name: gpu-nodeclass}
      requirements:
        - {key: karpenter.k8s.aws/instance-family, operator: In, values: ["g6f"]}
        - {key: karpenter.sh/capacity-type, operator: In, values: ["on-demand"]}
  limits:
    nvidia.com/gpu: "4"
```

Sequence: simulation sees `nvidia.com/gpu: 1`; the pod matches; after launch the NVIDIA device plugin detects the vGPU and reports `nvidia.com/gpu: 1` to the kubelet; the pod binds.

GPU memory differs by size: g6f.xlarge about 3 GB, g6f.2xlarge about 6 GB, g6f.4xlarge about 12 GB. Constrain with `karpenter.k8s.aws/instance-gpu-memory` or size requirements.

## Checked

2026-11-08. Confirmed against the NodeOverlays concept page (v1.13), section Example: Fractional GPU Instances (g6f). Claims match the page; nothing material removed.

Method: documentation only; no commands were run.
