---
id: computing-software.cloud-infrastructure-engineering.kubernetes.drift-detection-and-reconciliation
name: drift-detection-and-reconciliation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, gitops, drift, drift-detection, outofsync, self-heal, prune, ignoredifferences, server-side-apply, mutating-webhook, hpa-drift, argo-cd, fluxcd, reconciliation, manual-kubectl-edit]
level: practitioner
status: docs-checked
description: "Diagnose GitOps drift: real OutOfSync causes (manual edits, mutating webhooks, HPA/VPA-managed fields), self-heal vs prune, and scoping ignoreDifferences narrowly."
sources: ["https://github.com/argoproj/argo-cd/blob/master/docs/user-guide/diffing.md", "https://github.com/argoproj/argo-cd/blob/master/docs/user-guide/auto_sync.md", "https://github.com/argoproj/argo-cd/blob/master/docs/user-guide/sync-options.md", "https://github.com/fluxcd/kustomize-controller/blob/main/docs/spec/v1/kustomizations.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Drift detection and reconciliation — knowing why OutOfSync fired, not just clearing it

**Goal:** every `OutOfSync`/drift alert has a specific cause. The failure mode this
skill exists to prevent is reflexively adding an `ignoreDifferences` rule (or
clicking "sync") without knowing which of four distinct causes produced the diff —
each needs a different fix.

## 1. The four real causes of drift
1. **Someone ran `kubectl edit`/`kubectl patch` directly.** The fix is social
   (break-glass process, RBAC restricting direct write access) as much as technical —
   GitOps tooling will keep re-flagging or reverting this, which is correct behavior,
   not a bug to suppress.
2. **A controller mutates the resource after apply** — HPA writes
   `spec.replicas` (and may reorder `spec.metrics`), VPA writes resource requests/limits, a
   mutating admission webhook or another controller alters the object after it was submitted. This
   is *expected* drift from a
   legitimate in-cluster actor, not a human error — the fix is scoping
   `ignoreDifferences`/equivalent to that exact field, not disabling diffing broadly.
3. **Manifest or rendering problems** — per the Argo CD diffing docs, a manifest with
   extra or unknown fields (dropped when the live state is read back) shows as OutOfSync, and a
   Helm chart using a function like `randAlphaNum` produces different data on every render. Argo
   CD also ignores the `status` field when diffing by default (`ignoreResourceStatusField: all`).
   Fix the manifest where you can; use `ignoreDifferences` only when you cannot.
4. **Genuine reconciliation lag** — the change is in git, the controller hasn't
   applied it yet (interval not elapsed, controller down, admission webhook
   rejecting the apply). This clears on its own or on a forced reconcile
   (`argocd app sync`/`flux reconcile kustomization`); treat as drift
   only if it persists past the expected interval.

## 2. Scoping the exception correctly (Argo CD)
```yaml
spec:
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers: ["/spec/replicas"]       # HPA owns this field
    - group: admissionregistration.k8s.io
      kind: MutatingWebhookConfiguration
      jqPathExpressions: ['.webhooks[]?.clientConfig.caBundle']   # field set by another controller
```
`jsonPointers` use RFC 6902 paths (escape a `/` inside a key as `~1`), `jqPathExpressions` select
list items by content, and `managedFieldsManagers` ignores fields owned by named managers. Scope
the rule narrowly (a path, and `name`/`namespace` where possible); broad rules such as
`managedFieldsManagers` on every kind hide real drift as well. The same settings can be applied
system-wide through `resource.customizations` in `argocd-cm`.

## 3. `self-heal` vs `prune` — different knobs, different risk
- **Self-heal** (`automated: {selfHeal: true}` in Argo CD, off by default: live-cluster changes
  do not trigger an automated sync unless it is set; Flux's Kustomization runs a server-side apply
  dry-run every `.spec.interval` to detect and correct drift) reverts a manual edit back to
  git's state. Protects against drift cause #1 but will also fight
  a well-intentioned emergency `kubectl edit` during an incident — know how to
  pause reconciliation before you need it at 2am: in Argo CD set
  `spec.syncPolicy.automated.enabled: false` (for an ApplicationSet-managed Application, changing
  the Application has no effect; change the ApplicationSet), in Flux set `.spec.suspend: true` or
  run `flux suspend kustomization <name>`, which pauses drift correction as well as new
  revisions.
- **Prune** removes live resources no longer present in git (off by default for Argo CD
  automated sync, with a separate `allowEmpty` safeguard against pruning everything; `.spec.prune`
  is a required field on a Flux Kustomization). Without it, deleting a
  manifest leaves an orphan (a quieter, opposite failure mode from drift:
  "git says it's gone but it's still running"). Prune is the one that needs the
  tightest directory-path scoping (see
  `computing-software.cloud-infrastructure-engineering.kubernetes.gitops-repo-structure-patterns`)
  because an overly broad apply scope + `prune: true` can delete another team's
  resources that happen to share a namespace.

## 4. Server-side apply changes the picture
Field-manager-aware server-side apply (SSA) means multiple actors (your GitOps
controller, HPA, a webhook) can own *different fields of the same object*. In Argo CD, SSA is
opt-in with the `ServerSideApply=true` sync option (per Application or per resource via the
`argocd.argoproj.io/sync-options` annotation), which then runs `kubectl apply --server-side
--force-conflicts`; `Force=true` on its own does not combine with it. Flux's Kustomization applies
with server-side apply. Check which mode your setup uses, since it changes which diffs are
conflicts versus expected multi-owner fields.

## Gotchas
- `ignoreDifferences` rules accumulate silently over time as a team firefights one
  false positive after another — audit them periodically; a long list is a sign the
  diff tool's defaults aren't matching your actual controller mix, not a sign
  everything's fine.
- Self-heal + a controller that legitimately needs to mutate a field *not* covered by
  an ignore rule creates a fight loop (GitOps reverts, controller re-mutates,
  repeat) that burns API server write throughput — visible as rapid resourceVersion
  churn; diagnose with `kubectl get <resource> -w` before blaming either side.
- A webhook that fails open/closed differently under load can produce drift that
  looks like cause #2 but is actually cause #4 (reconciliation lag from a rejected
  apply) — check controller/webhook error logs before writing an ignore rule.

