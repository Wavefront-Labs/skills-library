---
id: computing-software.database-administration.cloudnative-pg.alter-system-and-applying-config-changes
name: alter-system-and-applying-config-changes
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [alter-system, allow-alter-system, configuration-changes, reload, rolling-update, enablealtersystem]
level: practitioner
status: docs-checked
description: "Change PostgreSQL settings through the Cluster manifest, understand reload versus rolling restart, and why ALTER SYSTEM is disabled unless enableAlterSystem is set."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/postgresql_conf.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Edit the `postgresql` section of the `Cluster`. Instances reload the configuration immediately; if a changed parameter needs a restart, the operator performs a rolling update. Edit the manifest rather than the pods so every instance stays coherent.

New clusters disable `ALTER SYSTEM`. Set `.spec.postgresql.enableAlterSystem` to `true` to allow it:

```yaml
spec:
  postgresql:
    enableAlterSystem: true
```

Why it is off: `ALTER SYSTEM` acts only on the instance you are connected to and is **not replicated**, and changing options the operator controls can leave the cluster in an unpredictable or unrecoverable state.

Mechanics by version:

- PostgreSQL 17 and later: the field drives the `allow_alter_system` GUC (a feature CloudNativePG contributed upstream).
- Before 17: with the field false, `postgresql.auto.conf` is made read-only, so the command fails with `ERROR:  could not open file "postgresql.auto.conf": Permission denied`.

`allow_alter_system` itself is on the forbidden-parameter list, so you control it only through `enableAlterSystem`. If you enable it, remember that `ALTER SYSTEM` acts only on the connected instance and is not replicated.

## Checked

2026-11-04. Trimmed claims the page does not state. Change behaviour, enableAlterSystem semantics and pre-17 read-only postgresql.auto.conf error confirmed on the PostgreSQL Configuration page.

Method: documentation only; no commands were run.
