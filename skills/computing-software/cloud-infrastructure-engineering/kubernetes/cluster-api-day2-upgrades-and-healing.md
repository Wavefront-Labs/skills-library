---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cluster-api-day2-upgrades-and-healing
name: cluster-api-day2-upgrades-and-healing
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cluster-api, capi, machinehealthcheck, rolling-upgrade, kubeadmcontrolplane, machinedeployment, node-draining, version-skew, etcd, self-healing, fleet-upgrades, day2-operations]
level: advanced
status: docs-checked
description: "Roll Kubernetes version upgrades and auto-heal unhealthy nodes across a Cluster API fleet with MachineHealthCheck and rolling MachineDeployments/KCP."
sources: ["https://github.com/kubernetes-sigs/cluster-api/blob/main/docs/book/src/user/guide/lifecycle/upgrades.md", "https://github.com/kubernetes-sigs/cluster-api/blob/main/docs/book/src/user/guide/lifecycle/healthchecking.md", "https://github.com/kubernetes-sigs/cluster-api/blob/main/docs/book/src/reference/api/labels-and-annotations.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CAPI day 2: rolling upgrades and self-healing

**Goal:** change Kubernetes versions and replace unhealthy nodes across Cluster API clusters by editing declarative fields. Builds on `computing-software.cloud-infrastructure-engineering.kubernetes.cluster-api-fundamentals`. Examples use the `v1beta2` API (supported); `v1beta1` is deprecated since v1.11.

## 1. Rolling upgrades
- The control plane is upgraded before workers. Control plane upgrades must go one Kubernetes minor version at a time; workers may skip versions but must stay within the allowed skew from the control plane (n-3).
- Without ClusterClass you must respect the version skew policy yourself; with ClusterClass change `spec.topology.version` on the Cluster.
- Control plane: change `KubeadmControlPlane.spec.version` (and, if needed, the kubeadm config and `spec.machineTemplate.spec.infrastructureRef` to a new infrastructure template) in a single operation; Cluster API then rolls out new Machines.
- Workers: change the `MachineDeployment` version/template; it rolls out like a Deployment through MachineSets.
- KCP does not upgrade CoreDNS on its own: it only reconciles CoreDNS when `kubeadmConfigSpec.clusterConfiguration.dns.imageTag` (and optionally `imageRepository`) is set.
- Check the Cluster API Kubernetes version support matrix; you may need to upgrade Cluster API first.
- Set PodDisruptionBudgets before upgrading; node replacement honours them like any node drain.

## 2. MachineHealthCheck (self-healing)
```yaml
apiVersion: cluster.x-k8s.io/v1beta2
kind: MachineHealthCheck
metadata: {name: worker-mhc}
spec:
  clusterName: team-a-prod
  selector:
    matchLabels: {cluster.x-k8s.io/deployment-name: md-0}
  checks:
    nodeStartupTimeoutSeconds: 600
    unhealthyNodeConditions:
    - {type: Ready, status: Unknown, timeoutSeconds: 300}
    - {type: Ready, status: "False", timeoutSeconds: 300}
  remediation:
    triggerIf:
      unhealthyLessThanOrEqualTo: 40%
```
- Machines get the label `cluster.x-k8s.io/deployment-name` when controlled by a MachineDeployment, and `cluster.x-k8s.io/control-plane` when part of a control plane.
- MHC only supports Machines owned by a MachineDeployment, MachineSet or KubeadmControlPlane. Remediation by default deletes the Machine and the owner creates a replacement.
- `nodeStartupTimeoutSeconds` defaults to 10 minutes (0 disables it); a Machine whose Node never joins in that time is remediated, and a Machine whose Node was removed is remediated immediately.
- Short-circuiting: `remediation.triggerIf.unhealthyLessThanOrEqualTo` (a count or percentage) stops remediation when more Machines than that are unhealthy; its default is 100%, so short-circuiting is off unless set. `unhealthyInRange` (for example `[3-5]`) takes precedence when both are set. In `v1beta1` the equivalent fields were `maxUnhealthy`, `unhealthyConditions` with `timeout`, and `nodeStartupTimeout`.
- Control plane remediation rules: needs at least two control plane Machines unless the cluster is not yet initialized, a previous remediation must have completed, no Machine may be deleting, and etcd quorum must be preserved. KCP also supports `spec.remediation` with `maxRetry`, `retryPeriodSeconds` and `minHealthyPeriodSeconds` (default 3600) to limit repeated remediation.
- Skipping remediation: the Machine has `cluster.x-k8s.io/skip-remediation` or `cluster.x-k8s.io/paused`, the MHC has `cluster.x-k8s.io/paused`, or the Cluster has `.spec.paused: true`.
- Overlapping MHC selectors cause conflicts; with ClusterClass the class author's MHC is used by default (override or disable via `healthCheck` in `Cluster.spec.topology`).

## Gotchas
- A `nodeStartupTimeout` that is too short remediates slow-booting nodes in a loop.
- Pause the MHC or the Cluster (`cluster.x-k8s.io/paused`) before debugging a stuck rollout so remediation does not fight the upgrade.
- If the kubelet on the node hosting the etcd leader is not working, KCP cannot run some checks and remediation does not happen; the book recommends moving etcd leadership manually and deleting the Machine.
- Infrastructure quota can stall a rollout that needs extra capacity temporarily.

## Verify
- [ ] After an upgrade, `kubectl get kubeadmcontrolplane,machinedeployments -o wide` shows the new version fully rolled out.
- [ ] Stopping a worker's kubelet triggers remediation after the configured timeout in a non-production cluster.
- [ ] `unhealthyLessThanOrEqualTo` blocks remediation when more nodes than the threshold fail together.

## Checked

Checked 2026-10-26 against Cluster API book (main branch, latest commit 2026-10-22; latest release v1.14.3). Confirmed: upgrade ordering and skew, MachineHealthCheck v1beta2 fields and defaults, short-circuiting, control plane remediation rules, skip annotations, KCP remediation fields.

Method: documentation only; no commands were run.
