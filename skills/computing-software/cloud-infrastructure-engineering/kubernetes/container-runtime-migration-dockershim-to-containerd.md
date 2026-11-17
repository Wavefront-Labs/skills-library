---
id: computing-software.cloud-infrastructure-engineering.kubernetes.container-runtime-migration-dockershim-to-containerd
name: container-runtime-migration-dockershim-to-containerd
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, containerd, dockershim, cri, cri-o, container-runtime, kubelet-flags, runtime-migration, docker-deprecation, crictl, image-cache]
level: advanced
status: docs-checked
description: "Migrate worker nodes off Docker/dockershim to containerd or CRI-O: CRI socket config, re-pulling cached images, kubelet flag changes, and what tooling breaks."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/migrating-from-dockershim/change-runtime-containerd/", "https://kubernetes.io/docs/setup/production-environment/container-runtimes/", "https://github.com/containerd/containerd/blob/main/docs/getting-started.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container runtime migration: dockershim to containerd

**Goal:** move a node's container runtime off Docker without a workload outage, for
clusters still running pre-1.24 Docker+dockershim setups or any node-level runtime
swap. Dockershim was removed from kubelet in 1.24 — this is mandatory migration work
for anything that old, and still-relevant general-purpose skill for any CRI swap
(moving to CRI-O, Firecracker-based runtimes, etc.).

## 1. What dockershim actually was
- Pre-1.24, kubelet talked to Docker Engine through an in-tree shim
  (**dockershim**) translating the CRI (Container Runtime Interface) calls kubelet
  makes into Docker Engine API calls.
- 1.24 removed dockershim from kubelet entirely. Any cluster that hadn't moved kubelet
  to talk to a CRI runtime directly by then simply can't run kubelet 1.24+ — this
  wasn't a deprecation warning, it was a hard removal.

## 2. The migration itself
The Kubernetes task page (written for clusters on 1.23 or earlier) drains the node, stops Docker, installs containerd, points the kubelet at it, verifies, then removes Docker Engine:
```bash
kubectl drain <node> --ignore-daemonsets
systemctl stop kubelet
systemctl disable docker.service --now
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml
# set SystemdCgroup = true in the runc options (see containerd-systemd-cgroup-driver)
sudo systemctl restart containerd
```
Point kubelet at the CRI socket, either by adding the flag to
`/var/lib/kubelet/kubeadm-flags.env`:
```
--container-runtime-endpoint=unix:///run/containerd/containerd.sock
```
or, on kubeadm nodes, by creating `/var/lib/kubelet/instance-config.yaml` with the
`containerRuntimeEndpoint` parameter (kubeadm stores the node's CRI socket there):
```yaml
containerRuntimeEndpoint: unix:///run/containerd/containerd.sock
```
```bash
systemctl start kubelet
kubectl get nodes -o wide     # containerd should appear as the node's runtime
kubectl uncordon <node>
```
Only remove Docker Engine after the node is healthy; the docs warn that Docker's uninstall
instructions can delete containerd, so be careful.

## 3. What breaks or needs re-checking
- **Images**: do not assume Docker's cached images are visible to the CRI; plan for pods to
  re-pull images and pre-pull where a pull storm would hurt.
- **`docker` CLI stops being useful for cluster debugging** — `crictl` is the CRI-level
  replacement:
  ```bash
  crictl ps -a
  crictl logs <container-id>
  crictl images
  ```
  Any runbook, monitoring script, or habit built on `docker ps`/`docker logs` against
  Kubernetes-managed containers needs to move to `crictl` (or `ctr` for lower-level
  containerd operations) — this is the single biggest operational-habit change.
- **cgroup driver mismatch**: as with initial bootstrap
  (`computing-software.cloud-infrastructure-engineering.kubernetes.kubeadm-cluster-bootstrap`),
  containerd's `SystemdCgroup` setting must match kubelet's `cgroupDriver` — a Docker
  setup that was using `cgroupfs` needs this reconciled explicitly during migration,
  not assumed to carry over.
- **Private registry auth**: use kubelet image pull secrets; the CRI `auths` property of containerd is deprecated.
- **Anything shelling into the Docker socket directly** (some older monitoring agents,
  some CI runners using Docker-in-Docker against the node's socket) breaks outright —
  audit for this before migrating, it's an easy thing to miss until a seemingly
  unrelated tool stops working.

## 4. Rollout order
Migrate workers in waves like any node change — drain, swap runtime, uncordon, confirm
workload scheduling and image pulls work, before moving to the next batch. Control
plane nodes (if stacked, running etcd as static pods) go through the same runtime
swap; verify static pods restart cleanly under the new CRI before treating the node as
done.

## Gotchas
- Some workloads assumed Docker-specific behavior (mounting the Docker socket to build
  images inside a pod, Docker-in-Docker CI patterns) and need re-architecting (rootless
  buildkit, kaniko, img) — this is a real migration cost some teams discover late.
- A node left on Docker/dockershim after the rest of the fleet moves to kubelet 1.24+
  simply can't run the new kubelet at all — there's no partial-skew tolerance for this
  one, unlike ordinary version skew.

## Verify
- [ ] `crictl info` on the node shows the CRI runtime healthy and matches the intended
      cgroup driver.
- [ ] A test pod schedules, pulls its image, and runs successfully post-migration on
      each migrated node before moving to the next batch.
- [ ] Any tooling/scripts referencing the Docker CLI or Docker socket against cluster
      nodes have been identified and migrated to `crictl`/CRI equivalents.
- [ ] Private registry credentials are confirmed working under the new runtime, not
      assumed carried over from Docker's credential store.

## Checked

2026-10-26, against Kubernetes website docs (migrating-from-dockershim, container-runtimes) and containerd docs, main branch as of 2026-10-21. Confirmed: dockershim removed in 1.24, the migration steps, `--container-runtime-endpoint` flag, `containerRuntimeEndpoint` in instance-config.yaml, default containerd CRI socket path, the Docker-uninstall caution. Removed the unconfirmed `nodeRegistration.criSocket` claim, image-store and credential-helper specifics.

Method: documentation only; no commands were run.
