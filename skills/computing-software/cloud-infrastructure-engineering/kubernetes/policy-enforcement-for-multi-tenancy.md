---
id: computing-software.cloud-infrastructure-engineering.kubernetes.policy-enforcement-for-multi-tenancy
name: policy-enforcement-for-multi-tenancy
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kyverno, gatekeeper, opa, policy-as-code, pod-security-admission, admission-controller, multi-tenancy, validatingadmissionpolicy, guardrails, mutation-policy, audit-mode]
level: advanced
status: docs-checked
description: "Enforce tenant guardrails at admission with Kyverno or Gatekeeper and Pod Security Admission so soft multi-tenancy holds under scale."
sources: ["https://kyverno.io/docs/policy-types/overview/", "https://kyverno.io/docs/policy-types/cluster-policy/generate/", "https://open-policy-agent.github.io/gatekeeper/website/docs/violations", "https://kubernetes.io/docs/concepts/security/pod-security-admission/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Admission policy for multi-tenancy — making the guardrails self-enforcing

**Goal:** stop relying on code review to catch "this Deployment forgot its
ResourceQuota-safe limits" or "this namespace has no NetworkPolicy" — enforce it at the
API server so a non-compliant object is rejected (or auto-fixed) before it's ever
scheduled. Builds directly on `computing-software.cloud-infrastructure-engineering.kubernetes.namespace-soft-multi-tenancy`,
whose controls this makes mandatory rather than advisory.

## 1. Kyverno vs Gatekeeper
- **Kyverno** policies are plain Kubernetes YAML (no new language) — easier for
  platform teams without Rego experience; supports validate, mutate and
  generate in one engine. The `ClusterPolicy` form is deprecated as of Kyverno v1.19 and removed in
  v1.20 (estimated Nov 2026); new policies should use the CEL-based `ValidatingPolicy`,
  `MutatingPolicy` and `GeneratingPolicy` (`policies.kyverno.io/v1`, stable since v1.18). The example
  below is the legacy form. `generate` is particularly useful for multi-tenancy:
  auto-create a default-deny NetworkPolicy, ResourceQuota, and LimitRange whenever a
  new tenant namespace is created, so tenants can't forget them.
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata: {name: require-tenant-label}
spec:
  validationFailureAction: Enforce
  rules:
  - name: require-tenant-label
    match: {resources: {kinds: [Namespace]}}
    validate:
      message: "namespaces must carry a tenant label"
      pattern: {metadata: {labels: {tenant: "?*"}}}
```
- **OPA Gatekeeper** uses Rego (via `ConstraintTemplate` + `Constraint` CRDs) — more
  expressive for complex cross-field logic, steeper learning curve, and a separate
  language to maintain/debug.
- **ValidatingAdmissionPolicy** (in-tree, CEL, no webhook) now covers many simple cases
  either tool used to be needed for — prefer it for straightforward rules to cut
  webhook latency and an extra moving part; reach for Kyverno/Gatekeeper when you need
  `generate`-style side effects or a policy library/ecosystem.

## 2. Multi-tenancy-specific policies worth having
- Require every namespace to declare a `tenant` label (used by cost reporting and by
  NetworkPolicy/RBAC generation).
- Require ResourceQuota and a default-deny NetworkPolicy to exist in any namespace
  labeled as a tenant namespace — enforce it by generating them automatically (Kyverno
  `generate`) rather than only validating their presence, which closes the "forgot to
  create one" gap entirely.
- Forbid `hostPath`, `hostNetwork`, `hostPID`, and privileged containers outside an
  explicitly allow-listed `platform` namespace set.
- Forbid cross-tenant `Service` type `ExternalName` or wildcard `NetworkPolicy` egress
  that would bypass the isolation namespace-soft-multi-tenancy relies on.
- Image provenance: require images come from an approved registry/digest-pinned
  source — relevant once multiple tenants can push their own workloads.

## 3. Rollout discipline
- Ship every new policy in **audit mode** first (Kyverno `validationFailureAction:
  Audit`, Gatekeeper `enforcementAction: dryrun`, ValidatingAdmissionPolicyBinding
  `validationActions: [Audit]` or `[Warn]`) and watch violations for a real
  traffic/deploy cycle before switching to `Enforce`/`deny` — flipping straight to
  enforce is the single most common cause of a policy rollout outage.
- Scope new policies to a pilot namespace or tenant group first via `match`/
  `namespaceSelector` exclusions, widen gradually.

## Gotchas
- Admission webhooks (for example Kyverno `validate`/`mutate` rules) with `failurePolicy: Fail` block
  **all** matching creates if the policy engine pod is down — always run the engine
  highly available and exclude `kube-system` from policy evaluation.
- `generate` rules rules: with `synchronize: true` Kyverno keeps generated resources in sync with the policy and
  reverts manual edits; `generateExisting: true` (default `false`) also generates for trigger
  resources that already exist when the policy is created or updated.
- Rego in Gatekeeper constraint templates is easy to write a subtly wrong rule in
  (e.g. an `if` that's vacuously true for missing fields) — unit-test constraints with
  `gator test` before shipping.
- Policy evaluation adds admission latency; a slow policy engine under load manifests
  as "pods are slow to schedule" far from the actual cause — monitor webhook latency,
  not just policy pass/fail counts.

## Verify
- [ ] A deliberately non-compliant object (privileged pod, missing tenant label, no
      quota) is rejected in a test namespace once a policy is in `Enforce` mode.
- [ ] Every new policy went through an audit-mode period with its violation count
      reviewed before enforcement, with that period's findings on record.
- [ ] `generate` policies produce the expected ResourceQuota/NetworkPolicy
      automatically on a fresh tenant namespace with no manual step.
- [ ] Policy-engine pods are HA and `kube-system`/platform namespaces are excluded from
      tenant-facing rules so a platform outage can't be self-inflicted by policy.

## Checked

Checked 2026-10-27 against Kyverno docs source (kyverno/website, main; policy types overview and sigstore pages describe Kyverno v1.19), the Gatekeeper docs source and the Kubernetes docs.

- Kyverno generate semantics (`synchronize`, `generateExisting` default false), ClusterPolicy deprecation and the CEL-based policy types confirmed in the Kyverno docs.
- Gatekeeper `enforcementAction` (`deny`, `dryrun`, `warn`), per-constraint `excludedNamespaces`, and `gator test` confirmed; ValidatingAdmissionPolicy `validationActions` and webhook `failurePolicy` default Fail confirmed in the Kubernetes docs.
- Removed the unconfirmed claim that Kyverno `generate` rules are mutating webhooks.

Method: documentation only; no commands were run.
