---
id: computing-software.cloud-infrastructure-engineering.kubernetes.static-pod-control-plane-management
name: static-pod-control-plane-management
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, static-pods, control-plane, manifests, kubelet, kube-apiserver, mirror-pod, manifest-path, kubeadm, break-glass, recovery]
level: advanced
status: docs-checked
description: "Operate kube-apiserver/scheduler/controller-manager/etcd as kubelet-managed static pods: how manifest edits apply, mirror pods, and recovery with no working API server."
sources: ["https://kubernetes.io/docs/tasks/configure-pod-container/static-pod/", "https://kubernetes.io/docs/concepts/workloads/pods/static-pods/", "https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/", "https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-reconfigure/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static pod control-plane management

**Goal:** understand and safely edit the one part of a kubeadm cluster that is not an
API object — because when the API server itself is broken, static pods and
`/etc/kubernetes/manifests/` are the only lever left to fix it. Certificate renewal
through this mechanism is covered operationally in
`computing-software.cloud-infrastructure-engineering.kubernetes.certificate-rotation-and-expiry-management`.

## 1. What a static pod actually is
- A pod defined by a YAML file on a **node's local filesystem**
  (`/etc/kubernetes/manifests/*.yaml` by default, configured via kubelet's
  `staticPodPath`), managed directly by **kubelet**, with no Deployment/ReplicaSet/API
  object controlling it. kubeadm uses this for `kube-apiserver`, `kube-controller-manager`,
  `kube-scheduler`, and (stacked topology) `etcd` — these need to exist *before* the API
  server they'd otherwise be scheduled by is up, so they can't be ordinary pods.
- kubelet creates a read-only **mirror pod** in the API server (once it's reachable) so
  `kubectl get pods -n kube-system` shows them — but `kubectl delete` on a mirror pod
  just causes kubelet to recreate the mirror; it does not stop the real process. To
  actually stop/restart one, edit or move the manifest file on the node.

## 2. How edits take effect
- The kubelet rescans `staticPodPath` periodically (`fileCheckFrequency`, default 20s) and
  creates, restarts or removes static pods as files change; the docs only require a kubelet
  restart when you first configure `staticPodPath`.
- To force a one-off restart without an edit: `mv` the manifest out of the directory,
  wait for kubelet to notice and terminate the pod, then move it back.
- A syntactically broken manifest fails silently from `kubectl`'s point of view —
  there's no API object to report the error. Check `journalctl -u kubelet` or the
  container runtime's logs (`crictl ps -a`, `crictl logs <id>`) directly on the node.

## 3. Debugging when the API server itself won't start
This is the scenario this skill exists for — `kubectl` is unusable because the thing
`kubectl` talks to is down:
```bash
crictl ps -a | grep apiserver          # is the container even running, or crash-looping?
crictl logs <container-id>             # actual startup error — bad flag, bad cert path, etc.
```
- Common causes: a bad edit to the manifest (typo'd flag, wrong cert path after a
  renewal), a cert that's actually expired (see cert-rotation skill), or a resource
  constraint on the node (OOM-killed, check `dmesg`/`journalctl -k`).
- Fix by editing the manifest directly on disk and letting kubelet reconcile — this is
  the only path available; there is no `kubectl apply` fallback when the API server is
  the thing that's broken.
- If etcd is also down (stacked topology, same failure), diagnose etcd's own container
  first — the API server crash-looping is often a downstream symptom of etcd being
  unreachable, not the root cause.

## 4. Safe editing practice
- Copy the manifest out, edit the copy, diff against the original, then move the edited
  version back in. Keep every backup outside the manifests directory: the kubelet reads all
  files that do not start with a dot, so a `.bak` copy can replace the real spec.
- Keep manifests under version control (even just a git repo of
  `/etc/kubernetes/manifests` synced out via a config-management tool) so a bad edit has
  a known-good version to revert to without reconstructing it from memory.
- kubeadm writes these manifests from the `ClusterConfiguration` stored in the `kubeadm-config`
  ConfigMap (`kubectl -n kube-system get cm kubeadm-config`); manual edits not reflected there
  or in kubeadm patches can be overwritten by a later kubeadm operation, so update the
  `ClusterConfiguration` (or patches) for anything that must persist.

## Gotchas
- Deleting a static pod's mirror via `kubectl delete pod` looks like it worked (the
  mirror disappears briefly) but kubelet recreates it from the still-present manifest —
  this confuses people expecting normal pod-delete semantics.
- A manifest moved out of `staticPodPath` and never moved back is an easy way to
  accidentally leave a control-plane component permanently stopped after a
  troubleshooting session — always confirm the directory's final state matches intent.
- Resource `requests`/`limits` on static pods are enforced like those of any pod; if an
  undersized control-plane pod is OOM-killed, look in node-level logs (`journalctl -k`,
  `crictl`).

## Verify
- [ ] `crictl ps` (not just `kubectl get pods`) is the first troubleshooting step when a
      control-plane component mirror pod looks unhealthy or missing.
- [ ] Manifest edits are made on a copy, diffed, then swapped in — not edited in place
      live.
- [ ] `/etc/kubernetes/manifests` contents are backed up or under version control
      per control-plane node.
- [ ] A test "move the API server manifest out and back" drill has been run on a
      non-prod node so the recovery mechanics are known before an incident forces it.

## Checked

Checked 2026-10-26 against Kubernetes documentation v1.37 (kubernetes/website commit 2026-10-25) and kubernetes/kubernetes master (kubelet source, 2026-10-24). Confirmed: kubeadm runs kube-apiserver, kube-controller-manager, kube-scheduler and local etcd as static pods; mirror pods and the `kubernetes.io/config.mirror` annotation; deleting a mirror pod does not stop the pod; the 20s `fileCheckFrequency`; moving a manifest out and back as the restart technique (kubeadm certs documentation); the `kubeadm-config` ConfigMap as the source for regenerated manifests; the warning about backups inside the manifests directory. Removed as unconfirmed: the claim that a kubelet restart forces immediate pickup, the half-written-file failure mode, and the "silently overwritten" wording.

Method: documentation only; no commands were run.
