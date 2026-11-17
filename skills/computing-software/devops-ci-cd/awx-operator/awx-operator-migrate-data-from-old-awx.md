---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-migrate-data-from-old-awx
name: awx-operator-migrate-data-from-old-awx
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, migration, old-postgres-configuration, secret-key, pg-dump-suffix, old-awx]
level: advanced
status: docs-checked
description: "Migrate an older AWX into the operator by providing the old secret key and old database credentials as Secrets and referencing them in the AWX spec."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/migration/migration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator migrate data from old awx

Migration needs two Secrets in the target namespace, named after the AWX resource (`<resourcename>` must equal the AWX `metadata.name`).

Secret key (find it in the inventory file used before AWX 18):

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: <resourcename>-secret-key
stringData:
  secret_key: <old-secret-key>
type: Opaque
```

Old database credentials:

```yaml
metadata:
  name: <resourcename>-old-postgres-configuration
stringData:
  host: <external ip or url resolvable by the cluster>
  port: "5432"        # quotes required
  database: <db name>
  username: <user>
  password: <password>
```

Reference both in the AWX spec:

```yaml
spec:
  old_postgres_configuration_secret: <resourcename>-old-postgres-configuration
  secret_key_secret: <resourcename>-secret-key
```

If the database is an external server not managed by the deployment, use a secret without `-old-` and pass it as `postgres_configuration_secret`. Back up first. Data is streamed from the old postgres pod; if it has a custom label set `postgres_label_selector`. Customize the dump with `pg_dump_suffix`, e.g. `--exclude-table-data 'main_jobevent*' --exclude-table-data 'main_job'`. In a single file separate blocks with `---`, otherwise the setup will be inoperable.

## Checked

2026-11-09. Confirmed the secret key and old database Secrets, the quoted port rule, the spec fields, the external database variant, the label selector, pg_dump_suffix and the document separator warning against the AWX Operator migration page (read in full).

Method: docs-checked 2026-11-09 against the AWX Operator docs page docs/migration/migration.md
