---
id: computing-software.devops-ci-cd.argo-cd.self-heal-timeout-and-backoff
name: self-heal-timeout-and-backoff
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, self-heal-timeout, self-heal, retry-backoff]
level: advanced
status: docs-checked
description: "Tune Argo CD self-heal timing (self-heal timeout and backoff) so drift fights with controllers and webhooks do not hammer the API server or spin forever."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/argocd-cmd-params-cm-yaml/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Self-heal timeout and backoff

When live state drifts from Git, self-heal triggers a sync, waiting between attempts.

## Settings
- `--self-heal-timeout-seconds` (controller flag; `controller.self.heal.timeout.seconds` in
  `argocd-cmd-params-cm`): delay before re-attempting self-heal; the auto-sync guide gives 5 seconds
  by default, while the example `argocd-cmd-params-cm` lists `controller.self.heal.timeout.seconds: "0"`.
- The same example ConfigMap documents exponential self-heal backoff between attempts:
  `controller.self.heal.backoff.timeout.seconds` (example value 2), `.factor` (3),
  `.cap.seconds` (300). Check the docs for your Argo CD version for how the fixed timeout and
  the backoff interact.
- Per-app sync retry (for failed syncs, not drift) is separate:
  ```yaml
  syncPolicy:
    automated: { selfHeal: true, prune: true }
    retry: { limit: 5, backoff: { duration: 5s, factor: 2, maxDuration: 3m } }
  ```

```yaml
apiVersion: v1
kind: ConfigMap
metadata: { name: argocd-cmd-params-cm, namespace: argocd }
data:
  controller.self.heal.backoff.timeout.seconds: "5"
  controller.self.heal.backoff.factor: "2"
  controller.self.heal.backoff.cap.seconds: "600"
```
Check that the application controller picked up the new values for your install method.

## Drift fights
Symptom: app flips Synced/OutOfSync constantly, history shows a sync every few seconds. Cause: a
controller/webhook mutates fields Argo manages (HPA replicas, injected sidecars, defaulted fields).
Fix the root cause with `ignoreDifferences` + `RespectIgnoreDifferences=true`, or ServerSideApply,
rather than slowing self-heal.

## Verify
- [ ] `kubectl -n argocd get cm argocd-cmd-params-cm -o yaml` shows values; controller logs show increasing intervals during a forced drift.

## Checked
2026-10-31. Confirmed on the Argo CD auto-sync guide (5 s self-heal timeout, `--self-heal-timeout-seconds`, `retry` block) and the `argocd-cmd-params-cm` example (`controller.self.heal.timeout.seconds`, `controller.self.heal.backoff.*` keys and example values 2, 3, 300). Removed unconfirmed claims: the 2.13+/3.x version gate, that backoff replaces the fixed timeout, and the controller-restart instruction.
Method: documentation only; no commands were run.
