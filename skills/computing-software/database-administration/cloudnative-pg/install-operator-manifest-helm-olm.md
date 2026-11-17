---
id: computing-software.database-administration.cloudnative-pg.install-operator-manifest-helm-olm
name: install-operator-manifest-helm-olm
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [installation, operator, manifest, helm, olm, cnpg-system, server-side-apply, gke]
level: intro
status: docs-checked
description: "Install the CloudNativePG operator with a server-side applied manifest, the cnpg plugin, Helm or OLM, confirm the controller rollout and handle the GKE webhook firewall issue."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/installation_upgrade.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Direct manifest install uses server-side apply:

```sh
kubectl apply --server-side -f \
  https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/release-1.30/releases/cnpg-1.30.1.yaml
kubectl rollout status deployment \
  -n cnpg-system cnpg-controller-manager
```

To change defaults before installing, generate a manifest with the plugin, for example restricting the watched namespace:

```shell
kubectl cnpg install generate \
  --watch-namespace "specific-namespace" \
  > cnpg_for_specific_namespace.yaml
```

Other routes: the Helm chart from `cloudnative-pg/charts`, or OLM from OperatorHub.io. Development snapshots from `cloudnative-pg/artifacts` are unsupported and not for production.

The operator runs in namespace `cnpg-system` as a Deployment named `cnpg-controller-manager` (manifest or plugin) or `cnpg-cloudnative-pg` (Helm; override with `fullnameOverride`). One replica is the default; for operator-level HA raise the replicas, since leader election is supported, and use taints and tolerations to keep it off the nodes running PostgreSQL.

On GKE, a `failed to call webhook` error means the firewall blocks control-plane to node traffic. Either change the webhook service `targetPort` to an allowed port or open webhook port `9443`.

## Checked

2026-11-04. Install commands, deployment names, GKE webhook note and leader-election remark confirmed on the Installation and upgrades page (release-1.30 manifest URL as printed there).

Method: documentation only; no commands were run.
