---
id: computing-software.devops-ci-cd.flux.helmrelease-force-and-reset
name: helmrelease-force-and-reset
category: computing-software
field: devops-ci-cd
product: flux
tags: [helmrelease, forceat, resetat, reconcile, annotation]
level: advanced
status: docs-checked
description: "Force a one-off Helm release or reset remediation retries on a HelmRelease using annotations or flux reconcile --force."
sources:
  - https://fluxcd.io/flux/components/helm/helmreleases/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two annotations let you nudge helm-controller without changing the spec. Each must be set together with a reconcile request of the same value, and acts only if the value differs from the last one handled (see `.status.lastHandledForceAt`, `.status.lastHandledResetAt`, `.status.lastHandledReconcileAt`).

Force a one-off install or upgrade, for example to recover from a stuck release:

```sh
TOKEN="$(date +%s)"; \
kubectl annotate --field-manager=flux-client-side-apply --overwrite helmrelease/NAME \
"reconcile.fluxcd.io/requestedAt=$TOKEN" \
"reconcile.fluxcd.io/forceAt=$TOKEN"
```

or simply:

```sh
flux reconcile helmrelease NAME --force
```

Reset the failure counters so the controller keeps trying according to install and upgrade remediation after retries ran out:

```sh
TOKEN="$(date +%s)"; \
kubectl annotate --field-manager=flux-client-side-apply --overwrite helmrelease/NAME \
"reconcile.fluxcd.io/requestedAt=$TOKEN" \
"reconcile.fluxcd.io/resetAt=$TOKEN"
```

(`flux reconcile helmrelease NAME --reset` does the same.)

Failed uninstall: the controller retries until it succeeds and the HelmRelease stays failed meanwhile. If the cause cannot be fixed, force delete by manually deleting the Helm storage Secret for the release.

Find out why a release fails with `flux get helmreleases` and `kubectl describe helmrelease NAME` (Status and Events sections).

## Checked

2026-11-03. Read the HelmRelease reference (fluxcd.io/flux/components/helm/helmreleases/) (forceAt, resetAt, requestedAt annotations, `.status.lastHandled*At`, failed uninstall handling) and the flux reconcile helmrelease CLI page (`--force`, `--reset`). Replaced `flux get helmrelease NAME` with `flux get helmreleases`, the documented form.

Method: documentation only; no commands were run.
