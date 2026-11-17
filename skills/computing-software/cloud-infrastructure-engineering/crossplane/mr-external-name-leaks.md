---
id: computing-software.cloud-infrastructure-engineering.crossplane.mr-external-name-leaks
name: mr-external-name-leaks
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [managed-resource, external-name, leaked-resource, annotations, recovery]
level: advanced
status: docs-checked
description: "Name external resources with crossplane.io/external-name and recover from a possible leaked resource."
sources:
  - https://docs.crossplane.io/latest/managed-resources/managed-resources/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default the external resource gets the managed resource's name. Set the annotation at creation to override:

```yaml
metadata:
  name: my-rds-instance
  annotations:
    crossplane.io/external-name: my-custom-name
```

`kubectl get` shows it in EXTERNAL-NAME.

Providers write three creation annotations to detect leaked resources (created but never recorded, a risk when the cloud generates names): `crossplane.io/external-create-pending`, `external-create-succeeded` and `external-create-failed`. If the latest pending time is newer than the latest succeeded or failed time, the provider may have leaked a resource and stops reconciling, emitting a `cannot determine creation result` event.

To recover:

1. Run `kubectl describe` on the MR to see the event.
2. Use the pending timestamp to find resources created around that time in the external system.
3. Delete any leaked resource, if it is safe.
4. Remove the `crossplane.io/external-create-pending` annotation. The provider resumes and recreates the resource.

Providers never remove these annotations; multiple being present is normal.

## Checked

2026-11-03. Confirmed against the Crossplane docs (Managed Resources page, docs.crossplane.io/latest): the field names, values, defaults and behaviours stated above. Removed or reworded: the closing paragraph about setting the external name before creation.

Method: documentation only; no commands were run.
