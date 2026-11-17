---
id: computing-software.data-engineering.kestra.configuration-basics
name: configuration-basics
category: computing-software
field: data-engineering
product: kestra
tags: [configuration, environment-variables, datasource, storage, sdk-authentication, micronaut]
level: practitioner
status: docs-checked
description: "Configure Kestra: where config lives, minimal boot settings, YAML to environment variable naming, the storage credential underscore trap, and SDK authentication."
sources:
  - https://kestra.io/docs/configuration/configuration-basics
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Config is YAML from a mounted file, the `KESTRA_CONFIGURATION` variable, inline Docker Compose, or Helm values. Environment variables override files.

```yaml
datasources:
  postgres:
    url: jdbc:postgresql://postgres:5432/kestra
    driver-class-name: org.postgresql.Driver
    username: kestra
    password: k3str4
kestra:
  repository:
    type: postgres
  queue:
    type: postgres
  storage:
    type: local
  url: "http://localhost:8080/"
```

Decide the repository type, a compatible queue type, and the storage type.

Variable naming: replace dots and hyphens with underscores, split camelCase, uppercase, and prefix Kestra keys with `KESTRA_`, for example `KESTRA_STORAGE_TYPE=s3`, `DATASOURCES_POSTGRES_USERNAME=kestra`.

Trap: for multi-word storage keys such as `kestra.storage.s3.access-key`, use YAML or double underscores, otherwise Micronaut may parse a nested object and fail with `UnrecognizedPropertyException`.

```bash
KESTRA_STORAGE_S3_ACCESS__KEY=<aws-access-key-id>
KESTRA_STORAGE_S3_SECRET__KEY=<aws-secret-access-key>
```

SDK plugin credentials resolve: namespace default service account, tenant default, then `kestra.tasks.sdk.authentication`. In OSS they derive from `kestra.server.basic-auth`. Set both `username` and `password` or neither; one alone errors on first SDK use.

## Checked

2026-11-04. Confirmed against the Kestra configuration basics page: config sources, environment override, minimal boot settings, variable naming rules, the double-underscore storage key trap with UnrecognizedPropertyException, and SDK authentication resolution order and the username/password pairing rule. Nothing removed.

Method: documentation only; no commands were run.
