---
id: computing-software.data-engineering.data-warehouse-architecture.secrets-management-for-pipelines
name: secrets-management-for-pipelines
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, data-security, pipeline-secrets, secrets-manager, workload-identity, credential-rotation, vault, least-privilege]
level: practitioner
status: docs-checked
description: "Manage credentials for data pipelines: secrets managers vs workload identity, wiring Airflow/dbt/Spark/Connect to them, rotation without downtime, scanning and least privilege."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
  - https://airflow.apache.org/docs/apache-airflow/stable/security/secrets/secrets-backend/index.html
  - https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secrets management for pipelines

**Goal:** no passwords in code, configs, images or logs; every credential is scoped, rotatable and auditable.

## Prefer no secret at all: workload identity
- Cloud workloads can assume roles or managed identities instead of holding keys; use your cloud's workload identity feature.
- CI: GitHub Actions OIDC to cloud roles instead of long-lived keys.

## When a secret is unavoidable: secrets manager
AWS Secrets Manager / SSM, GCP Secret Manager, Azure Key Vault, HashiCorp Vault. Pipelines fetch at runtime with their identity.

## Wiring common tools
| Tool | Mechanism |
|---|---|
| Airflow | a secrets backend configured in the `[secrets]` section (see the Airflow secrets backend docs for the backend class of your secrets manager) |
| dbt | env vars in profiles (`{{ env_var('DBT_ENV_SECRET_PASSWORD') }}`); `DBT_ENV_SECRET_` prefix is scrubbed from logs; inject from the orchestrator/CI secret store |
| Spark / Databricks | Databricks secret scopes (`dbutils.secrets.get`, redacted in output), or cloud IAM for storage; Spark on k8s with mounted secrets |

## Rotation
- Dual-credential pattern: create new credential, deploy consumers using it, revoke old (Snowflake `RSA_PUBLIC_KEY_2`, two DB users, two API keys).
- Rotate on schedule (e.g. 90 days) and immediately on staff departure or exposure.

## Detection and hygiene
- Secret scanning in repos and CI, and pre-commit hooks.
- Redact in logs: Airflow masks connection passwords and variables with sensitive names; extend `sensitive_var_conn_names`.
- One credential per pipeline/service (not a shared "etl" user): blast radius and audit trail.
- Least privilege: read-only for extractors, write only to target schemas.

## Gotchas
- Secrets baked into Docker images or notebooks persist in layers/history; rotate if it happened.
- Environment variables leak via debug endpoints, crash dumps and `ps e`; prefer file mounts or runtime fetch for highly sensitive values.
- Caching secrets forever defeats rotation.

## Verify
- [ ] Secret scan of all data repos clean; push protection enabled.
- [ ] Inventory lists each credential, owner, scope and last rotation date.

## Checked

2026-10-28. Confirmed: dbt `env_var` page (`DBT_ENV_SECRET` prefix variables for profiles.yml and packages.yml), Databricks secrets page (`dbutils.secrets.get`, values redacted), Snowflake key-pair page (`RSA_PUBLIC_KEY_2`, up to two public keys per user), Airflow mask-sensitive-values page (`sensitive_var_conn_names`). Removed: IRSA/EKS Pod Identity and federation claims, the Airflow backend class path, the Kafka Connect, Kubernetes and Terraform rows, AWS rotation Lambdas and named scanners (not in the cited pages).

Method: documentation only; no commands were run.
