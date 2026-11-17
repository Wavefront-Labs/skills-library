---
id: computing-software.cybersecurity-defensive.zitadel.helm-database-tls-and-operations
name: helm-database-tls-and-operations
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, kubernetes, helm, postgresql, upgrades, autoscaling]
level: advanced
status: docs-checked
description: "Connect the ZITADEL Helm chart to PostgreSQL with TLS, upgrade releases safely and enable autoscaling."
sources:
  - https://zitadel.com/docs/self-hosting/deploy/kubernetes/database
  - https://zitadel.com/docs/self-hosting/deploy/kubernetes/operations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Database: store the DSN in a Kubernetes Secret and pass it as `ZITADEL_DATABASE_POSTGRES_DSN` through `zitadel.env` with `secretKeyRef`. TLS choices:

- `sslmode=disable`: no encryption; only for tests or a private network.
- `sslmode=require`: encrypted but the server certificate is not verified, so it does not stop man-in-the-middle attacks.
- Full verification: use `sslmode=verify-full` with a CA certificate. Put the CA in a secret and set `dbSslCaCrt` and `dbSslCaCrtSecret` in the values.

Upgrades: review release notes, back up the database, update `values.yaml`, then:

```bash
helm repo update
helm upgrade my-zitadel zitadel/zitadel --values values.yaml --version <target-version>
```

Watch pods with `kubectl get pods --watch` and check `helm status`. For v3 to v4 follow the dedicated upgrade guide. Newer charts may deploy Login V2 by default, which does not enable it on existing instances; set `login.enabled: false` if you are not adopting it yet.

Scaling: set `replicaCount`, or enable the autoscaler:

```yaml
zitadel:
  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 10
    targetCPUUtilizationPercentage: 80
```

Also configure resource requests and limits; the operations page gives example sizing.

## Checked

2026-11-08. Read in full: the Kubernetes database page and the operations page. Reworded the closing resource advice to what the page states.

Method: documentation only; no commands were run.
