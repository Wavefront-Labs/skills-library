---
id: computing-software.cloud-infrastructure-engineering.kubernetes.crossplane-claims-functions-and-provider-design
name: crossplane-claims-functions-and-provider-design
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [crossplane, claim, composition-function, function-pipeline, provider-aws, provider-gcp, provider-azure, upbound, crossplane-provider, go-templating, kcl, rbac-multi-tenancy, self-service-infra, providerconfig]
level: sme
status: docs-checked
description: "Choosing claim vs. direct-XR access for app teams, writing Composition Functions, and scoping Crossplane provider credentials per environment."
sources: ["https://docs.crossplane.io/latest/composition/composite-resource-definitions/", "https://docs.crossplane.io/latest/composition/compositions/", "https://docs.crossplane.io/latest/guides/upgrade-to-crossplane-v2/", "https://docs.crossplane.io/latest/packages/functions/", "https://docs.crossplane.io/latest/packages/providers/", "https://docs.crossplane.io/latest/guides/write-a-composition-function-in-python/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Crossplane claims, functions, and provider design

**Goal:** decide who gets to request infrastructure and how, write Composition
Functions that encode real platform logic instead of brittle YAML patching,
and scope cloud provider credentials so a namespace-level self-service request
can't accidentally touch another team's cloud account. XRD/Composition
mechanics are in
`computing-software.cloud-infrastructure-engineering.kubernetes.crossplane-compositions-and-xrds`.

## 1. Claim vs. direct XR — who faces the app team
A **Claim** is a namespaced proxy for a Composite Resource (XR); giving app
teams RBAC only on Claims (never on XRs or managed resources directly) is the
standard multi-tenancy boundary — a team can request a `PostgresInstance` in
their own namespace, see its status, and delete it, but can't see or touch
another team's claim, and can't see the underlying `RDSInstance` or cloud
credentials at all. Reserve direct XR access for the platform team's own
tooling (e.g. a controller that needs cluster-scoped visibility across all
claims for cost reporting). If a consumer needs no namespace isolation at all,
Crossplane v2's namespaced XRs (the default `Namespaced` XRD scope) let you skip the claim indirection:
the XR lives in a team namespace and can only compose resources in that namespace. Claims remain
available for v1-style `LegacyCluster` XRDs with `claimNames`.

## 2. Composition Functions — real logic, not patch soup
A function is a package (installed with a `Function` object in `pkg.crossplane.io/v1`; its pod runs in
the `crossplane-system` namespace by default) called in `spec.pipeline[]` order; each receives the XR and
the state so far and returns desired composed resources and an updated `status`. Three
practical authoring paths:
- **`function-patch-and-transform`**: declarative YAML patches, fine for simple
  field mapping, same mental model as classic compositions.
- **`function-go-templating`**: Go template strings rendering resource YAML —
  good middle ground, no new language, but logic-in-strings gets unreadable
  past a few conditionals.
- **A custom function (Go, Python via the `function-sdk-python` SDK, or KCL via
  `function-kcl`)**: full language for branching and validation. The Python guide covers unit tests and
  `crossplane composition render` for testing a function locally; pin the function package version in the
  `Function` object.

## 3. Scoping provider credentials — the actual security boundary
A Crossplane `Provider` (e.g. `provider-aws`) is usually authenticated with a `ProviderConfig` whose
`spec.credentials` reference a `Secret` (other credential sources, such as workload identity, are covered in
the provider and workload-identity guides). One ProviderConfig with org-wide admin credentials used by every
Composition means a bug in one pipeline can touch anything in the cloud account. Prefer separate
per-environment or per-team ProviderConfigs whose cloud permissions are limited to what that environment may
touch, and set the right `providerConfigRef` on the composed managed resources (for example from a field on
the XR). Treat it like any CI/CD credential scoping exercise.

## 4. Gotchas
- Crossplane itself needs RBAC to create the resources a Composition composes; the RBAC manager
  (enabled by default) grants access to MRs and XRs, and other resource kinds need a ClusterRole labelled
  `rbac.crossplane.io/aggregate-to-crossplane: "true"`.
- Upgrade providers and Crossplane deliberately: v2 removed native patch-and-transform compositions,
  `ControllerConfig` (use `DeploymentRuntimeConfig`) and the `--registry` default flag, so run
  `crossplane beta upgrade check` with the v1.20 CLI first and test upgrades on a non-production control plane.

## Verify
- An app-team RBAC role that can `create`/`get`/`delete` Claims in its own
  namespace cannot `get` the corresponding XR or any managed resource
  (`kubectl auth can-i get xpostgresinstances.platform.example.org --as=system:serviceaccount:team-ns:default`
  returns `no`).
- Two claims in different environments (`dev`, `prod`) resolve to visibly
  different ProviderConfigs, confirmed by checking which cloud account/role
  each composed resource actually lands in.
- A deliberately broken custom function fails the XR reconcile visibly (check the XR conditions and events).

## Checked

Checked against `crossplane/docs` (last commit 2026-10-25), version v2.4 pages: composition/composite-resource-definitions, composition/compositions, packages/functions, packages/providers, guides/upgrade-to-crossplane-v2, guides/write-a-composition-function-in-python.
Confirmed: `Namespaced`/`LegacyCluster` scopes and claims for legacy XRDs; `Function` package kind and default namespace; function-go-templating, function-kcl and function-python are listed functions; Python SDK and `crossplane composition render`; ProviderConfig with Secret credentials; RBAC manager and the aggregate-to-crossplane label; removed v2 features and `crossplane beta upgrade check`.
Removed as wrong or unconfirmed: `crossplane-rbac` and `function-runtime-deno`/`-shell` as function runtimes, the `Fatal` result wording, the provider-aws family-split behaviour, the per-function ServiceAccount claim.

Method: documentation only; no commands were run.
