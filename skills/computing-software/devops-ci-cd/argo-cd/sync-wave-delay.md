---
id: computing-software.devops-ci-cd.argo-cd.sync-wave-delay
name: sync-wave-delay
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, sync-wave-delay, argocd-sync-wave-delay, wave-timing]
level: advanced
status: docs-checked
description: "Tune the pause between Argo CD sync waves with ARGOCD_SYNC_WAVE_DELAY when controllers need time to update status before the next wave proceeds."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/sync-waves/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sync wave delay

Between waves Argo CD waits for resources in the current wave to be **healthy**, then waits an
extra delay (default **2 seconds**) before applying the next wave. The delay gives other
controllers a chance to update `.status` — otherwise Argo CD might read a stale "healthy" status
from before the controller noticed the change.

## 1. Change it
Set on the application controller:
```yaml
# argocd-application-controller StatefulSet
env:
  - name: ARGOCD_SYNC_WAVE_DELAY
    value: "10"          # seconds
```

## 2. When to raise it
- CRD-backed resources whose operator reports health late (e.g. a database operator sets
  `Ready` after a reconcile loop), and the next wave depends on it.
- Webhook/cert-manager chains: wave 0 issues certificates, wave 1 needs the Secret present.
- Symptoms: later waves fail intermittently with "not found"/"connection refused" right after an earlier wave reported healthy.

## 3. Better fixes first
- Custom **health checks** (the FAQ describes health check customization) so Argo CD knows when the CRD is really ready (the wave then waits correctly, no blind delay).
- `PreSync`/`Sync` hooks (Jobs) that poll for readiness.
- The delay applies to every wave of every app on that controller — large values slow all syncs.

## Verify
- [ ] The sync operation timeline shows the expected gap between waves; intermittent failures stop.

## Checked
2026-10-31. Confirmed on the Argo CD sync-waves guide: delay between waves exists so other controllers can react and so health is not assessed against a stale object; current delay 2 seconds, configurable with `ARGOCD_SYNC_WAVE_DELAY`; and on the FAQ: health check customization. Removed unconfirmed claims: Helm `controller.env` key and the `--show-operation` command.
Method: documentation only; no commands were run.
