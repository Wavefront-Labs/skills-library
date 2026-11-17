---
id: computing-software.cloud-infrastructure-engineering.kubernetes.admission-webhook-development
name: admission-webhook-development
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, operator, admission-webhook, validatingwebhookconfiguration, mutatingwebhookconfiguration, controller-runtime, webhook-validator, webhook-defaulter, cert-manager, ca-bundle-injection, failurepolicy, sideeffects, dry-run, kubebuilder-webhook]
level: advanced
status: docs-checked
description: "Build a CRD's own validating/mutating webhook with controller-runtime: the Validator/Defaulter interfaces, cert injection, failurePolicy choice, and dry-run correctness."
sources: ["https://book.kubebuilder.io/cronjob-tutorial/webhook-implementation", "https://book.kubebuilder.io/cronjob-tutorial/cert-manager", "https://github.com/kubernetes-sigs/controller-runtime/tree/main/pkg/webhook", "https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Admission webhook development for a CRD — the controller-runtime side of validation and defaulting

**Goal:** give your own CRD a validating and/or mutating webhook that runs inside
the operator binary, registered via controller-runtime, correctly surviving
`dry-run`, rolling upgrades, and certificate rotation. This is scoped to building
the webhook *as part of an operator* (your CRD, your Go types); for general
cluster-wide admission policy (Kyverno/Gatekeeper/OPA, ValidatingAdmissionPolicy
over built-in resources) see
`computing-software.cloud-infrastructure-engineering.kubernetes.k8s-rbac-and-security`.
Prefer `x-kubernetes-validations` (CEL) in the CRD schema over a webhook wherever
it reaches — see
`computing-software.cloud-infrastructure-engineering.kubernetes.crd-schema-design-and-validation`
— and write a webhook only for checks CEL can't express (cross-resource lookups,
calls to an external system, defaulting that depends on other objects in the
cluster).