## Verify
- [ ] Every `ignoreDifferences`/equivalent rule in the repo is scoped to a specific
      path, and a comment next to it names which controller/actor legitimately owns
      that field.
- [ ] A deliberately introduced manual `kubectl edit` on a self-heal-enabled app
      reverts within one reconcile interval.
- [ ] Deleting a manifest from git actually removes the live resource (prune is
      scoped correctly and working).
- [ ] The team has a documented, tested way to pause reconciliation during an
      incident without having to look it up live.

## Checked

Checked 2026-10-27. Documentation checked: Argo CD docs (diffing, automated sync, sync options; argoproj/argo-cd master) and Flux kustomize-controller Kustomization spec (main). Confirmed: `ignoreDifferences` fields `jsonPointers`, `jqPathExpressions`, `managedFieldsManagers` and group/kind/name/namespace scoping, the `~1` escape, HPA reordering `spec.metrics`, `randAlphaNum` Helm drift, `ignoreResourceStatusField` default `all`, `selfHeal`/`prune`/`allowEmpty` defaults, `automated.enabled`, ApplicationSet override note, `ServerSideApply=true` and `Force=true` interaction, Flux `.spec.interval` dry-run drift correction, `.spec.suspend`, `.spec.prune`, `flux suspend kustomization` and `flux reconcile kustomization`. Fixed: removed `argocd app set --sync-policy none` (not documented), the "no path ignores everything" claim and the cert-manager and CRD-without-status-subresource attributions, none of which the docs support.

Method: documentation only; no commands were run.
