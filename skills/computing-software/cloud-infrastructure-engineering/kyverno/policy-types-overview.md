---
id: computing-software.cloud-infrastructure-engineering.kyverno.policy-types-overview
name: policy-types-overview
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [policy-types, cel-policies, clusterpolicy-deprecation, namespaced-policies, policyexception, globalcontextentry]
level: intro
status: docs-checked
description: "Know Kyverno's CEL policy types, their namespaced variants, the supporting resources, and the ClusterPolicy deprecation timeline."
sources:
  - https://kyverno.io/docs/policy-types/overview/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CEL policy types, group `policies.kyverno.io/v1` (stable since v1.18 unless noted):
- ValidatingPolicy (v1.14): validate resources or JSON payloads.
- MutatingPolicy (v1.15): mutate new or existing resources.
- GeneratingPolicy (v1.15): create or clone resources from flexible triggers.
- DeletingPolicy (v1.15): delete matching resources on a schedule.
- ImageValidatingPolicy (v1.14): verify image signatures and attestations.

Each has a namespaced variant (NamespacedValidatingPolicy and so on) that applies only in its own namespace.

Legacy `kyverno.io`: ClusterPolicy (`v1`, validate/mutate/generate/verifyImages rules) and CleanupPolicy (`v2`). Timeline: marked for deprecation v1.17 (Feb 2026), critical fixes only v1.18, deprecated v1.19 (Aug 2026), removed v1.20 (estimated Nov 2026).

Supporting resources: PolicyException (`policies.kyverno.io/v1`, stable v1.19), GlobalContextEntry (`kyverno.io/v2`), UpdateRequest (internal), PolicyReport/ClusterPolicyReport (`wgpolicyk8s.io/v1alpha2`), EphemeralReport (internal).

Deprecated versions: `policies.kyverno.io/v1alpha1` use `v1`; GlobalContextEntry `v2alpha1` use `v2`; UpdateRequest `v1beta1` use `v2`. Storage for `policies.kyverno.io` is `v1beta1` in v1.19, `v1` in v1.20; use `kyverno migrate`.

Detecting legacy use in v1.19: creating a legacy policy returns an admission warning; metric `kyverno_deprecated_api_requests_total`; CLI kind warnings and `--warnings-as-errors` for CI. CEL types have full feature parity with the legacy ones.

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
