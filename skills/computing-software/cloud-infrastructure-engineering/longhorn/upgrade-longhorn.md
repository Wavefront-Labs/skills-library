---
id: computing-software.cloud-infrastructure-engineering.longhorn.upgrade-longhorn
name: upgrade-longhorn
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [upgrade, helm-upgrade, rollback, global-manager, gitops]
level: advanced
status: docs-checked
description: "Upgrade Longhorn to 1.13.0 from 1.12.x with kubectl, Helm or GitOps tools, preconditions, failure behaviour and rollback."
sources:
  - https://longhorn.io/docs/1.13.0/deploy/upgrade/longhorn-manager/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: upgrade the Longhorn manager safely.

Supported path: upgrade to v1.13.0 only from v1.12.x; older versions must go through v1.12.x first. Engine live upgrade is supported from v1.12.x to v1.13.0.

Before upgrading:
- Back up volumes.
- v1.13.0 also creates the Longhorn Global Manager Deployment; at least one of its pods must be schedulable.
- Helm or Rancher chart installs: leave default StorageClass parameters (`numberOfReplicas`, `staleReplicaTimeout`, `fromBackup`, `baseImage`) unchanged or the chart upgrade may fail; copy the StorageClass under a new name to change it.
- Rancher: upgrade in the same UI used to install.

Commands:

```bash
kubectl apply -f https://raw.githubusercontent.com/longhorn/longhorn/v1.13.0/deploy/longhorn.yaml
helm upgrade longhorn longhorn/longhorn --namespace longhorn-system --version 1.13.0
```

GitOps: Helm Controller `spec.version: v1.13.0` (set `failurePolicy: abort`; the default `reinstall` uninstalls Longhorn on a failed upgrade), Fleet `helm.version`, Flux `spec.chart.spec.version`, Argo CD `targetRevision`.

Then upgrade the engines.

Failures: with kubectl the upgrade is blocked, reason in `longhorn-manager` logs; reapply the previous manifest and delete new components. With Helm a `pre-upgrade` job blocks it and records FailedUpgradePreCheck; use `helm rollback longhorn [REVISION]` (see `helm history longhorn`).

Error `updates to provisioner are forbidden` means the default StorageClass was modified; delete the deprecated one before upgrading.

## Checked

2026-11-08. Read in full against https://longhorn.io/docs/1.13.0/deploy/upgrade/longhorn-manager/ : supported path, Global Manager note, StorageClass parameters, upgrade commands per tool, failure and rollback behaviour. Nothing else was removed.

Method: documentation only; no commands were run.
