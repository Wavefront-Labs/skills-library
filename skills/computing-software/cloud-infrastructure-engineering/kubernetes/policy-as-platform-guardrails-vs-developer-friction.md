---
id: computing-software.cloud-infrastructure-engineering.kubernetes.policy-as-platform-guardrails-vs-developer-friction
name: policy-as-platform-guardrails-vs-developer-friction
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [policy-as-code, guardrails, admission-control, warn-vs-block, audit-mode, pod-security-standards, platform-engineering, developer-friction, paved-road, exception-process, cognitive-load]
level: sme
status: docs-checked
description: "Deciding when a platform guardrail should warn, audit, or hard-block, and how to run an exception process so policy doesn't just push teams around it."
sources: ["https://kubernetes.io/docs/concepts/security/pod-security-standards/", "https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/", "https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/", "https://open-policy-agent.github.io/gatekeeper/website/docs/violations", "https://kyverno.io/docs/guides/exceptions/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Policy as platform guardrails — the warn/block tradeoff

**Goal:** decide, for each rule a platform wants to enforce, where it sits on
the warn → audit → block spectrum, and run an exception process so the rule
doesn't just get routed around. This is the judgment layer; the mechanics of
*implementing* the chosen enforcement mode are in
`computing-software.cloud-infrastructure-engineering.kubernetes.opa-gatekeeper-vs-kyverno-implementation-tradeoffs`.
Admission webhook internals are
`computing-software.cloud-infrastructure-engineering.kubernetes.admission-webhooks-validating-and-mutating`.
General IaC policy-as-code (Terraform/Sentinel-style, pre-apply) is
`computing-software.cloud-infrastructure-engineering.infrastructure-as-code.policy-as-code-with-opa-or-sentinel`
— that's gating *before* a change reaches the cluster; this skill is guardrails
*at* the cluster boundary, which catches drift, manual `kubectl apply`, and
anything that skipped the pipeline.

## 1. The enforcement ladder, and why skipping rungs backfires
Four real modes, not two:
1. **Report-only / dashboard** — the rule is evaluated and findings surface
   in a report (e.g. Kyverno PolicyReport, Gatekeeper's audit results) but
   nothing is blocked or even visibly warned at apply-time. Use for "we think
   this matters but have no idea how many violations exist yet."
2. **Warn** — `kubectl apply` succeeds but the apiserver returns a visible
   warning (webhook `AdmissionReview.response.warnings`, ValidatingAdmissionPolicyBinding
   `validationActions: [Warn]`, or Gatekeeper's `enforcementAction: warn`). The resource is created anyway.
   Use once you know the violation rate and want visibility without
   blocking anyone mid-sprint.
3. **Audit / dry-run block** — the webhook would reject, but
   `enforcementAction: dryrun` (or `validationActions: [Audit]` on a ValidatingAdmissionPolicyBinding)
   records what *would* have been blocked without actually blocking. The critical step everyone is tempted to skip: run
   audit mode against real traffic for at least one full deploy cycle
   (longer for infrequently-deployed services) before flipping to block, or
   the first thing block-mode does is break someone's quarterly batch job
   nobody remembered.
4. **Block** — hard reject at admission. Reserve for rules with a
   near-zero false-positive rate and a known, low current violation count
   (confirmed via step 3's data, not guessed).
Jumping straight to block on a new rule is the single most common way a
platform team burns trust — one unexpected blocked deploy during an incident
and "the policy engine" becomes the thing everyone routes around, not the
thing that keeps the cluster safe.

## 2. Guardrails need an exception process, not just an on/off switch
A rule with no escape hatch gets one anyway — someone finds the webhook's
`failurePolicy: Ignore` edge case, or disables the whole ValidatingWebhook
for their namespace "temporarily." Build the exception path into the policy
itself: a label/annotation-based exemption
(`policy.platform.io/exempt: CVE-2024-XXXX-pending-fix`) that the policy
engine checks and *logs loudly* when matched, reviewed on a cadence (e.g.
every exemption expires in 30 days and must be renewed with a reason) rather
than a silent permanent carve-out. Gatekeeper's `match.excludedNamespaces`
and Kyverno's `exclude` blocks or PolicyExceptions (off by default: enable with the
`enablePolicyException` flag and `exceptionNamespace`) are the mechanism — the governance (who can
grant an exemption, how long it lasts, who reviews the list) is the actual
platform-team skill, not the YAML.

## 3. Picking rules — risk-weighted, not exhaustive
A platform team that writes 80 policies in month one, all in block mode,
produces an unusable cluster. Start from real incidents or compliance
requirements (Pod Security Standards' `restricted` profile is a good
default floor, not a from-scratch rule set), pick the handful of
highest-risk, lowest-false-positive rules first (no privileged containers,
no `hostNetwork`, required resource requests/limits, required labels for
cost attribution), prove each through the ladder in §1, and only add the
next rule once the current set is stable and trusted. Measuring adoption
and whether guardrails are actually reducing incidents (not just producing
audit noise) overlaps with
`computing-software.cloud-infrastructure-engineering.kubernetes.measuring-platform-adoption-and-developer-experience`.

## 4. Gotchas
- `failurePolicy: Fail` on a validating webhook that becomes unreachable
  (crashed pod, bad rollout) blocks **all** matching admissions
  cluster-wide, not just new violations — pair any block-mode policy
  webhook with HA (multiple replicas, PDB) and a documented
  `failurePolicy: Ignore` fallback for genuine outages, decided in advance,
  not improvised during an incident.
- Audit-mode findings reported against resources created *before* the
  policy existed will flood the report with historical violations
  unrelated to new activity — filter by creation/update timestamp when
  deciding if a rule is "ready" for block mode, or old debt looks like a
  current failure rate.
- A policy that blocks on namespace creation but not on later namespace
  edits (or vice versa) creates a gap teams find by accident — audit
  whether a rule covers CREATE, UPDATE, and DELETE consistently, not just
  the operation it was first written for.

## Verify
- Every currently-blocking rule has a dated record of having run in audit
  mode first, with a measured violation rate before enforcement flipped.
- At least one active exemption exists with a reason, an expiry, and a
  named owner — if none exist, either no one has ever needed one (unlikely
  past a few dozen services) or the exception process isn't actually
  discoverable, which is worth checking directly with a few app teams.
- Disabling the policy webhook (in a test cluster) and checking
  `failurePolicy` behavior confirms the platform's chosen fail-open/fail-
  closed stance is the one actually configured, not the engine's default.

## Checked

Checked 2026-10-27 against Kyverno docs source (kyverno/website, main; policy types overview and sigstore pages describe Kyverno v1.19), the Gatekeeper docs source and the Kyverno docs source.

- Webhook responses can carry warnings returned as HTTP `Warning` headers; webhook `failurePolicy` defaults to Fail; ValidatingAdmissionPolicy `validationActions` (Deny, Warn, Audit): confirmed in the Kubernetes docs (the "1.19+" version claim was dropped as unconfirmed).
- Gatekeeper `enforcementAction` values `deny`, `dryrun`, `warn` and `excludedNamespaces`: confirmed. Kyverno PolicyException being disabled by default: confirmed.
- Pod Security `restricted` profile as a baseline floor: confirmed in the Pod Security Standards page.
- Removed the uncited CNCF whitepaper entry from `sources`.

Method: documentation only; no commands were run.
