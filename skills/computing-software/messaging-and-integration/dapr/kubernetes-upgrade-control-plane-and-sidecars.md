---
id: computing-software.messaging-and-integration.dapr.kubernetes-upgrade-control-plane-and-sidecars
name: kubernetes-upgrade-control-plane-and-sidecars
category: computing-software
field: messaging-and-integration
product: dapr
tags: [kubernetes, upgrade, helm, crds, rollout-restart, dapr-upgrade]
level: practitioner
status: docs-checked
description: "Upgrade Dapr on Kubernetes with dapr upgrade -k or Helm: replace CRDs first, upgrade the chart, then rollout restart app deployments so sidecars pick up the new runtime."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/hosting/kubernetes/kubernetes-upgrade.md
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/hosting/kubernetes/kubernetes-production.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Upgrading is two phases: control plane, then data plane (the sidecars).

CLI route:

```bash
dapr upgrade -k --runtime-version=<version>
```

Helm values can be passed through the CLI. Known issue: clusters that once ran a version before 1.0.0-rc.2 may hold an incompatible `configurations.dapr.io` CustomResourceDefinition ("spec.preserveUnknownFields: Invalid value: true"). Fix it by running `kubectl replace -f` on the `charts/dapr/crds/configuration.yaml` file of the target release, then rerun the upgrade.

Helm route: the page says Helm does not handle upgrading resources (the CRDs), so do it manually first; the resources are backward-compatible and should only be installed forward. The page replaces `components.yaml`, `configuration.yaml` and `subscription.yaml` and applies `resiliency.yaml` and `httpendpoints.yaml`, all from `charts/dapr/crds/` of the target release tag in the dapr/dapr repository. Then:

```bash
helm repo update
helm upgrade dapr dapr/dapr --version <version> --namespace dapr-system --wait
```

Add `--values` if you use a values file. Existing certificate values are reused automatically (from 1.0.0 on).

Data plane: sidecars only change when pods restart.

```bash
kubectl rollout restart deploy/<DEPLOYMENT-NAME>
```

List Dapr-enabled deployments with `dapr list -k` or the dashboard. The page points to the Dapr version policy for the supported upgrade path.

## Checked

2026-11-08. Read the cited dapr/docs v1.15 page in full and compared each claim; wording tightened where it went beyond the page, the remaining claims are unchanged.

Method: documentation only; no commands were run.
