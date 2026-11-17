---
id: computing-software.devops-ci-cd.argo-workflows.database-iam-authentication
name: database-iam-authentication
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [azure-token, aws-rds-token, iam-authentication, postgresql-ssl, db-proxy-sidecar]
level: advanced
status: docs-checked
description: "Connect the controller to PostgreSQL with short-lived Azure Entra ID or AWS RDS IAM tokens instead of a static password."
sources: ["https://argo-workflows.readthedocs.io/en/latest/workflow-archive/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database IAM token authentication
Available from v4.1, PostgreSQL only. With token auth, `passwordSecret` is unused, but `userNameSecret` is still needed and must hold the database user mapped to your cloud identity. Only one token mechanism may be enabled. The settings are part of the shared database configuration, so they apply to archive, synchronization and node status offloading databases too.

Azure (Entra ID):
```yaml
postgresql:
  host: example.postgres.database.azure.com
  ssl: true
  sslMode: require
  userNameSecret: {name: argo-postgres-config, key: username}
  azureToken:
    enabled: true
```
A token is requested per new connection through the default Azure credential chain (Workload Identity, Managed Identity, others). Scope defaults to `https://ossrdbms-aad.database.windows.net/.default`; override with `azureToken.scope`.

AWS RDS:
```yaml
postgresql:
  host: example.eu-west-1.rds.amazonaws.com
  ssl: true
  awsRDSToken:
    enabled: true
    region: eu-west-1
```
Uses the default AWS credential chain (IRSA, instance profiles). `region` is optional and auto-detected. `ssl: true` is mandatory.

Other providers: run the vendor database proxy as a sidecar (the page cites CloudSQL Proxy on GCP) and point the config at the local proxy address with the IAM username and an empty string password.

## Checked

2026-11-08. Read the Argo Workflows workflow archive page in full (raw markdown) including the IAM-based authentication section and confirmed v4.1 availability, userNameSecret requirement, Azure and AWS RDS settings, default scope, SSL requirement, and the sidecar proxy alternative. Nothing removed.

Method: documentation only; no commands were run.
