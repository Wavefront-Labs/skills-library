---
id: computing-software.cloud-infrastructure-engineering.rancher.helm-upgrade-rancher-procedure
name: helm-upgrade-rancher-procedure
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [upgrade, helm, helm-upgrade, upgrade-path, backup, feature-charts]
level: practitioner
status: docs-checked
description: "Upgrade a Helm-installed Rancher: latest-patch-then-next-minor path, backup first, repo update, review feature charts, helm get values, and helm upgrade with preserved settings."
sources:
  - https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/install-upgrade-on-a-kubernetes-cluster/upgrades
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The documented procedure covers Helm installs on Kubernetes, including air gapped ones. Run Helm from where your kubeconfig lives (RKE2: `/etc/rancher/rke2/rke2.yaml`, K3s: `/etc/rancher/k3s/k3s.yaml`) or target it with `--kubeconfig`. Read the release notes for known issues first. Upgrades to, from or between alpha charts are not supported.

**Upgrade path:** the only tested and supported minor-to-minor path is from the latest patch of your current minor release to the latest patch of the next minor. If you are behind on patches, upgrade to the latest patch first. List available versions with:

```
helm repo update
helm search repo rancher-<CHART_REPO>/rancher --versions
```

The outline:

1. Back up the Rancher cluster with the Rancher Backups application; it is your restore point.
2. Update the Helm repo, confirm the repo name used at install with `helm repo list`, and optionally `helm fetch` the chart (add `--version=` for a specific one).
3. Review installed Rancher feature charts under **Apps & Marketplace** and update each to the latest within its current release line, so they stay compatible.
4. Capture current values with `helm get values rancher -n cattle-system`, then run `helm upgrade rancher rancher-<CHART_REPO>/rancher --namespace cattle-system` with every value passed as `--set key=value`. Alternatively export `helm get values rancher -n cattle-system -o yaml > values.yaml` and use `-f values.yaml --version=...` to change only the version.
5. Log in to confirm success.

Air gapped installs must first populate the private registry with images for the target version. If cert-manager is v1.5 or below, follow the cert-manager upgrade page first. Deployments from the AWS Marketplace use the release name `rancher-stable`.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: Upgrades. Nothing removed.

Method: documentation only; no commands were run.
