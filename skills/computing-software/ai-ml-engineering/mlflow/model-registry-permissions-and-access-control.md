---
id: computing-software.ai-ml-engineering.mlflow.model-registry-permissions-and-access-control
name: model-registry-permissions-and-access-control
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, registry-permissions, access-control, unity-catalog, basic-auth, rbac]
level: practitioner
status: docs-checked
description: "Control who can register, promote and load models: MLflow basic-auth and role-based access control for registered models, with pointers for managed registries."
sources:
  - https://mlflow.org/docs/latest/self-hosting/security/basic-http-auth/
  - https://mlflow.org/docs/latest/self-hosting/security/role-based-access-control/
  - https://mlflow.org/docs/latest/self-hosting/security/sso/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Registry permissions and access control

**Goal:** data scientists can register models, only CI or approvers can move production aliases, and serving identities can read but not change models.

## Role design (any backend)
| Principal | Needs |
|---|---|
| Data scientists | create models/versions in dev namespace, read prod |
| CI promotion service | set aliases on prod models |
| Serving / batch identities | read (load) specific models only |
| Platform admins | manage permissions |
Use groups and service principals, never personal accounts in pipelines.

## Open-source MLflow (basic-auth app)
Start the server with `mlflow server --app-name basic-auth ...` (needs `pip install 'mlflow[auth]'`). Permissions are `READ`, `USE`, `EDIT`, `MANAGE` and `NO_PERMISSIONS`, granted per resource; `default_permission` in the auth config (default `READ`) applies to everything without an explicit grant, so set it to `NO_PERMISSIONS` in shared deployments.
```python
from mlflow.server import get_app_client
auth = get_app_client("basic-auth", tracking_uri="https://mlflow.internal")
auth.create_user("svc-serving", password=secret)
auth.grant_user_permission("svc-serving", "registered_model", "churn", "READ")
auth.grant_user_permission("ci-promoter", "registered_model", "churn", "MANAGE")
```
The creator of a model gets `MANAGE` automatically. Since MLflow 3.13.0 grants flow through roles (`create_role`, `add_role_permission`, `assign_role`), which bundle grants for sets of users; the legacy per-resource methods (`create_registered_model_permission`, `update_registered_model_permission`) were removed in 3.13.0. Registered models and prompts are separate resource types: a registered-model grant does not satisfy a request for a prompt with the same name. For SSO see the SSO page of the self-hosting docs.

## Databricks and Unity Catalog
The Databricks workspace registry ACLs and Unity Catalog model grants are defined by Databricks and change over time. Take privilege and ACL names from the current Databricks documentation; this skill was checked against the open-source MLflow documentation only.

Promotion across environments is usually copying a version from the dev model to the prod model (`copy_model_version`) by a principal with rights on both, which keeps prod writes in CI.

## Audit
Enable and retain audit logs for your platform (for open-source MLflow, reverse-proxy and server logs) and alert on alias changes to production models outside CI.

## Verify
- [ ] The serving identity cannot set an alias or delete a version (try it).
- [ ] A data scientist cannot change the prod alias.
- [ ] Alias changes appear in audit logs with the acting principal.

## Checked

- Date: 2026-10-25. Release: MLflow 3.17.2 (released 2026-10-20); documentation and source read from the master branch of mlflow/mlflow (docs/docs, mlflow/, CHANGELOG.md) on 2026-10-25.
- Permission levels, default `READ`, `403` on missing permission, creator gets MANAGE, resource types (experiment, registered model, prompt, scorer, AI Gateway) and the prompt-versus-model separation: docs/self-hosting/security/basic-http-auth.mdx.
- `grant_user_permission(username, resource_type, resource_id, permission)`, roles API, legacy method removal in 3.13.0: role-based-access-control.mdx and CHANGELOG.md.
- Databricks workspace ACL names, Unity Catalog `GRANT` statements and `system.access.audit` were removed: Databricks documentation is not published in a public repository, so the skill now defers to it instead of stating privilege names.

Method: documentation only; no commands were run.
