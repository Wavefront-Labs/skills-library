---
id: computing-software.devops-ci-cd.argo-cd.flux-helmrelease-drift-detection-and-remediation
name: flux-helmrelease-drift-detection-and-remediation
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, helmrelease-drift-detection, helmrelease-remediation, helmrelease, flux-v2]
level: advanced
status: docs-checked
description: "Configure Flux HelmRelease drift detection (driftDetection enabled/warn, ignore rules) and install/upgrade remediation (retries, rollback, uninstall) for safe Helm GitOps."
sources: ["https://fluxcd.io/flux/components/helm/helmreleases/#drift-detection", "https://fluxcd.io/flux/components/helm/helmreleases/#configuring-failure-handling", "https://github.com/fluxcd/helm-controller/blob/main/docs/spec/v2/helmreleases.md", "https://github.com/fluxcd/flux2/blob/main/cmd/flux/reconcile_helmrelease.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HelmRelease drift detection and remediation

## Drift detection (helm-controller v2 API)
Helm alone never notices `kubectl edit` changes. Enable cluster-state comparison:
```yaml
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
metadata: { name: podinfo, namespace: apps }
spec:
  interval: 10m
  chart:
    spec: { chart: podinfo, version: "<semver-range>", sourceRef: { kind: HelmRepository, name: podinfo } }
  driftDetection:
    mode: enabled          # warn = detect and report only
    ignore:
      - paths: ["/spec/replicas"]
        target: { kind: Deployment }
```
With `warn` or `enabled`, once the HelmRelease is in sync with the Helm release in storage, the controller compares the stored manifest with the cluster using a server-side dry-run apply and
emits a Kubernetes Event summarising any drift. With `enabled` it also corrects the drift by
creating and patching the resources from the dry-run result (it does not run a Helm upgrade).
Start with `warn` to discover noisy fields; `ignore` takes JSON Pointers with an optional
`target` selector (group, version, kind, name, namespace, label and annotation selectors).

## Remediation on failure
```yaml
spec:
  install:
    remediation: { retries: 3 }
  upgrade:
    remediation:
      retries: 3
      strategy: rollback        # or uninstall
      remediateLastFailure: true
    cleanupOnFail: true
  rollback: { cleanupOnFail: true }
  timeout: 10m
```
`retries` defaults to `0` (a negative value means infinite). `strategy` defaults to `rollback`
(`uninstall` is the alternative, after which the controller tries to reinstall), and
`remediateLastFailure` defaults to `false` unless `retries` is greater than `0`. The `rollback`
block applies when the upgrade remediation strategy is `rollback`.

## Operations
```bash
flux get hr -A
flux reconcile hr podinfo -n apps --force       # force upgrade even if nothing changed
flux reconcile hr podinfo -n apps --reset        # reset the failure count
kubectl -n apps describe hr podinfo             # status conditions and events
```

## Verify
- [ ] Manually editing the Deployment image is reverted on next interval (mode enabled); a broken chart version rolls back after retries.

## Checked

2026-10-25, against the helm-controller HelmRelease v2 spec (main) and flux2 `reconcile_helmrelease.go`. Confirmed: `driftDetection.mode` warn/enabled behaviour (server-side dry-run, correction by patching), `ignore` paths and `target`, `install.remediation` and `upgrade.remediation` fields and defaults, `rollback.cleanupOnFail`, `flux reconcile hr --force` and `--reset`. Wrong in the earlier text: drift correction is not a Helm upgrade; `rollback.recreate` is deprecated and has no effect since Flux v2.8; the claimed 'v2.4+' gate for `--reset` and the 'retries exhausted' wording were unconfirmed and removed.

Method: documentation only; no commands were run.
