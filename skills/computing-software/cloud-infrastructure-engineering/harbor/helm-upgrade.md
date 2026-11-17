---
id: computing-software.cloud-infrastructure-engineering.harbor.helm-upgrade
name: helm-upgrade
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [helm-upgrade, helm-rollback, tls-secret, harbor-helm, database-backup]
level: practitioner
status: docs-checked
description: "Upgrade Harbor deployed by Helm chart: back up the database, keep the generated TLS certificate, and why helm rollback is unsupported."
sources:
  - https://goharbor.io/docs/main/administration/upgrade/helm-upgrade/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The guide covers Harbor deployed by chart since version 0.3.0.

Notes:
- The database schema may change between versions and is migrated during the upgrade, so downtime cannot be avoided.
- Schemas cannot be downgraded automatically, so `helm rollback` is not supported.

Procedure:
1. Back up the database Harbor uses, in case the upgrade fails.
2. Download the new chart.
3. Configure the new chart with the same values as the old one.
4. Run `helm upgrade release-name --force .`. The `--force` is needed when upgrading from 0.3.0 because of harbor-helm issue 30.

TLS gotcha: if TLS is on and the chart generated the certificate, the upgrade generates a new certificate that overwrites the old one, which hurts you if you distributed the old certificate. To keep it:
1. `kubectl get secret` and find the secret ending in `-harbor-ingress` (service exposed via Ingress) or `-harbor-nginx` (ClusterIP or NodePort).
2. `kubectl get secret <secret-name> -o yaml > secret.yaml`.
3. Change `metadata.name` in `secret.yaml` to a new name.
4. `kubectl create -f secret.yaml`.
5. Set `expose.tls.secretName` in the chart values to that new name.

Known issue: job logs are lost when upgrading from 0.3.0 because they were stored in an `emptyDir`.

## Checked

- 2026-11-03: concrete claims (parameter names, defaults, steps, limits, UI labels) read against the official Harbor docs: Upgrading Harbor Deployed with Helm.
Method: documentation only; no commands were run.
