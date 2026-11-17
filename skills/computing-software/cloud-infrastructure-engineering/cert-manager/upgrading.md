---
id: computing-software.cloud-infrastructure-engineering.cert-manager.upgrading
name: upgrading
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [upgrade, helm-upgrade, crds, reset-then-reuse-values, minor-version]
level: practitioner
status: docs-checked
description: "Upgrade cert-manager safely: one minor version at a time, back up first, and use the right Helm or kubectl command depending on how CRDs were installed."
sources:
  - https://cert-manager.io/docs/installation/upgrade/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rules:
- Back up all cert-manager resources first.
- Upgrade one minor version at a time, to the latest patch of that minor, and read each release's notes.
- For large jumps, a full uninstall and reinstall may avoid downtime and needless re-issuance; the page does not guarantee it for every setup (see the reinstall page).

Helm with CRDs installed by the chart (`--set crds.enabled=true`): the CRDs upgrade with the chart.

`helm upgrade --reset-then-reuse-values --version <version> <release_name> oci://quay.io/jetstack/charts/cert-manager`

Helm with CRDs installed separately: apply them first, then run the same upgrade.

`kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/<version>/cert-manager.crds.yaml`

Legacy repo: run `helm repo add jetstack https://charts.jetstack.io --force-update`, then upgrade with `jetstack/cert-manager` as the chart. That repo lags OCI by a few hours, so a new release may not appear yet.

Find the release name with `helm list | grep cert-manager` (usually `cert-manager`).

Static manifests: `kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/<version>/cert-manager.yaml`, then repeat the verify steps from the kubectl install guide.

## Checked

2026-11-03: Confirmed against the Upgrading page: back up first, one minor version at a time to the latest patch, the reinstall caveat without guarantee, `helm upgrade --reset-then-reuse-values --version <version> <release_name> oci://quay.io/jetstack/charts/cert-manager`, CRDs upgraded by Helm when installed with `crds.enabled=true` versus applying `cert-manager.crds.yaml` first, the legacy Jetstack repository and its lag, `helm list | grep cert-manager`, and the static manifest upgrade. Nothing removed.

Method: documentation only; no commands were run.
