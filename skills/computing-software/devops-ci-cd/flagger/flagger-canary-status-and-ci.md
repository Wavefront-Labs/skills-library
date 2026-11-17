---
id: computing-software.devops-ci-cd.flagger.flagger-canary-status-and-ci
name: flagger-canary-status-and-ci
category: computing-software
field: devops-ci-cd
product: flagger
tags: [canary, status, kubectl, ci, promoted]
level: practitioner
status: docs-checked
description: "Read Flagger canary status conditions and wait for a rollout in CI with kubectl wait on the promoted condition."
sources:
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/how-it-works.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
List all canaries with `kubectl get canaries --all-namespaces` (columns STATUS, WEIGHT, LASTTRANSITIONTIME). Inspect with `kubectl -n test get canary/podinfo -oyaml | awk '/status/,0'`.

The `Promoted` condition reason is one of: Initialized, Waiting, Progressing, WaitingPromotion, Promoting, Finalising, Succeeded or Failed. A failed canary has `Promoted` false, reason `failed`, and its `lastAppliedSpec` differs from `lastPromotedSpec`. Status also carries `canaryWeight`, `failedChecks` and `iterations`.

CI pattern from the docs:

```bash
kubectl set image deployment/podinfo podinfod=stefanprodan/podinfo:3.0.1
ok=false
until ${ok}; do
    kubectl get canary/podinfo | grep 'Progressing' && ok=true || ok=false
    sleep 5
done
kubectl wait canary/podinfo --for=condition=promoted --timeout=5m
kubectl get canary/podinfo | grep Succeeded
```

The first loop waits for Flagger to notice the change; `kubectl wait` blocks until the analysis finishes; the final grep distinguishes success from failure, since a failed analysis ends the wait too.

## Checked

2026-11-03. Confirmed against the Flagger documentation: https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/how-it-works.md.

No wrong claims found; nothing needed removing.

Method: documentation only; no commands were run.
