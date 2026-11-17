---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-database-managed-postgresql-resources-storage
name: awx-operator-database-managed-postgresql-resources-storage
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, managed-postgres, postgres-storage-class, resource-requirements, sclorg, hostpath, data-volume-init]
level: practitioner
status: docs-checked
description: "Tune the operator-managed PostgreSQL: image, resources, storage, class and the init container for hostPath-style volumes."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/database-configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator database managed postgresql resources storage

Without an external database the operator deploys PostgreSQL next to AWX. Customizable fields (defaults in brackets): `postgres_image` (quay.io/sclorg/postgresql-15-c9s), `postgres_image_version` (latest), `postgres_resource_requirements` (requests cpu 10m, memory 64Mi), `postgres_storage_requirements` (requests storage 8Gi), `postgres_storage_class` (empty, meaning the cluster default class), `postgres_priority_class` and `postgres_extra_settings`.

```yaml
spec:
  postgres_resource_requirements:
    requests: {cpu: 500m, memory: 2Gi}
    limits: {cpu: '1', memory: 4Gi}
  postgres_storage_requirements:
    requests: {storage: 8Gi}
    limits: {storage: 50Gi}
  postgres_storage_class: fast-ssd
```

Image: use the default sclorg image. Moving from the old `postgres:13` Docker Hub image, upgrading from operator 2.12.2 or lower to 2.15.0 or higher migrates data to the new image. You can no longer set `postgres_data_path`, as it is hardcoded in that image; a custom image like `postgres:15` has a different data directory and is not interchangeable.

Permissions: with hostPath-backed PVCs and some storage classes (such as Longhorn) the data dir must be writable by UID 26. Set `postgres_data_volume_init: true` to use an init container, and customize with `postgres_init_container_commands` such as `chown 26:0 /var/lib/pgsql/data` and `chmod 700 /var/lib/pgsql/data`.

## Checked

2026-11-04. Confirmed against the AWX Operator "Database Configuration" page (Managed PostgreSQL Service, image-override and Initialize Postgres data volume sections): field names, defaults, example, image note and init-container settings. Nothing removed.
Method: documentation only; no commands were run.
