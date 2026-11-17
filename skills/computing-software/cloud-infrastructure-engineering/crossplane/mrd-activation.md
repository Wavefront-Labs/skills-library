---
id: computing-software.cloud-infrastructure-engineering.crossplane.mrd-activation
name: mrd-activation
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [managedresourcedefinition, mrd, crd, activation, safe-start]
level: advanced
status: docs-checked
description: "Understand ManagedResourceDefinitions, which keep provider CRDs inactive until activated."
sources:
  - https://docs.crossplane.io/latest/managed-resources/managed-resource-definitions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Large providers install 100+ CRDs, each costing about 3 MiB of API server memory and slowing commands like `kubectl get managed`. A `ManagedResourceDefinition` (MRD) carries the same schema as a CRD plus two fields:

- `state`: `Active` or `Inactive` (the default). Inactive means no CRD, no API endpoint and no provider controller.
- `connectionDetails`: a list of `name` and `description` documenting the connection secret keys. It is schema-only; most providers do not populate it yet.

State changes are one-way: Inactive to Active, never back, so a CRD with existing resources cannot be removed by accident.

MRDs are enabled by default in Crossplane v2. Disable the conversion of provider CRDs to MRDs with `--enable-custom-to-managed-resource-conversion=false`.

Inspect:

```shell
kubectl get managedresourcedefinitions
kubectl describe mrd buckets.s3.aws.m.crossplane.io
```

An inactive MRD shows condition `Established: False` with reason `InactiveManagedResource`.

Activate MRDs with a ManagedResourceActivationPolicy (the recommended approach), or manually with `kubectl patch mrd <name> --type='merge' -p='{"spec":{"state":"Active"}}'`.

Crossplane v2 converts all provider CRDs to MRDs on package install. The provider's `safe-start` package capability sets the default: with it, MRDs start `Inactive`; without it, they start `Active` (legacy behaviour, all CRDs available). Check a provider with `kubectl get providerrevision <name> -o jsonpath='{.status.capabilities}'`.

An MRD with `state: Active` but `Established: False` means CRD creation failed; run `kubectl describe mrd <name>` for events.

## Checked

2026-11-08: read the whole Crossplane Managed Resource Definitions page (raw source of docs.crossplane.io/latest/managed-resources/managed-resource-definitions). Confirmed the 3 MiB per CRD figure, the `state` and `connectionDetails` fields, Inactive as default, one-way transition, the `--enable-custom-to-managed-resource-conversion=false` flag, the inspect commands, the `InactiveManagedResource` reason, the manual patch command, and `safe-start` setting the default state. Removed the claim that providers must declare `safe-start` to ship MRDs (the page says Crossplane converts every provider's CRDs) and the claim that activation needs no provider restart (not stated).
Method: documentation only; no commands were run.
