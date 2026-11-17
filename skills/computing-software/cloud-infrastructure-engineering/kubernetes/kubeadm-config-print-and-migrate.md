---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubeadm-config-print-and-migrate
name: kubeadm-config-print-and-migrate
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubeadm, kubeadm-config-print, kubeadm-config-migrate, kubeadm-config, v1beta4]
level: practitioner
status: docs-checked
description: "Generate a full kubeadm config with kubeadm config print, migrate old configs to the current API version and validate them before init or upgrade."
sources: ["https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-config/", "https://kubernetes.io/docs/reference/config-api/kubeadm-config.v1beta4/", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-upgrade/", "https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-reconfigure/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubeadm config print and migrate

## Start from the defaults, not a blog post
```bash
kubeadm config print init-defaults > kubeadm.yaml
kubeadm config print init-defaults \
  --component-configs KubeletConfiguration,KubeProxyConfiguration >> kubeadm.yaml
kubeadm config print join-defaults > join.yaml
kubeadm config print reset-defaults     # newer releases also have ResetConfiguration
kubeadm config print upgrade-defaults   # UpgradeConfiguration (v1beta4)
```
The printout matches the binary's own API version, so it is the only reliable template.
Delete fields you do not change; a short config is easier to review and migrate later.

## Migrate between API versions
```bash
kubeadm config migrate --old-config kubeadm-v1beta3.yaml --new-config kubeadm-v1beta4.yaml
kubeadm config validate --config kubeadm-v1beta4.yaml
```
Main v1beta3 to v1beta4 changes (kubeadm 1.31+):
- `extraArgs` became a list of `{name, value}` pairs, so a flag can be repeated.
- timeouts moved into `InitConfiguration.timeouts` / `JoinConfiguration.timeouts`.
- `ResetConfiguration` and `UpgradeConfiguration` are supported API types (pass them with `--config` to `kubeadm reset` and `kubeadm upgrade`).
- dry run can be set in `InitConfiguration` and `JoinConfiguration`.

## Read what the cluster is actually using
```bash
kubectl -n kube-system get cm kubeadm-config -o jsonpath='{.data.ClusterConfiguration}'
kubectl -n kube-system get cm kubelet-config -o yaml
```
`kubeadm upgrade` takes the cluster configuration from the cluster, not from a local file: its `--config`
accepts an `UpgradeConfiguration`, and the docs say ClusterConfiguration, InitConfiguration and component configs
passed there are ignored. `kubeadm upgrade` does not support reconfiguring an existing cluster; follow the
"Reconfiguring a kubeadm cluster" procedure in the Kubernetes docs for that.

## Gotchas
- Old API versions are removed after a deprecation window: kubeadm 1.27 and newer reject v1beta2 and older, and
  kubeadm 1.31 and newer can migrate v1beta3 to v1beta4. Migrate the file in Git as part of every minor upgrade.
- `migrate` reads, defaults, converts, validates and re-serialises the object, so its output is what kubeadm
  would read internally; diff old and new outputs before you commit.
- Component config printed with `--component-configs` uses its own API groups
  (`kubelet.config.k8s.io/v1beta1`); keep each document separated by `---`.

## Verify
- `kubeadm config validate` exits 0.
- `kubeadm init --config kubeadm.yaml --dry-run` renders manifests with your values.

## Checked

Date: 2026-10-26. Documentation release: Kubernetes website docs (kubernetes/website main, 2026-10-26), kubeadm config API v1beta4.

Fixed: `kubeadm upgrade` does not support reconfiguring an existing cluster, and its `--config` takes an `UpgradeConfiguration` (ClusterConfiguration, InitConfiguration and component configs passed there are ignored), so the advice to edit the ConfigMap or pass a ClusterConfiguration to `upgrade apply --config` was removed; use the kubeadm reconfigure procedure. Confirmed: `kubeadm config print init-defaults|join-defaults|reset-defaults|upgrade-defaults`, the `--component-configs` flag, `kubeadm config migrate --old-config/--new-config` (reads old versions and writes only v1beta4), `kubeadm config validate`; v1beta4 changes (structured `extraArgs` that allow duplicates, `Timeouts` structures, `ResetConfiguration` and `UpgradeConfiguration`, dry run settable in InitConfiguration and JoinConfiguration) arrived in 1.31; kubeadm 1.31 and newer migrate v1beta3 to v1beta4; v1beta2 and older are unsupported since 1.27. Removed as unconfirmed: the silent field-dropping claim.

Method: documentation only; no commands were run.
