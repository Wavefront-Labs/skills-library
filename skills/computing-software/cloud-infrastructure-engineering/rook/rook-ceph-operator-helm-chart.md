---
id: computing-software.cloud-infrastructure-engineering.rook.rook-ceph-operator-helm-chart
name: rook-ceph-operator-helm-chart
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [helm, operator-chart, rook-release, crds-enabled, monitoring-enabled]
level: practitioner
status: docs-checked
description: "Install the rook-ceph operator Helm chart with the release repo and know key values such as crds.enabled, monitoring.enabled and logLevel."
sources:
  - https://rook.io/docs/rook/latest-release/Helm-Charts/operator-chart/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The operator chart bootstraps a `rook-ceph-operator` deployment. It requires Helm 3.13 or newer. The recommended flow is install this chart, install the Ceph-CSI drivers chart so CSI can provision and mount volumes, then create a cluster.

Install from the release channel, preferably into the `rook-ceph` namespace (clusters go into separate namespaces):
```
helm repo add rook-release https://charts.rook.io/release
helm install --create-namespace --namespace rook-ceph rook-ceph rook-release/rook-ceph -f values.yaml
```

Selected values and defaults from the configuration table:
- `crds.enabled`: true. Whether the chart creates and updates CRDs. If false, manage them with `deploy/examples/crds.yaml`. Set only at first deployment; disabling later may destroy the cluster, and deleted CRDs require the disaster recovery guide.
- `logLevel`: "INFO" (ERROR, WARNING, INFO, DEBUG).
- `monitoring.enabled`: false. Needs Prometheus pre-installed; also creates RBAC for ServiceMonitors.
- `allowLoopDevices`: false, loop devices for OSDs in test clusters.
- `cephCommandsTimeoutSeconds`: "15".
- `currentNamespaceOnly`: false.
- `enableDiscoveryDaemon`: false; `disableDeviceHotplug`: false.
- `csi.installCsiOperator`: true, installs the ceph-csi-operator subchart.
- `image.repository`: `docker.io/rook/ceph`, `image.pullPolicy`: IfNotPresent.
- `containerSecurityContext` runs as non-root user and group 2016 with all capabilities dropped.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (operator-chart) against this skill: 21 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 0 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
