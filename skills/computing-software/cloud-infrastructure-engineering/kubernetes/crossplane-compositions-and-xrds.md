---
id: computing-software.cloud-infrastructure-engineering.kubernetes.crossplane-compositions-and-xrds
name: crossplane-compositions-and-xrds
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [crossplane, xrd, compositeresourcedefinition, composition, xr, composite-resource, infra-as-api, crossplane-v2, platform-api, crd-generation, control-plane]
level: sme
status: docs-checked
description: "Designing CompositeResourceDefinitions (XRDs) and Compositions so Crossplane turns infrastructure into a Kubernetes-native self-service API."
sources: ["https://docs.crossplane.io/latest/composition/composite-resource-definitions/", "https://docs.crossplane.io/latest/composition/compositions/", "https://docs.crossplane.io/latest/guides/upgrade-to-crossplane-v2/", "https://docs.crossplane.io/latest/packages/functions/", "https://docs.crossplane.io/latest/packages/providers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Crossplane Compositions and XRDs — infrastructure as a platform API

**Goal:** turn "provision a Postgres database" or "provision an app namespace
with quota and network policy" into a Kubernetes custom resource an app team
can `kubectl apply` or request through Backstage, without exposing Terraform,
cloud consoles, or raw provider CRDs. This is the mechanism underneath
"platform API" / "infra as API." Claims and functions (the newer composition
style) are in
`computing-software.cloud-infrastructure-engineering.kubernetes.crossplane-claims-functions-and-provider-design`.

## 1. XRD defines the API shape, Composition fills it in
A `CompositeResourceDefinition` (XRD) declares a new Kubernetes API
(`spec.group`, `spec.names.kind`, an OpenAPI `spec.versions[].schema` for the
fields a user sets) — this is pure API design, same discipline as any CRD.
Applying an XRD makes Crossplane generate the actual CRD for the Composite
Resource (XR). In Crossplane v2 the XRD is `apiextensions.crossplane.io/v2` and `spec.scope` defaults to
`Namespaced` (XRs live in a namespace and compose resources in that namespace); `Cluster` is cluster-scoped and
`LegacyCluster` is the v1-compatible cluster-scoped mode that supports claims. If `spec.claimNames` is set
(a v1-style XRD), a second namespaced CRD (the **Claim**) is generated for app teams. A `Composition` then matches XRs by
`compositionRef`/`compositionSelector` and defines what underlying managed
resources (a `RDSInstance`, a `Bucket`, a set of raw k8s objects) get created
to satisfy a given XR.

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: xpostgresinstances.platform.example.org
spec:
  scope: LegacyCluster   # v1-style XRDs default to this; claimNames needs it
  group: platform.example.org
  names: {kind: XPostgresInstance, plural: xpostgresinstances}
  claimNames: {kind: PostgresInstance, plural: postgresinstances}
  versions:
    - name: v1alpha1
      served: true
      referenceable: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties: {storageGB: {type: integer}, tier: {type: string, enum: [dev, prod]}}
```

## 2. Composition — mapping the API to real resources
A `Composition` uses `spec.mode: Pipeline` with a `spec.pipeline[]` of Composition Functions, each
referenced by `functionRef.name`, that receive the XR and emit desired composed resources. The native
patch-and-transform mode (`spec.mode: Resources`) was deprecated in v1.17 and removed in Crossplane v2;
`crossplane beta convert pipeline-composition` (v1.20 CLI) converts old compositions. Functions let you write
real Go or Python logic instead of fragile patch YAML. `function-patch-and-transform` lets you keep writing
patch and transform YAML inside the pipeline model if a full custom function is overkill.

## 3. The abstraction-design discipline
The XRD's schema IS the platform contract — every field you expose is a
promise to support it forever, and every field you omit is something the
platform team controls instead of the user. Expose `storageGB` and `tier`;
do NOT expose `instanceClass` or `engineVersion` directly unless multi-tenancy
requires it — translate `tier: prod` into the concrete instance class inside
the Composition so the platform team can change the mapping (cheaper
instance type, new engine version) without every consumer's manifest
changing. This is the actual skill: deciding what's a user-facing *intent*
field versus an internal *implementation* field.

## 4. Operational gotchas
- **Composition updates**: the XRD's `defaultCompositionUpdatePolicy` defaults to `Automatic`; set it to
  `Manual` to pin XRs to a Composition revision and roll changes out deliberately. `enforcedCompositionRef`
  and `defaultCompositionRef` set which Composition XRs use.
- **Schema evolution**: only one XRD version can be `referenceable: true`; changing it means updating
  `compositeTypeRef.apiVersion` in Compositions. Versions can't change existing fields, and new required fields
  count as breaking; breaking changes need conversion webhooks. New optional fields are fine.
- **Scope**: Crossplane v2 defaults new XRDs to `Namespaced` scope; existing v1 XRs keep working as
  `LegacyCluster`, and there is no automated migration tooling from cluster-scoped XRs to namespaced XRs yet.

## Verify
- `kubectl apply` of a Claim produces a bound XR and, within the expected
  provisioning time, a `Ready: True` condition on both the XR and the Claim.
- Changing a user-facing intent field (e.g. `tier: dev` → `tier: prod`)
  re-converges the composed resources to the new mapping without the user
  needing to know what changed underneath.
- Deleting the Claim deletes the composed resources; confirm in a test environment, including in the cloud
  provider console, before trusting this on anything with real spend attached.

## Checked

Checked against `crossplane/docs` (last commit 2026-10-25), version v2.4 pages: composition/composite-resource-definitions, composition/compositions, guides/upgrade-to-crossplane-v2.
Confirmed: XRD `v2` API with `scope` values `Namespaced` (default), `Cluster`, `LegacyCluster`; `claimNames` for legacy XRDs; `referenceable`; `defaultCompositionUpdatePolicy` default `Automatic`; `enforcedCompositionRef`; `mode: Pipeline`; removal of `mode: Resources` in v2 (deprecated v1.17); conversion webhooks for breaking schema changes.
Removed as unconfirmed: the management-policies and deletion-ordering behaviours.

Method: documentation only; no commands were run.
