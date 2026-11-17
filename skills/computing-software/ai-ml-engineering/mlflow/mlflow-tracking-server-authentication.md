---
id: computing-software.ai-ml-engineering.mlflow.mlflow-tracking-server-authentication
name: mlflow-tracking-server-authentication
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, mlflow-authentication, mlflow-tracking-server, basic-auth, permissions, security]
level: practitioner
status: docs-checked
description: "Secure an MLflow tracking server: built-in basic-auth app, users and experiment/model permissions, admin setup, client credentials, and reverse-proxy/SSO alternatives."
sources:
  - https://mlflow.org/docs/latest/self-hosting/security/basic-http-auth/
  - https://mlflow.org/docs/latest/self-hosting/security/role-based-access-control/
  - https://mlflow.org/docs/latest/self-hosting/security/sso/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tracking server authentication and permissions

**Default reality:** `mlflow server` has no authentication. Anyone who can reach the port can read, delete and overwrite experiments and models. Never expose it unauthenticated.

## Built-in basic auth
```bash
mlflow server --app-name basic-auth \
  --backend-store-uri postgresql://mlflow:***@db/mlflow \
  --artifacts-destination s3://ml-artifacts --host 0.0.0.0 --port 5000
```
- Install the extra (`pip install 'mlflow[auth]'`) and set `MLFLOW_FLASK_SERVER_SECRET_KEY` (CSRF protection; use the same value on every server).
- Config file via `MLFLOW_AUTH_CONFIG_PATH` (ini; the default is `mlflow/server/auth/basic_auth.ini`): `default_permission` (READ, USE, EDIT, MANAGE or NO_PERMISSIONS; default READ), `database_uri` (where permission and user data are stored), `admin_username` and `admin_password` (the admin user created on first start; the env vars `MLFLOW_AUTH_ADMIN_USERNAME` and `MLFLOW_AUTH_ADMIN_PASSWORD` override them).
- There is no default admin password: on first start the server creates the admin user from `MLFLOW_AUTH_ADMIN_PASSWORD` (or `admin_password`) and refuses to start if neither is set. Passwords must be at least 12 characters. For least privilege set `default_permission` to `NO_PERMISSIONS` (the default is READ).

## Manage users and permissions
```python
from mlflow.server import get_app_client
auth = get_app_client("basic-auth", tracking_uri="https://mlflow.example.com")
auth.create_user(username="alice", password="...")
auth.grant_user_permission("alice", "experiment", "12", "EDIT")
auth.grant_user_permission("ci-bot", "registered_model", "fraud-model", "MANAGE")
```
The creator of a resource automatically receives MANAGE on it. Grants cover experiments, registered models, prompts, scorers and AI Gateway resources, and a request without the required permission gets `403 Forbidden`. Since MLflow 3.13.0 permissions are granted through roles (RBAC): for shared sets use `create_role`, `add_role_permission` and `assign_role`; the legacy per-resource methods such as `create_experiment_permission()` were removed in 3.13.0.

## Clients
`export MLFLOW_TRACKING_USERNAME=alice MLFLOW_TRACKING_PASSWORD=...` (or `MLFLOW_TRACKING_TOKEN` behind a token proxy). In CI use a dedicated service user with the narrowest permission.

## Production hardening
- Terminate TLS at a reverse proxy (nginx, ALB, ingress) in front of MLflow; basic auth over plain HTTP leaks passwords.
- For SSO, use an authentication plugin such as `mlflow-oidc-auth` (OIDC) or a reverse proxy, as described on the SSO page of the self-hosting docs.
- Artifact access: with `--artifacts-destination` (artifact serving is on by default) the server proxies artifacts, so clients do not need direct bucket credentials; otherwise clients talk to the bucket directly and need their own credentials.

## Verify
- [ ] An unauthenticated request to `https://mlflow.example.com/api/2.0/mlflow/experiments/search` is refused and returns no data.
- [ ] A READ user cannot delete a run (expect 403).

## Checked

- Date: 2026-10-25. Release: MLflow 3.17.2 (released 2026-10-20); documentation and source read from the master branch of mlflow/mlflow (docs/docs, mlflow/, CHANGELOG.md) on 2026-10-25.
- `mlflow server --app-name basic-auth`, `mlflow[auth]`, `MLFLOW_FLASK_SERVER_SECRET_KEY`, no default admin password and the 12-character minimum, config keys and env overrides, permission levels READ/USE/EDIT/MANAGE/NO_PERMISSIONS with default READ, creator gets MANAGE, 403 on missing permission, `get_app_client("basic-auth", tracking_uri=...)`, `MLFLOW_TRACKING_USERNAME`/`MLFLOW_TRACKING_PASSWORD`: docs/self-hosting/security/basic-http-auth.mdx.
- RBAC (3.13.0): `grant_user_permission(username, resource_type, resource_id, permission)`, `create_role`/`add_role_permission`/`assign_role`, removal of the legacy per-resource methods: docs/self-hosting/security/role-based-access-control.mdx and CHANGELOG.md. SSO options: security/sso.mdx.
- `--artifacts-destination` / `--serve-artifacts` (default on): mlflow/cli/__init__.py and mlflow/utils/cli_args.py.
- Removed as unconfirmed: the auth DB being separate from the tracking DB, managed MLflow alternatives, and the claim that direct bucket access bypasses MLflow permissions. The old `ml/auth` link now redirects and was replaced.

Method: documentation only; no commands were run.
