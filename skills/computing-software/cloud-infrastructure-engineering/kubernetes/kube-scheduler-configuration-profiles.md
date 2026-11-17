---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kube-scheduler-configuration-profiles
name: kube-scheduler-configuration-profiles
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kube-scheduler, kubeschedulerconfiguration, scheduler-profiles, scoring-strategy, mostallocated, bin-packing, scheduler-plugins, schedulername]
level: advanced
status: docs-checked
description: "Configure kube-scheduler with KubeSchedulerConfiguration: multiple profiles via schedulerName, plugin weights, and NodeResourcesFit MostAllocated bin-packing."
sources: ["https://kubernetes.io/docs/reference/scheduling/config/", "https://kubernetes.io/docs/concepts/scheduling-eviction/resource-bin-packing/", "https://kubernetes.io/docs/reference/config-api/kube-scheduler-config.v1/", "https://github.com/kubernetes-sigs/scheduler-plugins"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# KubeSchedulerConfiguration profiles and scoring

## Wiring
kube-scheduler `--config=<file>`; on a kubeadm static pod, mount the file into the container with a
hostPath volume. Use `kubescheduler.config.k8s.io/v1` (v1beta3 was removed in v1.29).

```yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
clientConnection: {kubeconfig: /etc/kubernetes/scheduler.conf}
profiles:
- schedulerName: default-scheduler
  pluginConfig:
  - name: PodTopologySpread
    args:
      defaultingType: List
      defaultConstraints:
      - {maxSkew: 1, topologyKey: topology.kubernetes.io/zone, whenUnsatisfiable: ScheduleAnyway}
- schedulerName: bin-packing
  plugins:
    score:
      disabled: [{name: NodeResourcesBalancedAllocation}]
  pluginConfig:
  - name: NodeResourcesFit
    args:
      scoringStrategy:
        type: MostAllocated          # default is LeastAllocated; MostAllocated and RequestedToCapacityRatio pack
        resources: [{name: cpu, weight: 1}, {name: memory, weight: 1}, {name: nvidia.com/gpu, weight: 5}]
```
Pods opt in: `spec.schedulerName: bin-packing`. One kube-scheduler instance runs all its profiles
(the docs: "a single instance of kube-scheduler to run multiple profiles")
instead of a second scheduler binary.

## Common uses
- **Bin-packing** for batch/GPU pools so autoscalers can remove empty nodes.
- Cluster-wide **default topology spread** (above) so teams get zone spreading for free.
- `percentageOfNodesToScore` (top-level field) stops the search for feasible nodes early to speed scheduling on large clusters.
- Disabling a plugin for a profile (e.g. `ImageLocality` scoring) or changing weights:
  `score.enabled: [{name: NodeAffinity, weight: 5}]`.

## Extension points
`queueSort, preFilter, filter, postFilter, preScore, score, reserve, permit, preBind, bind,
postBind`, plus the config-only `multiPoint` (newer releases add further points, so read the
reference for your version). Out-of-tree plugins (kubernetes-sigs/scheduler-plugins lists
Capacity Scheduling, Coscheduling, Node Resource Topology and others) need a custom-built
scheduler binary, run as an additional scheduler with its own `schedulerName`.

## Managed clusters
Managed control planes may not let you pass `--config` to the default scheduler (check your provider's
documentation); a secondary scheduler deployed as a workload is the usual alternative.

## Verify
```bash
kubectl get pods -o wide        # compare placement of pods using each schedulerName
kubectl get events --field-selector reason=Scheduled
```
- [ ] Pods with `schedulerName: bin-packing` concentrate on fewer nodes than default ones.

## Checked
2026-10-23, against the Kubernetes website scheduler-configuration reference and resource bin packing page (profiles, extension points, MostAllocated and RequestedToCapacityRatio strategies, v1beta3 removal in v1.29), the kube-scheduler config v1 types and defaults source (top-level percentageOfNodesToScore, LeastAllocated default), and the scheduler-plugins README. The Policy API removal and the managed-provider claims were removed as unconfirmed.
Method: documentation only; no commands were run.