## 1. The two interfaces
`kubebuilder create webhook --group apps --version v1 --kind Widget --defaulting
--programmatic-validation` scaffolds a defaulter and a validator as separate structs
(in the current Kubebuilder CronJob tutorial) with typed, context-taking methods:
```go
func (d *WidgetDefaulter) Default(ctx context.Context, obj *appsv1.Widget) error { ... }          // mutating
func (v *WidgetValidator) ValidateCreate(ctx context.Context, obj *appsv1.Widget) (admission.Warnings, error) { ... }
func (v *WidgetValidator) ValidateUpdate(ctx context.Context, oldObj, newObj *appsv1.Widget) (admission.Warnings, error) { ... }
func (v *WidgetValidator) ValidateDelete(ctx context.Context, obj *appsv1.Widget) (admission.Warnings, error) { ... }
```
Older Kubebuilder and controller-runtime releases put `Default()` and `Validate*` methods
directly on the API type; check the scaffold your project version generated.
`ValidateUpdate` gets the old object — use it for immutability/monotonic rules that
need cross-object comparison CEL's `oldSelf` can't reach (e.g. a rule depending on
a different resource's current state). Returning a non-nil `error` rejects the
request with that message surfaced verbatim to the `kubectl apply` caller — make it
actionable, not a Go error string.

## 2. Registration and the webhook server
`ctrl.NewWebhookManagedBy(mgr, &appsv1.Widget{}).WithValidator(...).WithDefaulter(...).Complete()`
(called from the scaffolded `SetupWidgetWebhookWithManager(mgr)`) registers HTTP handlers on the manager's built-in
webhook server (default port 9443, serving `tls.crt`/`tls.key` from the configured cert directory;
the API server calls admission webhooks over HTTPS). The manager serves `/validate-apps-example-com-v1-widget` and
`/mutate-...` paths that must match the `ValidatingWebhookConfiguration`'s
`clientConfig.service.path` exactly; a path typo fails silently at the API-server
side as "webhook call failed" with no indication it's a path mismatch — check the
registered path against the generated config in `config/webhook/manifests.yaml`.

## 3. Certificates — the part that breaks in production first
TLS is mandatory and the API server validates the serving cert against a CA bundle
it's given out-of-band (CRD/webhook config, not standard cluster trust). Two paths:
- **cert-manager** (recommended): a `Certificate` resource issues the serving cert
  into a Secret the webhook pod mounts; the `cert-manager.io/inject-ca-from`
  annotation on the `*WebhookConfiguration` makes cert-manager's `ca-injector`
  patch in the current CA bundle automatically on rotation. Kubebuilder scaffolds
  this when you answer yes to webhook cert management.
- **Self-managed** (a Job that
  mints a cert at install time, or certificates you provision yourself into the cert directory): works but you own rotation — an expired serving
  cert makes the webhook unreachable, which (depending on `failurePolicy`) can
  block all writes to the CRD cluster-wide. Set a calendar reminder or monitoring
  alert on cert expiry if not using cert-manager.
- Whichever path: keep the webhook pod's readiness tied to the webhook server actually
  serving, so the Service has no endpoints until it can answer TLS requests.

## 4. failurePolicy and the blast radius
- `failurePolicy: Fail` (the default in `admissionregistration.k8s.io/v1`): webhook unreachable → write rejected.
  Protects invariants but means a broken/unready webhook deployment blocks *all*
  creates/updates matching the rule, including your own operator's upgrade rollout
  if it self-updates objects the webhook covers.
- `failurePolicy: Ignore`: webhook unreachable → write proceeds unchecked. Silent
  data-integrity gap during an outage — use only for webhooks that are pure
  convenience (defaulting a cosmetic field), never for anything load-bearing.
- Always exclude `kube-system` and the webhook's own namespace from
  `namespaceSelector` where feasible, and run 2+ replicas with a PodDisruptionBudget
  — a single-replica `Fail` webhook is a self-inflicted outage waiting for a node drain.
- `timeoutSeconds` (1 to 30, default 10): a slow webhook (calling an external API)
  delays every matching write by that long before failing; keep webhook logic fast
  and local, push slow checks to async reconciliation + status conditions instead.

## 5. Dry-run correctness
`kubectl apply --dry-run=server`, `kubectl diff`, and some CI/GitOps tools send
`dryRun: true` in the `AdmissionRequest`. A webhook that has side effects (calls an
external API, writes to another object) on every invocation will do so during a
dry-run too unless it explicitly checks `dryRun` and skips its side effects. The
Kubernetes docs require webhooks with side effects to skip them when `dryRun: true`.
Declare `sideEffects: NoneOnDryRun` for such a webhook; a webhook that does not declare
`None` or `NoneOnDryRun` does not receive dry-run requests, and the dry-run API request
fails instead. In controller-runtime read it from `admission.RequestFromContext(ctx)`
(`req.DryRun`, from the embedded `AdmissionRequest`) if the logic has any effect beyond computing the response.

## Gotchas
- `Default()` runs on every create/update including no-op resyncs from some
  clients — make it idempotent (setting the same default twice must be a no-op),
  same discipline as Reconcile (see `reconciliation-loop-design`).
- A mutating webhook that changes a field the CRD's own CEL validation then
  rejects produces a confusing "webhook accepted it, then it was rejected anyway"
  — validating webhooks run after all mutating webhooks (Kubebuilder's admission
  webhook reference states this), so validation sees the mutated object.
- `sideEffects` must be declared accurately: `None` or `NoneOnDryRun` in v1. Declaring
  `None` on a webhook that has real side effects makes dry-run tooling (`kubectl diff`,
  GitOps planning) trigger those effects.
- Webhook config `rules` with overly broad `apiGroups`/`resources` (e.g. `*`)
  slow down every matching write in the cluster, not just your CRD's, because each one
  adds a webhook call to API request latency.
- Webhooks on built-in types (Pod, Deployment) can deadlock the operator's own rollout;
  see the Kubebuilder "webhook bootstrap problem" page.

## Checked
Checked 2026-10-24 against the Kubernetes admission-controller reference on kubernetes.io
(current website source), the Kubebuilder book (CronJob tutorial webhook implementation,
cert-manager page, admission webhook reference) and controller-runtime `main`
(webhook server defaults: port 9443, `tls.crt`/`tls.key`; typed `Validator[T]`
interface with context). Confirmed: `timeoutSeconds` 1 to 30 and default 10;
`failurePolicy` values and default `Fail`; `sideEffects` values and dry-run behaviour;
`cert-manager.io/inject-ca-from` annotation; validating after mutating.
Method: documentation only; no commands were run.

## Verify
- [ ] `kubectl apply --dry-run=server` against an invalid object is rejected with
      the same message as a real apply, and produces no external side effect.
- [ ] Deleting the webhook Service temporarily: writes fail closed (`Fail`) or
      proceed as expected (`Ignore`) — matches the documented, intended policy.
- [ ] Cert rotation (manually trigger cert-manager renewal or wait for schedule)
      causes no downtime — webhook pods pick up the new cert without a restart or
      with a graceful one.
- [ ] `Default()` applied twice to an already-defaulted object produces zero diff.
