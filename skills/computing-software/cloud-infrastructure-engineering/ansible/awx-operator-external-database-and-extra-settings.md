---
id: computing-software.cloud-infrastructure-engineering.ansible.awx-operator-external-database-and-extra-settings
name: awx-operator-external-database-and-extra-settings
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, controller-install, external-postgres, external-database, extra-settings, awx-spec, awx-operator]
level: advanced
status: docs-checked
description: "Point an AWX deployed by the operator at an external PostgreSQL database and set controller settings with extra_settings and extra_settings_files in the AWX custom resource."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/database-configuration.md", "https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/advanced-configuration/extra-settings.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWX operator: external database and extra_settings

## External PostgreSQL
The operator can run Postgres itself (managed, the default when no `postgres_configuration_secret` is set), but
production usually uses a managed database with backups and HA handled there.

```yaml
apiVersion: v1
kind: Secret
metadata: {name: awx-postgres-configuration, namespace: awx}
stringData:
  host: <external host resolvable by the cluster>
  port: "5432"
  database: awx
  username: awx
  password: <from your secret manager>
  sslmode: verify-full
  target_session_attrs: read-write
  type: unmanaged
type: Opaque
---
apiVersion: awx.ansible.com/v1beta1
kind: AWX
metadata: {name: awx, namespace: awx}
spec:
  postgres_configuration_secret: awx-postgres-configuration
```
- The default PostgreSQL for the AWX bundled with the latest operator is PostgreSQL 15 (see `supported_pg_version` in the operator repo). Only that default is covered by the project's testing; newer versions will likely work but only as an external database. Do not override the version of an operator-managed database.
- The password must not contain single or double quotes or backslashes (they break deployment, backup and restore).
- `sslmode` applies to external databases only; allowed values: `prefer`, `disable`, `allow`, `require`, `verify-ca`, `verify-full`.
- `target_session_attrs` is only useful for clustered external databases; values `any` (default), `read-write`, `read-only`, `primary`, `standby`, `prefer-standby`. Only `read-write` and `primary` make sense for AWX, which needs a writable node.
- Setting a username, password, port or database but keeping the operator-managed database: add `type: managed` to the secret.
- Managed-database spec fields in the docs: `postgres_image`, `postgres_image_version`, `postgres_resource_requirements`, `postgres_storage_requirements`, `postgres_storage_class`, `postgres_priority_class`, `postgres_extra_settings` (a list of `setting`/`value`; replaces the deprecated `postgres_extra_args`; a pod restart is needed). `postgres_data_path` can no longer be configured.

## extra_settings
Controller settings appended to `/etc/tower/settings.py`:
```yaml
spec:
  extra_settings:
    - setting: MAX_PAGE_SIZE
      value: "500"
    - setting: LOG_AGGREGATOR_LEVEL
      value: "'DEBUG'"
```
- Some values, such as `LOG_AGGREGATOR_LEVEL`, need inner quotes.
- Settings set this way become read-only in AWX and cannot be changed in the UI. Change them on the AWX CR spec.

## extra_settings_files
Python settings files (`*.py`) from ConfigMaps or Secrets, mounted under `/etc/tower/conf.d`:
```yaml
spec:
  extra_settings_files:
    configmaps:
      - {name: my-custom-settings, key: custom_job_settings.py}
    secrets:
      - {name: my-custom-passwords, key: custom_passwords.py}
```
- Create them with `kubectl create configmap ... --from-file` / `kubectl create secret generic ... --from-file`. A file can set structured values such as `AWX_TASK_ENV` (proxy variables).
- Keys must be python file names ending `.py`, use only alphanumerics, `-`, `_` or `.`, and the derived name (`<instance name>-<KEY>-configmap` or `-secret`) must be at most 63 characters. `credentials.py`, `execution_environments.py` and `ldap.py` are reserved.
- If a setting appears in both `extra_settings` and `extra_settings_files`, the files win. Do not repeat a key across several files: load order is arbitrary.
- After updating a ConfigMap or Secret, restart the AWX pods to apply it.

## Gotchas
- Back up the secret key secret together with the database; check the operator docs for its spec name in your version.

## Verify
- [ ] The AWX custom resource reports success and the API ping endpoint answers.

## Checked
2026-10-28. Confirmed in the AWX Operator docs (database-configuration and extra-settings pages): the unmanaged secret fields, `sslmode` and `target_session_attrs` values, password character restriction, `type: managed`, default PostgreSQL 15, managed-database variables, `postgres_extra_settings` deprecating `postgres_extra_args`, `extra_settings` appended to `/etc/tower/settings.py`, read-only behaviour, `extra_settings_files` mount path, key restrictions and precedence. Removed because not confirmed: sample RDS host name, `bundle_cacert_secret`/`postgres_ssl_*`, the hostname/ingress/replica/resource/ee spec list, `admin_password_secret` and `secret_key_secret` details, `TOWER_URL_BASE`, the claim that changing `extra_settings` restarts pods, `awx-manage check_db`, and settings endpoints.
Method: documentation only; no commands were run.
