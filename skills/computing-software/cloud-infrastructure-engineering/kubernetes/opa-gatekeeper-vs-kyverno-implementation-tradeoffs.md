---
id: computing-software.cloud-infrastructure-engineering.kubernetes.opa-gatekeeper-vs-kyverno-implementation-tradeoffs
name: opa-gatekeeper-vs-kyverno-implementation-tradeoffs
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [opa, gatekeeper, kyverno, rego, constrainttemplate, policyreport, mutate-policy, generate-policy, admission-controller, policy-engine-comparison, cel-validatingadmissionpolicy]
level: advanced
status: docs-checked
description: "Choosing and implementing OPA/Gatekeeper, Kyverno, or built-in CEL ValidatingAdmissionPolicy for cluster guardrails, with the real authoring and ops tradeoffs between them."
sources: ["https://open-policy-agent.github.io/gatekeeper/website/docs/", "https://kyverno.io/docs/policy-types/overview/", "https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/", "https://kubernetes.io/docs/reference/access-authn-authz/mutating-admission-policy/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OPA/Gatekeeper vs. Kyverno vs. CEL ValidatingAdmissionPolicy

**Goal:** pick the right engine for a given guardrail and write it well. The
judgment about *when* to warn vs. block is
`computing-software.cloud-infrastructure-engineering.kubernetes.policy-as-platform-guardrails-vs-developer-friction`;
this skill is the three real implementation choices once a rule is decided.

## 1. Three engines, genuinely different authoring models
- **OPA/Gatekeeper**: policies written in **Rego**, packaged as a
  `ConstraintTemplate` (defines the Rego + a CRD schema for parameters) and
  instantiated as a `Constraint` CR per use. Rego is a real logic-programming
  language — powerful for genuinely complex cross-field or cross-resource
  rules, but it's a second language most app-platform engineers don't know,
  and debugging a wrong Rego rule (why did this unexpectedly match/not
  match) is its own skill (`opa eval`/`gator test` locally before deploying).
- **Kyverno**: policies are Kubernetes resources. The legacy `ClusterPolicy` (`kyverno.io/v1`, YAML with
  `validate`/`mutate`/`generate`/`verifyImages` rules) is deprecated as of Kyverno v1.19 and removed in
  v1.20 (estimated Nov 2026); its replacements are the CEL-based `ValidatingPolicy`, `MutatingPolicy`,
  `GeneratingPolicy`, `ImageValidatingPolicy` and `DeletingPolicy` (`policies.kyverno.io/v1`, stable
  since v1.18). No Rego to learn, and it
  natively supports **mutate** (auto-inject defaults, e.g. add a
  `resources.limits` if missing) and **generate** (create a companion
  resource whenever a trigger resource is created — e.g. auto-create a
  default NetworkPolicy for every new namespace) in ways Gatekeeper doesn't
  do as directly.
- **ValidatingAdmissionPolicy (CEL)**: built into the apiserver (stable since
  v1.30), no separate webhook deployment, no extra network hop,
  evaluated in-process by the apiserver using CEL expressions. Faster and
  one fewer moving part to operate, but it only validates (mutation is the separate in-tree
  MutatingAdmissionPolicy, stable in v1.36; nothing in-tree generates resources), and CEL's
  expression surface can be more limited than Rego for deeply nested cross-resource logic. Prefer this for simple,
  high-traffic validation rules once the cluster's k8s version supports it;
  keep Gatekeeper/Kyverno for generate or complex logic.

## 2. Picking per rule, not picking one engine for everything
Running all three isn't absurd — many platform teams end up with CEL
`ValidatingAdmissionPolicy` for simple hot-path validations (fewer
moving parts, lowest latency) and Kyverno for anything needing mutate/
generate, dropping Gatekeeper entirely unless a specific compliance
framework's rule set already ships as Rego/`ConstraintTemplate` bundles
(several compliance vendors publish Gatekeeper libraries first). Running
genuinely all three in production is real added operational surface
(three sets of CRDs, three failure domains for `failurePolicy`) — justify
each one's presence, don't default to "more tools, more coverage."

## 3. Performance and HA, concretely
Both Gatekeeper and Kyverno run as webhook pods — budget for at least 2
replicas with a PodDisruptionBudget and realistic `resources.requests`
(constraint evaluation on a busy cluster is CPU-bound; under-provisioned
policy pods become the admission-latency bottleneck during deploy storms).
`timeoutSeconds` on the webhook configuration (allowed range 1 to 30
seconds; keep it low) interacts with `failurePolicy`: a slow policy pod under load
combined with `failurePolicy: Fail` turns a resource-contention problem into
a cluster-wide inability to schedule anything. CEL `ValidatingAdmissionPolicy`
avoids this whole class of failure since there's no separate pod/network hop
to time out.

## 4. Gotchas
- Gatekeeper's `audit` controller re-evaluates all constrained resources on
  a timer (default every 60s, configurable) — on a large cluster with many
  constraints this audit scan itself is a real CPU/API-load source; tune
  `--audit-interval` and `--constraint-violations-limit` before assuming
  audit mode is "free" compared to block mode.
- Kyverno `generate` policies create resources with a `synchronize: true`
  option that *re-applies* the generated resource if someone edits it
  manually — useful for drift-prevention, surprising if you expected a
  one-time generate and then manual edits allowed; check this flag
  deliberately.
- CEL expressions in ValidatingAdmissionPolicy fail closed on an expression
  error by default (`failurePolicy` on the `ValidatingAdmissionPolicy`, default `Fail`; the binding's
  `validationActions` of `Deny`, `Warn` and `Audit` give the rollout ladder),
  same cluster-wide-block risk as any other admission control — a CEL typo
  deployed straight to production with no staged rollout is exactly the
  mistake the warn/audit ladder in the guardrails-vs-friction skill exists
  to prevent, and applies identically here.

## Verify
- `gator test` (Gatekeeper) or `kyverno apply --resource` (Kyverno) against
  a suite of known-good and known-bad manifests reproduces the intended
  allow/deny decision for every test case before the policy reaches a real
  cluster.
- Simulated webhook-pod slowness (e.g. artificial delay in a test
  deployment) confirms the configured `timeoutSeconds`/`failurePolicy`
  combination behaves as intended (fails open or closed, matching the
  documented platform decision) rather than an assumed default.
- For any `generate`/mutate policy, confirm the generated/mutated resource
  survives a manual edit the way the `synchronize`/mutate-once setting
  claims it should.

## Checked

Checked 2026-10-27 against Kyverno docs source (kyverno/website, main; policy types overview and sigstore pages describe Kyverno v1.19), the Gatekeeper docs source (open-policy-agent/gatekeeper, `website/docs`) and the Kubernetes docs.

- ValidatingAdmissionPolicy stable since v1.30; `failurePolicy` lives on the policy (default Fail), `validationActions` Deny/Warn/Audit on the binding; MutatingAdmissionPolicy gate stable and on by default from v1.36 (alpha v1.30, beta v1.34): all confirmed in the docs and feature-gate pages.
- Webhook `timeoutSeconds` must be between 1 and 30 seconds, and the default webhook `failurePolicy` is Fail: confirmed.
- Gatekeeper audit interval default 60 seconds (`--audit-interval`), `--constraint-violations-limit` default 20, `enforcementAction` values `deny`, `dryrun`, `warn`, and `gator test`: confirmed.
- Kyverno policy types, v1.18 stable and v1.19 deprecation of ClusterPolicy (removal v1.20, estimated), `generate` `synchronize` and `generateExisting` (default false), and `kyverno apply --resource`: confirmed.
- Removed the stale "since 1.26" claim and the "validate-only, no mutate" framing.

Method: documentation only; no commands were run.
