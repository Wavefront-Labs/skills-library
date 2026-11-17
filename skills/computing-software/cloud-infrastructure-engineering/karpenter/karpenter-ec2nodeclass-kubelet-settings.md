---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-ec2nodeclass-kubelet-settings
name: karpenter-ec2nodeclass-kubelet-settings
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [kubelet, maxpods, podspercore, systemreserved, kubereserved, eviction, imagegc, clusterdns, eni-limited-pod-density]
level: advanced
status: docs-checked
description: "EC2NodeClass spec.kubelet: maxPods, podsPerCore, reserved resources, eviction thresholds and grace periods, image GC, clusterDNS, RESERVED_ENIS and when to use userData instead."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodeclasses.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# EC2NodeClass kubelet settings

`spec.kubelet` is optional and is a subset of upstream KubeletConfiguration; change it only when needed.

```yaml
kubelet:
  maxPods: 20
  podsPerCore: 2
  systemReserved: {cpu: 100m, memory: 100Mi, ephemeral-storage: 1Gi}
  kubeReserved: {cpu: 200m, memory: 100Mi, ephemeral-storage: 3Gi}
  evictionHard: {memory.available: 5%, nodefs.available: 10%, nodefs.inodesFree: 10%}
  evictionSoft: {memory.available: 500Mi}
  evictionSoftGracePeriod: {memory.available: 1m}
  evictionMaxPodGracePeriod: 60
  imageGCHighThresholdPercent: 85
  imageGCLowThresholdPercent: 80
  cpuCFSQuota: true
  clusterDNS: ["10.0.1.100"]
```

- `podsPerCore` is multiplied by vCPUs (and passed as `--pods-per-core`); with `maxPods` also set, the minimum of the two is used for scheduling. Default density is limited by the ENIs an instance type can attach and IPs per ENI.
- The page contains a note that `maxPods` may not be set in an EC2NodeClass kubelet, yet its own example sets it; test on your Karpenter version.
- If `systemReserved` or `kubeReserved` are omitted, Karpenter computes defaults (based on its supported AMI families) used for the ephemeral-storage calculation; be aware of this with Custom AMI families.
- Eviction signals: `memory.available`, `nodefs.available`, `nodefs.inodesFree`, `imagefs.available`, `imagefs.inodesFree`, `pid.available`; values are percentages or quantities. A soft threshold must be exceeded for the full grace period before eviction starts; `evictionMaxPodGracePeriod` caps pod grace during soft eviction. The page does not state its units (example is 60).
- Fields not exposed go in `spec.userData`; with the Custom AMI family set them in both `spec.kubelet` and `spec.userData`.
- Small instances: enable prefix assignment mode in the AWS VPC CNI (added in v1.9) for higher density. With Custom Networking set the global `RESERVED_ENIS` to `"1"`. Windows nodes support only one ENI and no custom networking.

## Checked
Method: 2026-11-08 read the Karpenter v1.13 nodeclasses.md page; removed the claim that kubelet options "moved from NodePool" and the claim that overriding reserved values changes allocatable (not stated); added the page's maxPods inconsistency and eviction detail.
