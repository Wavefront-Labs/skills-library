---
id: computing-software.database-administration.cloudnative-pg.environment-variables-and-service-account-token
name: environment-variables-and-service-account-token
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [environment-variables, env, envfrom, tz, rolling-update, automountserviceaccounttoken]
level: practitioner
status: docs-checked
description: "Set env and envFrom on CloudNativePG pods (TZ, LDAPCONF), avoid reserved names, expect a rolling update on change, and control the ServiceAccount token automount."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/cluster_conf.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use `env` and `envFrom` in the cluster spec to customise container behaviour, for example `TZ` for the PostgreSQL container time zone or `LDAPCONF` for a custom LDAP configuration file.

```yaml
spec:
  instances: 3
  env:
  - name: TZ
    value: Australia/Sydney
  storage:
    size: 1Gi
```

```yaml
spec:
  envFrom:
  - configMapRef:
      name: config-map-name
  - secretRef:
      name: secret-name
```

Reserved names are rejected at admission: anything starting with `PG` or `CNPG_`, plus `POD_NAME`, `NAMESPACE` and `CLUSTER_NAME`.

Rollout behaviour matters: any change to `env` or `envFrom` triggers a rolling update of the PostgreSQL pods. But if they reference a Secret or ConfigMap, the operator does not watch the referenced object's contents, so editing it does not roll pods; like the kubelet, you must trigger the rollout manually.

`automountServiceAccountToken` in the cluster spec controls whether the ServiceAccount token is auto-mounted in instance Pods and operator-run Jobs. Setting it to `false` helps satisfy admission policies in hardened environments; the operator then mounts an equivalent projected volume so the instance manager keeps working (see the security page).

## Checked

2026-11-08. Read in full: docs/src/cluster_conf.md. Reserved variable rules, env/envFrom examples, rollout behaviour and automountServiceAccountToken note confirmed on the Instance Pod configuration page.

Method: documentation only; no commands were run.
