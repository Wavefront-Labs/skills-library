---
id: computing-software.cloud-infrastructure-engineering.kubernetes.admission-webhooks-validating-and-mutating
name: admission-webhooks-validating-and-mutating
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, admission-webhook, validatingwebhookconfiguration, mutatingwebhookconfiguration, admissionreview, admissionregistration, failurepolicy, timeoutseconds, sideeffects, reinvocationpolicy, matchpolicy, namespaceselector, cert-manager, opa, gatekeeper, kyverno, webhook-outage, ha]
level: advanced
status: docs-checked
description: "AdmissionReview request/response mechanics for validating and mutating webhooks, and the failurePolicy/HA mistakes that take down the whole API server."
sources: ["https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/", "https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/", "https://cert-manager.io/docs/concepts/ca-injector/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Admission webhooks — the mechanics that make or break the apiserver

**Goal:** understand the request/response contract well enough to write a webhook
(or operate someone else's, e.g. Gatekeeper/Kyverno) that enforces policy without
becoming a single point of failure for every `kubectl apply` in the cluster. RBAC
and Pod Security Standards are in
`computing-software.cloud-infrastructure-engineering.kubernetes.k8s-rbac-and-security`;
the built-in (non-webhook) controller chain is in
`computing-software.cloud-infrastructure-engineering.kubernetes.built-in-admission-controllers-and-apiserver-flags`.

## 1. Where webhooks sit in the request pipeline
Authentication → Authorization (RBAC) → **Mutating admission (built-in plugins and mutating
webhooks)** → Object schema validation → **Validating admission (built-in plugins,
ValidatingAdmissionPolicy and validating webhooks)** → etcd write.
Mutating admission runs *before* validating admission so a mutation (e.g. injecting a sidecar)
is itself validated afterward.

## 2. The AdmissionReview contract
The apiserver POSTs an `AdmissionReview` object to your webhook's HTTPS endpoint;
you return an `AdmissionReview` with `response.allowed` (bool), optional
`response.status.message`, and for mutating webhooks a base64 JSONPatch in
`response.patch` + `patchType: JSONPatch`.
```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
webhooks:
- name: require-labels.example.com
  clientConfig:
    service: {name: policy-webhook, namespace: policy, path: /validate}
    caBundle: <PEM>
  rules:
  - {apiGroups: [""], apiVersions: [v1], operations: [CREATE, UPDATE], resources: [pods]}
  failurePolicy: Fail
  sideEffects: None
  admissionReviewVersions: [v1]
  timeoutSeconds: 5
  namespaceSelector: {matchExpressions: [{key: kubernetes.io/metadata.name, operator: NotIn, values: [kube-system]}]}
```

## 3. `failurePolicy` is the decision that bites production
- `Fail` (the default in `admissionregistration.k8s.io/v1`): if the webhook is unreachable or
  times out, the request is **rejected**. Correct for security-critical policy — but
  if your webhook deployment goes to zero replicas, **every matching create/update
  cluster-wide stops**, including the webhook's own pod restart if it's not excluded.
- `Ignore`: unreachable webhook = request proceeds unchecked. Correct for
  best-effort mutation (sidecar injection) where availability beats enforcement, but
  silently defeats a security control with no signal.
- Always exclude `kube-system` (and the webhook's own namespace) via
  `namespaceSelector`/`objectSelector` when `failurePolicy: Fail` — otherwise a
  webhook outage can block the very components needed to fix it (CNI pods, CoreDNS,
  the webhook's own controller).

## 4. `timeoutSeconds` and the apiserver budget
- The allowed range is 1 to 30 seconds. Every webhook call adds to API request
  latency, so chatty webhooks degrade every write in the cluster, not just the ones
  they inspect. Keep webhooks fast (local in-memory checks); budget 1-3s typically.
- A webhook calling out to an external service (image registry, OPA data API) on
  the hot path is a latency and availability liability — cache or pre-sync data.

## 5. Mutating webhook specifics
- `reinvocationPolicy: IfNeeded` lets the webhook be called again if later admission
  plugins modify the object (the number of extra invocations is not guaranteed);
  `Never` (default) means it is called at most once per admission evaluation, so two
  mutating webhooks that patch the same field can leave the later one winning. To
  validate the object after all mutations are complete, use a validating webhook.
- JSONPatch ops must target paths that exist or use `add` on a parent that exists;
  a patch against a path the object doesn't have throws, which with `failurePolicy:
  Fail` rejects the request.
- In `v1`, `sideEffects` must be `None` or `NoneOnDryRun`. A webhook that has side
  effects on dry-run requests and does not suppress them must not be sent `dryRun: true`
  requests, so those API requests fail instead (`NoneOnDryRun` means the webhook is
  dry-run aware and suppresses its side effects).

## 6. HA and certificate rotation
- Run ≥2 replicas behind a Service with a PodDisruptionBudget; a single-replica
  webhook is a guaranteed outage during any node drain if `failurePolicy: Fail`.
- `caBundle` must match the serving cert's CA exactly; a stale `caBundle` after
  cert rotation causes TLS handshake failures that can look like a slow or
  unreachable webhook unless you
  check cert expiry. cert-manager's `cainjector` (annotation
  `cert-manager.io/inject-ca-from: <namespace>/<Certificate-name>`) automates keeping
  `caBundle` in sync with rotated certs.
- `matchPolicy: Equivalent` (default) matches requests via any API version/group
  alias that maps to the same resource, not just the literal `apiVersions` listed —
  important when clients use an older API version.

## Gotchas
- A `MutatingWebhookConfiguration` with `failurePolicy: Fail` and no namespace
  exclusion has, in practice, bricked clusters: the webhook pod crash-loops →
  nothing matching can be created, including the pods that would fix it. Keep a
  break-glass path (for example `matchConditions` that skip requests from an
  admin group) and know how to delete or edit the webhook configuration.
- `objectSelector` matches labels on the object being admitted; `namespaceSelector`
  matches labels on its namespace — mixing them up silently under- or over-scopes
  the webhook.

## Verify
- [ ] Every `failurePolicy: Fail` webhook excludes `kube-system` and its own namespace.
- [ ] Webhook deployment has ≥2 replicas, a PodDisruptionBudget, and a liveness probe
      independent of the policy-evaluation path.
- [ ] `caBundle` matches current serving cert (`openssl x509 -in cert -noout -dates`
      vs. the webhook config); cert rotation is automated (cert-manager or equivalent).
- [ ] p99 webhook response time is measured and under ~1s; alerting exists on webhook
      latency/error rate, not just pod liveness.
- [ ] A deliberate webhook-down test (scale to 0 in staging) produces the expected
      behavior (block vs. pass-through) and not a cluster-wide outage.

## Checked
Checked 2026-10-23 against the kubernetes/website docs (current release 1.37) and the cert-manager docs.
Confirmed: failurePolicy default Fail; timeoutSeconds range 1-30; reinvocationPolicy semantics and default Never;
matchPolicy default Equivalent; `sideEffects` values None/NoneOnDryRun and dry-run behaviour; mutating-then-validating
phases; cert-manager `cainjector` annotation. Removed unconfirmed claims (apiserver error wording, audit-stage
behaviour, delete-while-blocked recovery path).
Method: documentation only; no commands were run.
