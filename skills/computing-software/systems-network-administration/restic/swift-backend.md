---
id: computing-software.systems-network-administration.restic.swift-backend
name: swift-backend
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, openstack, swift, keystone, backend]
level: advanced
status: docs-checked
description: "Configure the OpenStack Swift backend with Keystone v1, v2 or v3 environment variables, application credentials or token authentication."
sources:
  - https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenStack Swift backend

URL form: container, then optional path. The container is created automatically.

```
restic -r swift:container_name:/path init
```

Restic should be compatible with an OpenStack RC file in most cases.

## Credential sets

- Keystone v1: `ST_AUTH`, `ST_USER`, `ST_KEY`
- Keystone v2: `OS_AUTH_URL`, `OS_REGION_NAME`, `OS_USERNAME`, `OS_PASSWORD`, `OS_TENANT_ID`, `OS_TENANT_NAME`
- Keystone v3: `OS_AUTH_URL`, `OS_REGION_NAME`, `OS_USERNAME`, `OS_USER_ID`, `OS_PASSWORD`, `OS_USER_DOMAIN_NAME`, `OS_USER_DOMAIN_ID`, `OS_PROJECT_NAME`, `OS_PROJECT_DOMAIN_NAME`, `OS_PROJECT_DOMAIN_ID`, `OS_TRUST_ID`
- Application credential by ID: `OS_APPLICATION_CREDENTIAL_ID` and `OS_APPLICATION_CREDENTIAL_SECRET`
- By name: `OS_APPLICATION_CREDENTIAL_NAME` and `OS_APPLICATION_CREDENTIAL_SECRET`, plus `OS_USERNAME`, `OS_USER_DOMAIN_NAME` and `OS_AUTH_URL`
- Pre-obtained token: `OS_STORAGE_URL` and `OS_AUTH_TOKEN`

`SWIFT_DEFAULT_CONTAINER_POLICY` sets the storage policy for a container restic creates.

## Checked

2026-11-03. Confirmed in the restic docs page Preparing a new repository (OpenStack Swift section) and Scripting: URL form with optional path, automatic container creation, each credential set and its variables (several are optional), `SWIFT_DEFAULT_CONTAINER_POLICY`, RC file compatibility. Removed: the application-credential recommendation and the environment-debugging paragraph (not in the docs).

Method: documentation only; no commands were run.
