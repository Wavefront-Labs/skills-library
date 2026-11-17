---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kyverno-policy-engine
name: kyverno-policy-engine
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kyverno, policy-as-code, validate, mutate, generate, clusterpolicy, policyexception, background-scan, cleanuppolicy, verifyimages, cosign, image-verification, admission-control, kyverno-cli]
level: advanced
status: docs-checked
description: "Kyverno's validate/mutate/generate rule model in plain YAML, image-signature verification, background audit scans, generate-sync hazards, and PolicyException scoping."
sources: ["https://kyverno.io/docs/policy-types/cluster-policy/overview/", "https://kyverno.io/docs/policy-types/cluster-policy/validate/", "https://kyverno.io/docs/policy-types/cluster-policy/generate/", "https://kyverno.io/docs/policy-types/cluster-policy/policy-settings/", "https://kyverno.io/docs/policy-types/cluster-policy/autogen/", "https://kyverno.io/docs/policy-types/cluster-policy/verify-images/sigstore/", "https://kyverno.io/docs/guides/exceptions/", "https://github.com/kyverno/policies"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kyverno — policy-as-YAML admission control

**Goal:** author Kyverno `ClusterPolicy`/`Policy` rules that validate, mutate, or
generate Kubernetes objects without Rego, know when `generate` rules drift from
their source instead of tracking it, and verify container images are signed
before they're admitted. OPA Gatekeeper, the Rego-based alternative, is in
`computing-software.cloud-infrastructure-engineering.kubernetes.opa-gatekeeper-policy-engine`;
signing mechanics themselves are in
`computing-software.cloud-infrastructure-engineering.kubernetes.container-image-signing-and-verification`.

**Deprecation:** the Kyverno docs state that `ClusterPolicy` and `Policy` (`kyverno.io/v1`) are deprecated as
of Kyverno v1.19 and will be removed in v1.20; the CEL-based policy types (for example `ValidatingPolicy`
and `ImageValidatingPolicy` in `policies.kyverno.io`) replace them, and the docs provide a migration guide.
This skill covers the legacy ClusterPolicy model for clusters that still run it.

## 1. The three rule types, one CRD
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata: {name: require-run-as-nonroot}
spec:
  background: true                  # default: also scan existing (already-admitted) resources
  rules:
  - name: check-runAsNonRoot
    match: {any: [{resources: {kinds: [Pod]}}]}
    validate:
      failureAction: Audit          # start here; Enforce blocks on failure
      message: "runAsNonRoot must be true"
      pattern: {spec: {securityContext: {runAsNonRoot: true}}}
```
- `validate` — declarative `pattern`/`anyPattern`, `deny` conditions, or (since Kyverno 1.11) a `cel`
  subrule, evaluated against the incoming object; blocks under `failureAction: Enforce`.
- `mutate` — `patchStrategicMerge` or JSON patches, applied before validation (same
  mutate-then-validate ordering as native webhooks).
- `generate` — creates a *new* downstream object (e.g. a default `NetworkPolicy`
  or `ResourceQuota`) whenever a trigger object (e.g. a new Namespace) appears.

## 2. `failureAction: Audit` vs `Enforce`
- The action is set per rule at `spec.rules[*].validate[*].failureAction`; the policy-level
  `spec.validationFailureAction` (and `validationFailureActionOverrides`) is deprecated in favour of it.
  `failureActionOverrides` under the rule varies the action by namespace.
- `Audit` (the dry-run equivalent) records `PolicyReport`/`ClusterPolicyReport`
  objects but admits the object anyway; set `spec.emitWarning: true` to also show violations as admission
  warnings. Run every new policy here first — same rollout discipline as Gatekeeper's `dryrun`.
- `background` (default `true`) additionally scans **already-existing** cluster objects and
  populates reports for resources that predate the policy — this is how you discover the blast radius
  before `Enforce`; `kubectl get policyreport -A` to review hits across namespaces.

## 3. `generate` rules — sync mode is the sharp edge
```yaml
  - name: default-deny-netpol
    match: {any: [{resources: {kinds: [Namespace]}}]}
    generate:
      apiVersion: networking.k8s.io/v1
      kind: NetworkPolicy
      name: default-deny
      namespace: "{{request.object.metadata.name}}"
      synchronize: true     # keep in lockstep with the policy; false = generate once
      data: {spec: {podSelector: {}, policyTypes: [Ingress, Egress]}}
```
- For a rule with a `data` source, `synchronize: true` means a modified downstream object is **reverted**,
  a deleted one is **recreated**, a modified policy is synced, and the downstream is **deleted** when the
  trigger is deleted. Deleting the rule or policy deletes the downstream unless
  `generate.orphanDownstreamOnPolicyDelete: true` is set (default `false`).
- With `synchronize: false` the downstream is generated once: manual edits stick, and deleting the
  downstream object really deletes it (it is not recreated).
- Generating other kinds may need extra permissions for the Kyverno background controller's
  ServiceAccount (see the docs on customizing permissions); a generate rule is effectively a standing write
  capability across every namespace it targets, so scope it tightly.
- Generate rules do not apply to existing trigger resources unless `generateExisting: true`.

## 4. Image verification
```yaml
  - name: verify-signature
    match: {any: [{resources: {kinds: [Pod]}}]}
    verifyImages:
    - imageReferences: ["registry.example.com/*"]
      attestors:
      - entries: [{keyless: {subject: "https://github.com/org/repo/.github/workflows/build.yml@refs/heads/main", issuer: "https://token.actions.githubusercontent.com"}}]
```
Verifies a Sigstore Cosign signature (keys, certificates or keyless) at admission; it can also
verify **attestations** and check their content, not just "is it signed." `imageReferences` lists the
image patterns to match, `skipImageReferences` excludes some, and `required` enforces that all matching
images are verified. Pin `imageReferences` narrowly: a broad pattern also matches images you do not
sign and blocks them.

## 5. `PolicyException` — scoped carve-outs without editing the policy
The current `PolicyException` is in `policies.kyverno.io` (introduced in Kyverno 1.14) and works with
the CEL policy types; the legacy `kyverno.io` PolicyException that pairs with ClusterPolicy is deprecated
as of v1.19 and removed in v1.20 (see the exceptions guide for its syntax).
```yaml
apiVersion: policies.kyverno.io/v1
kind: PolicyException
metadata: {name: exclude-skipped-deployment, namespace: default}
spec:
  policyRefs:
  - {name: require-prod-label, kind: ValidatingPolicy}
  matchConditions:
  - {name: skip-by-name, expression: "object.metadata.name == 'skipped-deployment'"}
```
PolicyExceptions are disabled by default: set the `enablePolicyException` flag to `true` and name the
namespaces they may be used in with the `exceptionNamespace` flag. A skipped rule is recorded in the
PolicyReport.

## Gotchas
- Background scans populate reports separately from admission events, so a resource created moments
  ago may not show in `PolicyReport` yet; don't treat an empty report as "clean" immediately after
  rollout.
- Autogen: a policy that matches `Pod` applies by default to the controllers that create Pods
  (Deployment, DaemonSet, StatefulSet, Job, CronJob); Kyverno adds `autogen-` rules for them. Inspect
  `kubectl get cpol <name> -o yaml` for the rules Kyverno actually added, and control it with the
  autogen settings in the Autogen docs; a policy that looks like it only matches `Pod` may already cover
  Deployments too, which can double-report if you also wrote an explicit Deployment rule.
- `mutate` runs before `validate` in the same policy evaluation, same as native
  webhooks — a mutate rule that fixes a value the validate rule would have
  rejected means the validate rule never fires; order rules deliberately.

## Verify
- [ ] Every new policy ran with `failureAction: Audit` and background scanning for at least one full
      deploy cycle; `kubectl get policyreport -A` reviewed before `Enforce`.
- [ ] `generate` rules' `synchronize` setting matches intent (lockstep vs.
      one-time default), and this is documented next to the policy.
- [ ] `verifyImages` `imageReferences` scoped to registries you actually sign for;
      unsigned base/vendor images are explicitly excluded or exempted.
- [ ] `PolicyException` support is confirmed enabled (`enablePolicyException` and `exceptionNamespace`)
      before relying on any exception object to take effect.
- [ ] Kyverno controller's own RBAC is reviewed — `generate`/`mutate` capability
      is scoped to the kinds/namespaces policies actually need.

## Checked

Documentation release: Kyverno docs (kyverno/website src/content/docs, repo commit 2026-10-23; Kyverno release v1.19.2).
Confirmed: the v1.19 deprecation and v1.20 removal of ClusterPolicy, Policy and the legacy PolicyException; `validate.failureAction` replacing `spec.validationFailureAction`; `emitWarning`; `background` default true; validate subrules including `cel` since 1.11; generate `synchronize` behaviour table, `orphanDownstreamOnPolicyDelete`, `generateExisting`; verifyImages fields (`imageReferences`, `skipImageReferences`, `required`) and keyless `subject`/`issuer`; the new `policies.kyverno.io/v1` PolicyException example, and the `enablePolicyException` and `exceptionNamespace` flags; autogen covering Pod controllers.
Corrected: the policy-level `validationFailureAction`, the claim that synchronize deletes the downstream on policy deletion unconditionally, the "silently does nothing" statement, the legacy PolicyException example, and the generate ServiceAccount description. Removed the unsourced background timer remark.

Method: documentation only; no commands were run.
