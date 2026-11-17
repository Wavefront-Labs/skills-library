---
id: computing-software.cloud-infrastructure-engineering.kubernetes.arm64-graviton-node-pools
name: arm64-graviton-node-pools
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cost-optimisation, graviton, arm64-nodes, multi-arch-images, karpenter]
level: practitioner
status: draft
description: "Introduce ARM64 (AWS Graviton, Azure Cobalt, Google Axion) node pools for cost savings with multi-arch images, opt-in scheduling and safe workload migration."
sources: ["https://aws.amazon.com/ec2/graviton/", "https://kubernetes.io/docs/reference/labels-annotations-taints/#kubernetes-io-arch", "https://karpenter.sh/docs/concepts/nodepools/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ARM64 and Graviton node pools

ARM instances usually give better price-performance (AWS states up to around 40 % for Graviton),
but every image a pod uses must have an arm64 variant.

## 1. Check images
```bash
kubectl get pods -A -o jsonpath='{range .items[*]}{range .spec.containers[*]}{.image}{"\n"}{end}{end}' | sort -u > images.txt
while read i; do echo "$i $(crane manifest "$i" 2>/dev/null | jq -r '[.manifests[]?.platform.architecture] | join(",")')"; done < images.txt
```
Images without `arm64` in the list need multi-arch builds (`docker buildx build --platform
linux/amd64,linux/arm64`, ko, or vendor arm64 tags). DaemonSets (CNI, CSI, logging, security
agents) must all be multi-arch before adding arm nodes.

## 2. Opt-in pool
```yaml
# Karpenter NodePool excerpt
spec:
  template:
    spec:
      requirements:
      - {key: kubernetes.io/arch, operator: In, values: [arm64]}
      - {key: karpenter.k8s.aws/instance-family, operator: In, values: [m7g, c7g, r7g]}
      taints: [{key: arch, value: arm64, effect: NoSchedule}]
```
Workloads opt in with a toleration (plus a nodeSelector or affinity if needed). Once most images are
multi-arch, remove the taint and allow both arches so the autoscaler picks the cheapest.

## 3. Migrate workloads
Move stateless services first; compare latency, CPU and error rate. JVMs, Go and Node.js usually
just work; native extensions, old Python wheels and AVX-specific code need checks.

## Gotchas
- `exec format error` means an amd64-only image landed on arm.
- Mixed-arch HPAs: CPU utilization differs per arch; compare per-arch metrics.

## Verify
`kubectl get nodes -L kubernetes.io/arch` shows arm64 nodes, and migrated workloads run there with
steady error rates and lower cost per request.
