---
id: computing-software.cloud-infrastructure-engineering.talos-linux.kubernetes-upgrade-k8s-automated
name: kubernetes-upgrade-k8s-automated
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [talosctl, upgrade-k8s, kubernetes, dry-run, manifests, prune, server-side-apply]
level: practitioner
status: docs-checked
description: "Upgrade Kubernetes on Talos with talosctl upgrade-k8s: dry-run preview, the six phases, restartability, manifest pruning from v1.13, and avoiding drift from stored configs."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/kubernetes-guides/advanced-guides/upgrading-kubernetes.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`talosctl upgrade-k8s` is the recommended way to upgrade Kubernetes on a Talos-native cluster. Point `--nodes` at one control plane node; all cluster members are upgraded.

```sh
talosctl --nodes <control-plane-ip> upgrade-k8s --to <new-kubernetes-version>
```

Preview first with `--dry-run`, which lists deprecated APIs found and every component update marked "skipped in dry-run".

Phases: (1) images for new components are pre-pulled; (2) each control plane machine config is patched with the new component images and the command waits for propagation; (3) the `kube-proxy` daemonset is updated; (4) the `kubelet` version is updated on every node and verified through the `Node` resource; (5) bootstrap manifests are re-applied; (6) unneeded resources are pruned (Talos v1.13+). If it fails, restart it; it resumes from the failure point. For custom component images use the `--*-image` flags. Talos does not disrupt workloads but kubelet restarts may.

Manifests: from v1.13 all are applied via Server-Side Apply and Talos forces field ownership. Disable pruning with `--manifests-no-prune`. To take over a Talos-applied resource: remove its inline or extra manifest entry from the machine config, confirm with `talosctl upgrade-k8s --dry-run --to <in-cluster-k8s-version>`, remove the entries from the inventory with `kubectl edit cm --namespace kube-system talos-bootstrap-manifests-inventory`, delete the `config.k8s.io/owning-inventory` annotation, then re-apply with your own field manager.

Drift: the upgrade changes live component images, so storing full `controlplane.yaml` or `worker.yaml` in Git and re-applying them later can downgrade components. The page advises against storing full machine configurations.

## Checked

2026-11-04. Command, dry-run, phase list, pruning and Server-Side Apply notes, inventory configmap steps and the drift warning confirmed on the Upgrading Kubernetes guide.

Method: documentation only; no commands were run.
