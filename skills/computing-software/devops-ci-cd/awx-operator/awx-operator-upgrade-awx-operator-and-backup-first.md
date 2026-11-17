---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-upgrade-awx-operator-and-backup-first
name: awx-operator-upgrade-awx-operator-and-backup-first
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, upgrade, backup, restore, default-awx-version, kustomize, namespace-scoped]
level: practitioner
status: docs-checked
description: "Upgrade AWX by upgrading the operator to the matching tag after a backup, and know the 0.14.0 namespace-scope breaking change."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/upgrade/upgrading.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator upgrade awx operator and backup first

Upgrade AWX by upgrading the operator to the version that maps to the AWX you want. Find the AWX version an operator tag installs by default:

```shell
AWX_OPERATOR_VERSION=2.8.0
docker run --entrypoint="" quay.io/ansible/awx-operator:$AWX_OPERATOR_VERSION bash -c "env | grep DEFAULT_AWX_VERSION"
```

Take a backup, then upgrade via `make deploy` on the desired tag or by applying a `kustomization.yaml` that pins the new operator version.

Backup note: secrets in the cluster work together with the database, so a database backup without the required secrets is not enough. To recover see the restore role documentation, and before restoring delete the old AWX CR and the database PVC from the old deployment (named like `postgres-15-<deployment-name>-postgres-15-0`). Do not delete the namespace or project, since that deletes the backup and its PVC too.

Upgrading to 0.14.0: AWX can only be deployed in the namespace where the operator lives (namespace-scoped operator), and the project moved to operator-sdk 1.x, so delete the old operator first:

```sh
kubectl -n default delete deployment awx-operator
kubectl -n default delete serviceaccount awx-operator
kubectl -n default delete clusterrolebinding awx-operator
kubectl -n default delete clusterrole awx-operator
```

Then install the new operator following Basic Install; the NAMESPACE environment variable must be the namespace in which your old AWX instance resides. Once the new operator is up and running, your AWX deployment is upgraded too.

## Checked

2026-11-04. Confirmed against the AWX Operator "Upgrading" page: the DEFAULT_AWX_VERSION lookup, backup advice, restore prerequisites (including the PVC name pattern), the namespace warning, and the v0.14.0 caveats and delete commands. Nothing removed.
Method: documentation only; no commands were run.
