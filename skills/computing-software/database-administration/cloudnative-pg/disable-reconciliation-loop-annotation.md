---
id: computing-software.database-administration.cloudnative-pg.disable-reconciliation-loop-annotation
name: disable-reconciliation-loop-annotation
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [reconciliation, annotation, emergency, manual-intervention, self-healing]
level: advanced
status: docs-checked
description: "Pause the operator on a Cluster or Backup with cnpg.io/reconciliationLoop disabled in emergencies, then remove it."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/failure_modes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The annotation `cnpg.io/reconciliationLoop` set to `"disabled"` makes the operator stop processing updates for the annotated resource: no automated changes and no self-healing. Use it with extreme caution and only in emergency operations.

Supported resources:

- **Cluster**: disables reconciliation of the PostgreSQL cluster.
- **Backup**: disables reconciliation of backup operations.

```yaml
metadata:
  name: cluster-example-no-reconcile
  annotations:
    cnpg.io/reconciliationLoop: "disabled"
spec:
  # ...
```

Warning from the docs: remove the annotation as soon as the issue is resolved. While it remains on a Cluster, the operator cannot perform self-healing actions **including failover**, so a primary crash during that window will not be handled.

The same page notes that manual operations in failure scenarios should be done with professional support, so treat this as a last resort rather than a maintenance tool.

## Checked

2026-11-08. Annotation name, value, supported resources and warning confirmed on the Failure Modes page, section Disabling Reconciliation.

Method: documentation only; no commands were run.
