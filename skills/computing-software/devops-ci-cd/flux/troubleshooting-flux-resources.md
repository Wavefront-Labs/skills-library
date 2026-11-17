---
id: computing-software.devops-ci-cd.flux.troubleshooting-flux-resources
name: troubleshooting-flux-resources
category: computing-software
field: devops-ci-cd
product: flux
tags: [troubleshooting, flux-get, flux-logs, kubectl-events, not-ready]
level: sme
status: docs-checked
description: "Diagnose Flux failures with flux get, flux logs, CRD categories, events and fixes for common Kustomize and Helm errors."
sources:
  - https://fluxcd.io/flux/cheatsheets/troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Start broad:

```sh
flux get all -A --status-selector ready=false
kubectl get fluxcd -A
kubectl get events -n flux-system --field-selector type=Warning
flux logs --all-namespaces --level=error
flux check
```

`kubectl get fluxcd-sources -A` and `fluxcd-appliers -A` filter by CRD category (Flux CRD categories). Check `Ready=True` and `Suspend=False` on sources first (`flux get sources all -A`), then Kustomizations and HelmReleases (`flux get kustomizations -A`, `flux get helmreleases -A`). On k3s or clusters bundling another Helm controller, `kubectl get helmcharts` may hit the wrong CRD; use the full name `helmcharts.source.toolkit.fluxcd.io`.

Common causes:
- `webhook does not support dry run`: set `sideEffects` to `None` or `NoneOnDryRun` on the offending Validating or MutatingWebhookConfiguration.
- Endless `configured` events: remove optional fields set to null, empty string, empty object or empty list from your manifests, because the server-side dry-run drift check sees them as changes.
- `Request entity too large: limit is 3145728` on Helm install: the release no longer fits in a Secret; trim the chart with `.helmignore` and `.sourceignore`.
- `HelmChart is not ready`: check `flux get sources helm` for index fetch errors, then `flux get sources chart` for a bad chart name or version.
- `install retries exhausted`: `kubectl describe helmrelease NAME` shows the last Helm log; set `install.disableWait: true` and `upgrade.disableWait: true` temporarily to inspect the failing workload.
- `unable to open the Badger database` (image-reflector-controller in CrashLoopBackOff on low-memory boards such as Raspberry Pi 2 and 3, 1GB RAM): the default 100MB Raspbian swap file is too small; add at least 1GB swap via `/etc/dphys-swapfile`.

## Checked

2026-11-08. Read in full: https://fluxcd.io/flux/cheatsheets/troubleshooting/ (raw source in the fluxcd/website repository).

Removed or corrected: the claim that all Flux CRDs carry categories since Flux 2.9 (not on the page).

Method: documentation only; no commands were run.
