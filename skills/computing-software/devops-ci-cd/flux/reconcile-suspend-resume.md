---
id: computing-software.devops-ci-cd.flux.reconcile-suspend-resume
name: reconcile-suspend-resume
category: computing-software
field: devops-ci-cd
product: flux
tags: [flux-reconcile, suspend, resume, requestedat, reconcile-annotation]
level: sme
status: docs-checked
description: "Trigger on-demand Kustomization reconciliation, suspend or resume it, and pause one resource with the reconcile annotation."
sources:
  - https://fluxcd.io/flux/components/kustomize/kustomizations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Trigger a reconcile outside the interval by setting `reconcile.fluxcd.io/requestedAt` to any value that differs from `.status.lastHandledReconcileAt`:

```sh
kubectl annotate --field-manager=flux-client-side-apply --overwrite \
  kustomization/NAME reconcile.fluxcd.io/requestedAt="$(date +%s)"
```

The annotation queues the Kustomization for reconciliation only if the value differs from the last one the controller acted on.

Pause a whole Kustomization with `.spec.suspend: true`, or use `flux suspend kustomization NAME` and `flux resume kustomization NAME`. While suspended, new source revisions are not applied and drift detection and correction are paused. To resume, set the field to `false` or remove it. Setting `false` allows no hot patching with kubectl under GitOps because the declared state in Git overwrites the patch.

Pause one resource managed by a Kustomization by annotating or labelling it in-cluster:

```yaml
kustomize.toolkit.fluxcd.io/reconcile: disabled
```

The controller then neither applies changes to it nor prunes it. Resume by setting the value to `enabled` in the source, or by removing it from the live object.

Wait for `Ready` with `kubectl wait kustomization/NAME --for=condition=ready --timeout=1m`.

## Checked

2026-11-08. partial read of https://github.com/fluxcd/kustomize-controller/blob/main/docs/spec/v1/kustomizations.md: only the Suspend, Triggering a reconcile, Waiting for Ready and Suspending and resuming sections.

Removed or corrected: the --with-source flag, the claims for other kinds, the Suspended column and incident remarks, and the not-pruned claim for a suspended object, none of which is in the Suspend and Triggering sections.

Method: documentation only; no commands were run.
