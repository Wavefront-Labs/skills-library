---
id: computing-software.database-administration.cloudnative-pg.pg-hba-podselectorrefs-dynamic-ips
name: pg-hba-podselectorrefs-dynamic-ips
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [pg-hba, podselectorrefs, label-selector, pod-ip, dynamic-access, reload]
level: advanced
status: docs-checked
description: "Use spec.podSelectorRefs and the podselector placeholder in pg_hba so client pod IPs are resolved into /32 rules automatically, with scope, validation and zero-match rules."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/postgresql_conf.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pod IPs change, so hand-maintained `pg_hba` CIDRs rot. Define named label selectors and reference them with `${podselector:NAME}`:

```yaml
podSelectorRefs:
  - name: app-pods
    selector:
      matchLabels:
        app: myapp
  - name: monitoring
    selector:
      matchLabels:
        role: monitoring
postgresql:
  pg_hba:
    - "hostssl mydb myuser ${podselector:app-pods} scram-sha-256"
    - "hostssl postgres monitor ${podselector:monitoring} scram-sha-256"
```

The operator resolves matching pod IPs and the instance manager expands each reference into one rule per IP (`/32` for IPv4, `/128` for IPv6), for example `hostssl mydb myuser 10.0.0.5/32 scram-sha-256`.

Constraints:

- Selectors only see pods in the **same namespace** as the Cluster.
- The placeholder is valid only in the address field of `host`, `hostssl`, `hostnossl`, `hostgssenc` and `hostnogssenc` entries.
- Pod create, delete and IP-change events regenerate the configuration and trigger a PostgreSQL reload.
- Selector names must match `^[a-z]([a-z0-9_-]*[a-z0-9])?$`, and every referenced name must be defined; the webhook enforces both.

Warning: when a selector matches zero pods its `pg_hba` lines are omitted entirely, so make sure the default rules give sensible fallback access. A complete sample is `cluster-example-pod-selector-refs.yaml`.

## Checked

2026-11-04. podSelectorRefs workflow, expansion example, constraints and zero-match warning confirmed on the PostgreSQL Configuration page.

Method: documentation only; no commands were run.
