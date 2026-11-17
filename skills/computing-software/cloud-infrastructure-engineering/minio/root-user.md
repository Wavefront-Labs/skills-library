---
id: computing-software.cloud-infrastructure-engineering.minio.root-user
name: root-user
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, root-user, minio-root-user, minio-root-password, minioadmin, credential-rotation, deprecated-access-key-variables]
level: intro
status: docs-checked
description: "Set and rotate the MinIO root user through MINIO_ROOT_USER and MINIO_ROOT_PASSWORD, avoid the minioadmin defaults and know the deprecated MINIO_ACCESS_KEY variables."
sources: ["https://github.com/minio/docs/blob/main/source/administration/identity-access-management/minio-user-management.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO root user

Every deployment has a `root` user with access to all actions and resources regardless of the configured identity manager. At first start the server reads:
- `MINIO_ROOT_USER`
- `MINIO_ROOT_PASSWORD`

If unset, MinIO falls back to `minioadmin` / `minioadmin`, which the docs strongly discourage in every environment.

## Guidance from the docs
- Use long, unique, random values and restrict who can retrieve them to trusted people who need superuser access.
- Do not use root for regular client access in development, staging or production. Create users with minimal actions and resources per workload (`computing-software.cloud-infrastructure-engineering.minio.users-and-access-keys`).
- Rotating the credentials means updating either or both variables on **all** MinIO servers in the deployment.
- Deprecated since RELEASE.2021-04-22T15-44-28Z: `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`, `MINIO_ACCESS_KEY_OLD` and `MINIO_SECRET_KEY_OLD`.

## Related behaviour
- Root cannot modify COMPLIANCE-locked objects (`computing-software.cloud-infrastructure-engineering.minio.object-locking`).
- Root access keys are not synced by site replication, and a new peer site must use the same root credentials as existing ones (`computing-software.cloud-infrastructure-engineering.minio.site-replication-setup`).

## Checked

2026-11-03. Confirmed against the MinIO docs source: user-management page: root variables, minioadmin fallback, deprecated access key variables and their release. Removed or fixed: nothing.

Method: documentation only; no commands were run.
