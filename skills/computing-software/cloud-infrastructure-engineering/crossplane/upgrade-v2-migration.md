---
id: computing-software.cloud-infrastructure-engineering.crossplane.upgrade-v2-migration
name: upgrade-v2-migration
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [upgrade, helm, v2, migration, removed-features]
level: advanced
status: docs-checked
description: "Upgrade Crossplane one minor version at a time and clear removed features before moving to v2."
sources:
  - https://docs.crossplane.io/latest/guides/upgrade-crossplane/
  - https://docs.crossplane.io/latest/guides/upgrade-to-crossplane-v2/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Upgrade with Helm, one minor version at a time using the latest patch of each:

```shell
helm repo update
helm upgrade crossplane --namespace crossplane-system crossplane-stable/crossplane
```

Helm keeps your original flags. Without `helm repo update` you get the last cached chart. Path example: v1.18 to v1.19 to v1.20 to v2.0.

Upgrade to v2 only from v1.20. Before upgrading, clear what v2 removes:

- Native patch and transform (`spec.mode: Resources`): convert with the v1.20 CLI, `crossplane beta convert pipeline-composition old.yaml -o new.yaml`.
- ControllerConfig: `crossplane beta convert deployment-runtime controller-config.yaml -o deployment-runtime-config.yaml`.
- External secret stores: move to native Secrets or External Secrets Operator.
- XR connection details (MRs unaffected): compose your own Secret.
- The default registry flag `--registry`: every package needs a fully qualified name; check with `kubectl get pkg -o wide`.

`crossplane beta upgrade check`, from the v1.20 CLI, scans for all of these.

Order: prepare, upgrade core, configure activation policies, upgrade providers, then adopt v2 features. Existing v1 cluster-scoped XRs and MRs keep working; no tool migrates them to namespaced style yet.

## Checked

Checked against the upgrade-crossplane and upgrade-to-crossplane-v2 guides, read in full: one-minor-at-a-time rule, helm repo update and helm upgrade, v1.20 prerequisite, the five removed features with their convert commands, beta upgrade check, kubectl get pkg -o wide, upgrade order, and the note on no automated XR/MR migration.

Method: docs-checked 2026-11-09 against the upgrade-crossplane and upgrade-to-crossplane-v2 guides (docs repo raw markdown).
