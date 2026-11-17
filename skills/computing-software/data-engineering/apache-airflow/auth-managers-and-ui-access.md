---
id: computing-software.data-engineering.apache-airflow.auth-managers-and-ui-access
name: auth-managers-and-ui-access
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, auth-manager, simple-auth-manager, fab-auth-manager, rbac]
level: advanced
status: docs-checked
description: "Choose and configure an Airflow auth manager: Simple auth manager for dev, FAB for roles/LDAP/OAuth, and the Airflow 3 API token flow for the UI and REST API."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/auth-manager/index.html
  - https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/auth-manager/simple/index.html
  - https://airflow.apache.org/docs/apache-airflow-providers-fab/stable/auth-manager/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auth managers and UI access control

**Goal:** control who can log in to Airflow and what they can see or trigger.

## Airflow 3 model
Authentication and authorization are pluggable **auth managers** (`[core] auth_manager`). The UI and REST API both use JWT tokens issued by the auth manager.

## Simple auth manager (default in Airflow 3; dev/test)
```ini
[core]
auth_manager = airflow.api_fastapi.auth.managers.simple.simple_auth_manager.SimpleAuthManager
simple_auth_manager_users = alice:admin,bob:viewer,ci:op
# simple_auth_manager_all_admins = True   # local only: everyone admin, no login
```
Roles: `viewer`, `user`, `op`, `admin`. Passwords are stored in the file named by `[core] simple_auth_manager_passwords_file`. Not for production.

## FAB auth manager (roles, LDAP, OAuth)
```bash
pip install apache-airflow-providers-fab
```
```ini
[core]
auth_manager = <FAB_AUTH_MANAGER_CLASS_PATH>   # class path is given in the FAB provider docs
```
Configure the identity provider, role mapping and per-DAG permissions as described in the FAB provider's auth-manager documentation (see sources).
Users: `airflow users create --role Admin ...` (FAB CLI).

## Other managers
Providers can ship their own auth managers (for example a Keycloak auth manager). Pick one that matches your SSO.

## REST API tokens (Airflow 3)
`POST /auth/token` with credentials returns a JWT; send `Authorization: Bearer <token>` to `/api/v2/...`.

## Gotchas
- Switching auth manager changes where users and roles live; plan a migration.
- Leaving `all_admins` on in a shared environment is an open door.

## Verify
Log in as a viewer: trigger/clear buttons disabled, restricted DAGs hidden; an API call without a token is rejected.

## Checked

2026-10-28. Confirmed in the Airflow configuration reference and auth-manager pages: `[core] auth_manager`, the Simple auth manager class and its settings (`simple_auth_manager_users`, `simple_auth_manager_all_admins`, `simple_auth_manager_passwords_file`), roles viewer/user/op/admin, `POST /auth/token` issuing a JWT, a Keycloak auth manager, `airflow users create -r Admin` (FAB). Removed: FAB class path, `webserver_config.py` keys, FAB built-in roles, the `access_control` example and warning claim, the AWS auth manager claim, and the generated-password file name.
Method: documentation only; no commands were run.
