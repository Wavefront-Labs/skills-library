---
id: computing-software.cloud-infrastructure-engineering.kubernetes.operator-status-conditions-and-observability
name: operator-status-conditions-and-observability
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, operator, status-conditions, metav1-condition, observedgeneration, printer-columns, kubectl-get, events-v1, controller-runtime-recorder, condition-utils, status-subresource, debuggability, event-recorder]
level: advanced
status: docs-checked
description: "Design a CRD's status: metav1.Condition conventions, observedGeneration, additionalPrinterColumns and Events so an operator is debuggable from kubectl get/describe alone."
sources: ["https://pkg.go.dev/k8s.io/apimachinery/pkg/api/meta", "https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Condition", "https://book.kubebuilder.io/reference/raising-events", "https://book.kubebuilder.io/reference/good-practices"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Operator status, conditions and observability — make the CRD tell its own story

**Goal:** an operator whose health, in-progress state, and failures are all
readable with `kubectl get`/`describe` and `kubectl get events` — no log-diving
required for the common cases. This is the difference between an operator
production teams trust at 3am and one that gets paged out of.

## 1. Use `metav1.Condition`, not a free-form string
```go
type WidgetStatus struct {
    ObservedGeneration int64              `json:"observedGeneration,omitempty"`
    Conditions         []metav1.Condition `json:"conditions,omitempty"`
}
```
`metav1.Condition` (in `k8s.io/apimachinery/pkg/apis/meta/v1`) has
`Type`, `Status` (`True`/`False`/`Unknown`), `ObservedGeneration`, `LastTransitionTime`,
`Reason` (CamelCase, required, not empty), `Message` (human-readable, may be empty). Use the
`k8s.io/apimachinery/pkg/api/meta` helpers (`meta.SetStatusCondition`,
`meta.FindStatusCondition`) — `SetStatusCondition` sets `LastTransitionTime` to now only when the status
differs from the existing condition (or the type is new), and avoids duplicate-type bugs from manual
slice manipulation.
```go
meta.SetStatusCondition(&widget.Status.Conditions, metav1.Condition{
    Type: "Ready", Status: metav1.ConditionFalse,
    ObservedGeneration: widget.Generation,
    Reason: "DependencyUnavailable", Message: "waiting on Secret db-creds",
})
```
Pick 2-5 condition `Type`s that mean something stable over the object's lifetime
(`Ready`, `Progressing`, `Degraded` is a common trio) — don't invent a new
condition type per code path; that's what `Reason` is for.

## 2. `observedGeneration` — the field that tells you if status is stale
`metadata.generation` increments on every spec change (not on status-only
updates). Mirror it into `status.observedGeneration` whenever you've actually
processed the current spec. Any consumer (a dashboard, `kubectl get`, a human)
can then tell "has the controller even looked at my latest edit yet?" by comparing
`.metadata.generation` to `.status.observedGeneration` — mismatch means stale,
either a stuck controller or a reconcile still in flight. Set both the top-level
`status.observedGeneration` and (if using per-condition tracking) each condition's
own `observedGeneration`, since a condition can lag behind a newer generation if
part of reconciliation is still catching up.

## 3. Printer columns — the first thing anyone checks
```yaml
additionalPrinterColumns:
- name: Ready
  type: string
  jsonPath: .status.conditions[?(@.type=="Ready")].status
- name: Reason
  type: string
  jsonPath: .status.conditions[?(@.type=="Ready")].reason
- name: Age
  type: date
  jsonPath: .metadata.creationTimestamp
```
Kubebuilder marker equivalent: `// +kubebuilder:printcolumn:name="Ready",type="string",JSONPath=".status.conditions[?(@.type=='Ready')].status"`.
Without printer columns, `kubectl get widgets` shows only NAME and AGE, forcing every
investigation to start with `-o yaml`.

## 4. Events — the timeline conditions can't hold
Conditions show current state; **Events** show the history of
what happened, visible via `kubectl describe` and `kubectl get events`. With the Kubebuilder
scaffold the recorder comes from `mgr.GetEventRecorder("<name>-controller")` and a call looks like
`r.Recorder.Eventf(cr, nil, corev1.EventTypeWarning, "CleanupFailed", "Cleanup", "could not delete load balancer: %v", err)`
(arguments: regarding, related, event type, reason, action, message). The `reason` should be short
`UpperCamelCase`. The Kubebuilder docs recommend not emitting Events for every operation, because too many
make them hard to use. The kube-apiserver `--event-ttl` flag defaults to 1h, so Events are not an audit log;
anything needing retention belongs in Conditions (current) or external logs and metrics (history).

## 5. Metrics and the manager's built-in endpoints
controller-runtime's manager exposes `/metrics` (controller-runtime's own
reconcile count/duration/error histograms per controller, Prometheus format) and
`/healthz`/`/readyz` for liveness/readiness — wire these into a ServiceMonitor and
probes rather than rebuilding them. Add custom business metrics (e.g.
"widgets_provisioning_duration_seconds") sparingly and only for things Conditions/
Events can't express as a single current snapshot — a duration histogram across
many objects, not a single object's state.

## Gotchas
- Updating `status` and `spec` in the same `Update` call risks losing one to a
  resourceVersion conflict if something else wrote in between — always use the
  `/status` subresource client (`r.Status().Update(ctx, obj)`) for condition
  changes, never the main client.
- `LastTransitionTime` set to `time.Now()` on every reconcile (instead of only on
  actual status flips) makes conditions useless for "how long has this been
  broken" — always gate it on an actual `Status` change, which `meta.SetStatusCondition`
  does correctly if you let it own the comparison.
- A `Ready: True` condition that's actually a lie (set optimistically before the
  cleanup/creation step that could fail) is worse than no condition — set it last,
  after the thing it claims is actually true.
- Verify printer column `jsonPath` expressions against a real object.

## Verify
- [ ] `kubectl get widgets` shows Ready/Reason/Age without `-o yaml`.
- [ ] After editing spec, `status.observedGeneration` lags briefly then catches up
      to `metadata.generation` within one reconcile.
- [ ] Injecting a failure (delete a dependency) produces both a `Ready=False`
      condition with an accurate `Reason`/`Message` and a corresponding Warning
      Event, visible in `kubectl describe`.
- [ ] `/metrics` on the manager's bind address exposes
      `controller_runtime_reconcile_total` with nonzero count for the controller.

## Checked

Checked on 2026-10-26 against `kubernetes/apimachinery` (`pkg/api/meta/conditions.go`, `pkg/apis/meta/v1/types.go`), the Kubebuilder book (`reference/raising-events`, `reference/good-practices`) on `kubernetes-sigs/kubebuilder`, and `kubernetes/kubernetes` (`EventTTL` default of 1h).
Confirmed: `metav1.Condition` fields and the `True`/`False`/`Unknown` status enum, non-empty CamelCase `reason`, `observedGeneration` semantics (condition is stale when it lags `.metadata.generation`), `SetStatusCondition` and `FindStatusCondition` helpers and their `LastTransitionTime` behaviour, the Kubebuilder Eventf signature and advice to limit Events, `--event-ttl` default 1h, controller-runtime metric `controller_runtime_reconcile_total`.
Corrected: the Event recorder call now uses the `Eventf(regarding, related, ...)` form in the current Kubebuilder docs. Removed as unconfirmed: API-server Event deduplication/drop behaviour and the silent `<none>` printer-column failure.

Method: documentation only; no commands were run.
