---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-automated-upgrades-plans
name: k3s-automated-upgrades-plans
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, system-upgrade-controller, upgrade-plan, k3s-upgrade]
level: advanced
status: docs-checked
description: "Automate K3s upgrades with the system-upgrade-controller and server and agent Plan resources tied to a release channel."
sources:
  - https://docs.k3s.io/upgrades/automated
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: declaratively upgrade nodes. Not for Rancher-managed clusters: if Rancher provisioned or registered the cluster, use Rancher for upgrades.

Install the controller (CRD, deployment, service account, cluster role binding, configmap):

```
kubectl apply -f https://github.com/rancher/system-upgrade-controller/releases/latest/download/crd.yaml -f https://github.com/rancher/system-upgrade-controller/releases/latest/download/system-upgrade-controller.yaml
```

Config changes to its configmap need the controller pod deleted to apply.

Create at least two Plans (apiVersion upgrade.cattle.io/v1, namespace system-upgrade, same namespace as the controller) because servers must upgrade before agents. Server plan: concurrency 1, cordon true, nodeSelector node-role.kubernetes.io/control-plane In "true", serviceAccountName system-upgrade, upgrade.image rancher/k3s-upgrade, channel https://update.k3s.io/v1-release/channels/stable. Agent plan: nodeSelector control-plane DoesNotExist, plus `prepare` with image rancher/k3s-upgrade and args `prepare server-plan` so agent jobs wait for the server plan.

Instead of channel, pin `version: v1.33.4+k3s1`. The upgrade starts once the target resolves; editing a plan re-evaluates it and channels are polled periodically.

Monitor:

```
kubectl -n system-upgrade get plans -o wide
kubectl -n system-upgrade get jobs
```

The Kubernetes version skew policy applies; the controller does not stop you skipping minor versions.

## Checked

2026-11-08: read the whole Automated Upgrades page (raw markdown from the k3s-io/docs repo, which backs docs.k3s.io/upgrades/automated). Confirmed the install command, plan fields, prepare step, version pinning, polling behaviour, monitoring commands and the version skew warning.

Method: documentation only; no commands were run.
