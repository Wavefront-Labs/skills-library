---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gke-node-pool-configuration-labels-taints-images-kubelet-local-ssd
name: gke-node-pool-configuration-labels-taints-images-kubelet-local-ssd
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gke, node-pools, node-labels-taints, node-pool-taints, node-system-config, kubelet-config, sysctl-config, node-image, containerd-cos, local-ssd-node-pool, ephemeral-storage]
level: advanced
status: docs-checked
description: "Configure GKE Standard node pools: labels and taints for dedicated pools, COS vs Ubuntu containerd images, kubelet and sysctl system config, and local SSD for ephemeral or block storage."
sources: ["https://docs.cloud.google.com/kubernetes-engine/docs/how-to/node-system-config", "https://docs.cloud.google.com/kubernetes-engine/docs/how-to/node-taints", "https://docs.cloud.google.com/kubernetes-engine/docs/concepts/node-images"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GKE node pool configuration

## 1. Labels and taints (dedicated pools)
```bash
gcloud container node-pools create batch --cluster=<C> --region=<R> --machine-type=c3-standard-22 \
  --node-labels=workload=batch --node-taints=workload=batch:NoSchedule
```
A new node pool does not inherit taints from the cluster; set `--node-taints` when you create it.
Taint effects are `PreferNoSchedule`, `NoSchedule` and `NoExecute`. Remove all taints from a pool with
`gcloud beta container node-pools update <POOL> --node-taints="" --cluster=<C>`.
Pods need both a `nodeSelector`/affinity on the label and a toleration. For how `update`
treats existing labels and taints, and for persistence across upgrades, check the node pool
reference before relying on it.

## 2. Node image
| image type | Notes |
|---|---|
| `cos_containerd` | Container-Optimized OS with containerd; the only choice on Autopilot |
| `ubuntu_containerd` | Ubuntu with containerd, for Standard when you need it |
| `windows_ltsc_containerd` | Windows Server node pools (Windows Server 2022 and 2019 images) |
Changes to a node VM's boot disk do not persist across node re-creation, and nodes are re-created during
upgrades, auto-repair and autoscaling.

## 3. Kubelet and sysctls
```yaml
# system.yaml
kubeletConfig:
  cpuManagerPolicy: static          # none or static
  podPidsLimit: 4096                # 1024 to 4194304
  cpuCFSQuota: true
linuxConfig:
  sysctl:
    net.core.somaxconn: "2048"
```
```bash
gcloud container node-pools create lowlat --cluster=<C> --region=<R> --system-config-from-file=system.yaml
```
`--system-config-from-file` works with `clusters create`, `node-pools create` and `node-pools update`
(not the console). Applying a configuration file re-creates the nodes, which can disrupt running workloads,
regardless of maintenance policies. `kubeletConfig.allowedUnsafeSysctls` allows `kernel.shm*`, `kernel.msg*`,
`kernel.sem`, `fs.mqueue.*` and `net.*` for Pods. Read current settings from `linuxNodeConfig` in
`node-pools describe`, but write them under `linuxConfig`. Check the page for the allowed
`sysctl` and hugepage fields before using others.

## Gotchas
- A taint without matching tolerations on DaemonSets you need (log agents, CSI) leaves those nodes unmonitored.
- `cpuManagerPolicy: static` pins CPUs only for Guaranteed QoS Pods with whole-number CPU requests (Kubernetes behaviour).

## Verify
- [ ] `kubectl get nodes -L workload` and `kubectl describe node` show the expected label and taint.
- [ ] After applying the system config, the node pool shows the new settings in `node-pools describe`.

## Checked

2026-10-24, GKE node system configuration, node taints and node images pages on docs.cloud.google.com. Confirmed: `--node-taints` effects and clearing syntax, no taint inheritance for new pools, image type names (`cos_containerd`, `ubuntu_containerd`, `windows_ltsc_containerd`), Autopilot always uses COS with containerd, `--system-config-from-file` scope, `cpuManagerPolicy` values, `podPidsLimit` range, `cpuCFSQuota` spelling, `allowedUnsafeSysctls` groups, node re-creation on config change, `linuxConfig` versus `linuxNodeConfig`. Removed unconfirmed claims: `--node-labels` update semantics, persistence of kubectl-set labels, Docker runtime removal version, Local SSD flags and counts, `net.ipv4.tcp_keepalive_time`, the hugepage field. Corrected: field name is `cpuCFSQuota`.

Method: documentation only; no commands were run.
