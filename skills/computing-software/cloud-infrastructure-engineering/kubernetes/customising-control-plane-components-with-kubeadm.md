---
id: computing-software.cloud-infrastructure-engineering.kubernetes.customising-control-plane-components-with-kubeadm
name: customising-control-plane-components-with-kubeadm
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubeadm, kubeadm-extraargs, kubeadm-patches, extravolumes, control-plane-manifest-edit, apiserver-manifest-edit, clusterconfiguration, static-pods, kube-apiserver, audit-policy, encryption-at-rest]
level: advanced
status: docs-checked
description: "Three ways to change kube-apiserver/controller-manager/scheduler flags and mounts on kubeadm clusters (extraArgs, patches dir, direct manifest edit) and which survives upgrades."
sources: ["https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/control-plane-flags/", "https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-reconfigure/", "https://kubernetes.io/docs/reference/config-api/kubeadm-config.v1beta4/", "https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/", "https://kubernetes.io/docs/tasks/configure-pod-container/static-pod/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Customising control-plane components with kubeadm

**Goal:** add a flag or a mount (audit policy, EncryptionConfiguration, OIDC, feature gates)
to a control-plane component without having it silently reverted at the next
`kubeadm upgrade apply`.

## Option A — `extraArgs` / `extraVolumes` in ClusterConfiguration (survives upgrades)
```yaml
apiVersion: kubeadm.k8s.io/v1beta4
kind: ClusterConfiguration
apiServer:
  extraArgs:                       # v1beta4 is a list of name/value; v1beta3 was a map
    - name: audit-policy-file
      value: /etc/kubernetes/audit/policy.yaml
    - name: audit-log-path
      value: /var/log/kubernetes/audit.log
    - name: encryption-provider-config
      value: /etc/kubernetes/enc/enc.yaml
  extraVolumes:
    - name: audit
      hostPath: /etc/kubernetes/audit
      mountPath: /etc/kubernetes/audit
      readOnly: true
      pathType: DirectoryOrCreate
    - name: audit-log
      hostPath: /var/log/kubernetes
      mountPath: /var/log/kubernetes
      pathType: DirectoryOrCreate
controllerManager:
  extraArgs:
    - name: bind-address
      value: 0.0.0.0              # so Prometheus can scrape it
scheduler:
  extraArgs:
    - name: bind-address
      value: 0.0.0.0
```
Apply on an existing cluster: edit the ConfigMap, then reflect the change in the manifests on
each control-plane node (kubeadm's reconfiguration guide; back up `/etc/kubernetes/` first):
```bash
kubectl edit cm -n kube-system kubeadm-config                    # change data.ClusterConfiguration
kubectl -n kube-system get cm kubeadm-config -o jsonpath='{.data.ClusterConfiguration}' > cc.yaml
kubeadm init phase control-plane apiserver --config cc.yaml      # rewrites /etc/kubernetes/manifests/kube-apiserver.yaml
```
The `--config` file must match the updated `ClusterConfiguration`. Repeat on **every**
control-plane node, one at a time: the ConfigMap is cluster-wide but the manifests are per node,
and writing a manifest makes the kubelet restart that static pod. The `ClusterConfiguration` is
global, so a flag you add applies to every instance of that component; use patches for
per-node differences.

## Option B — patches directory (per node, structured; you must pass it again on upgrade)
Patches are beta (since v1.22). Put files such as `/etc/kubernetes/patches/kube-apiserver+strategic.yaml`:
```yaml
spec:
  containers:
  - name: kube-apiserver
    resources:
      requests: {cpu: 500m, memory: 1Gi}
```
and reference the directory from `InitConfiguration`, `JoinConfiguration` or `UpgradeConfiguration`:
```yaml
apiVersion: kubeadm.k8s.io/v1beta4
kind: InitConfiguration
patches:
  directory: /etc/kubernetes/patches
---
apiVersion: kubeadm.k8s.io/v1beta4
kind: UpgradeConfiguration
apply:
  patches:
    directory: /etc/kubernetes/patches
node:
  patches:
    directory: /etc/kubernetes/patches
```
When you upgrade with `kubeadm upgrade apply` and `kubeadm upgrade node` you must provide the same
patches again so the customisation is kept (the reconfiguration guide also mentions
`kubeadm upgrade ... --patches <directory>`). File naming: `<target>[suffix][+patchtype].{json,yaml}`
with target in `kube-apiserver`, `kube-controller-manager`, `kube-scheduler`, `etcd`,
`kubeletconfiguration`, `corednsdeployment`; `suffix` orders patches alphanumerically; patchtype is
`strategic` (default), `merge` or `json`. Use patches for what `extraArgs` cannot express
(resources, probes, duplicate flags).

## Option C — edit the static pod manifest directly (fast, NOT upgrade-safe)
```bash
cp /etc/kubernetes/manifests/kube-apiserver.yaml /root/kube-apiserver.yaml.bak   # NOT into the manifests dir
vi /etc/kubernetes/manifests/kube-apiserver.yaml
```
The kubelet rescans `staticPodPath` (default every 20s) and recreates the pod. Use for emergencies
and experiments; kubeadm may overwrite manifest files on `kubeadm upgrade` unless the change is
also in the `ClusterConfiguration` or a patch. Back-port the change into Option A or B once it
works.

## Gotchas
- Backups placed inside `/etc/kubernetes/manifests` are themselves treated as static pods → a
  second, conflicting apiserver trying to bind :6443.
- A typo in a flag makes the apiserver crash-loop and `kubectl` dies with you; debug with
  `crictl ps -a | grep apiserver` and `crictl logs <id>` on the node.
- Duplicate flags (the same key twice) are not supported in `extraArgs`; use a patch for that.
- Mounts: the apiserver runs in a container — any file referenced by a flag must also be in
  `extraVolumes`, or the pod fails with "no such file or directory" at startup.

## Verify
- [ ] `ps -ef | grep kube-apiserver` on each control-plane node shows the new flag.
- [ ] `kubectl -n kube-system get cm kubeadm-config -o yaml` contains the change (Option A).
- [ ] A `kubeadm upgrade plan`/`apply` dry run (`kubeadm upgrade diff v1.3x.y`) shows the flag retained.

## Checked

Checked 2026-10-26 against Kubernetes documentation v1.37 (kubernetes/website and kubernetes/kubernetes master, commit dates 2026-10-24/25). Confirmed: v1beta4 `extraArgs` as name/value lists, `extraVolumes` fields (`name`, `hostPath`, `mountPath`, `readOnly`, `pathType`), that `ClusterConfiguration` is global per component, the reconfiguration steps (edit the `kubeadm-config` ConfigMap, then `kubeadm init phase control-plane <component> --config`), patches (beta since v1.22, file naming, targets, patch types, `patches.directory` in Init/Join/UpgradeConfiguration and the need to supply them again on upgrade), and the warning about backup files inside the static pod directory. Wrong and fixed: `kubeadm upgrade apply --patches` was shown as the only route and a `upload-config` step was invented for persistence. Removed as unconfirmed: the json-patch flag-removal claim, the managed-cluster remark, and the claim that upgrades always revert manual edits.

Method: documentation only; no commands were run.
