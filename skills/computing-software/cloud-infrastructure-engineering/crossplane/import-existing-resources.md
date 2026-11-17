---
id: computing-software.cloud-infrastructure-engineering.crossplane.import-existing-resources
name: import-existing-resources
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [import, observe, external-name, managementpolicies, adopt]
level: practitioner
status: docs-checked
description: "Import existing cloud resources as managed resources, starting observe-only then taking control."
sources:
  - https://docs.crossplane.io/latest/guides/import-existing-resources/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Import with a managed resource using the `Observe` management policy (beta; the provider must support management policies).

```yaml
apiVersion: sql.gcp.upbound.io/v1beta1
kind: DatabaseInstance
metadata:
  name: my-imported-database
  annotations:
    crossplane.io/external-name: my-external-database
spec:
  managementPolicies: ["Observe"]
  forProvider:
    region: "us-central1"
```

Steps:

1. Create a manifest of the right kind with `managementPolicies: ["Observe"]`.
2. Set `crossplane.io/external-name` to the resource's name in the provider.
3. Pick a Kubernetes object name.
4. If several external resources share the name, add a distinguishing `forProvider` field such as `region`.
5. Apply. Crossplane fills `status.atProvider` and `spec.forProvider` from the real resource; conditions become Ready and Synced.

Observe-only never changes or deletes the resource.

To take control, change `managementPolicies` after copying the needed values from `status.atProvider` into `spec.forProvider` so Crossplane does not overwrite the resource with empty or default settings. Use `["*"]` or a chosen subset.

After a successful import the docs' example shows `status.atProvider` populated and the conditions Ready (reason `Available`) and Synced (reason `ReconcileSuccess`) both True. The external name must match the name inside the provider.

## Checked

2026-11-08: read the whole Crossplane Import Existing Resources guide (raw source of docs.crossplane.io/latest/guides/import-existing-resources). Confirmed the beta status and provider-support caveat for `managementPolicies`, the `Observe` policy never changing or deleting the resource, the `crossplane.io/external-name` annotation, disambiguating with a `spec.forProvider` field, `status.atProvider` population, and switching to `["*"]` after copying values from `status.atProvider`. Replaced an unsourced "not found" troubleshooting sentence with what the example shows.
Method: documentation only; no commands were run.
