---
id: computing-software.devops-ci-cd.argo-cd.argocd-cmd-params-cm-component-flags
name: argocd-cmd-params-cm-component-flags
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, server-insecure, argocd-server-flags, argocd-cmd-params-cm, controller-processors]
level: advanced
status: docs-checked
description: "Configure Argo CD component flags declaratively through argocd-cmd-params-cm: server.insecure, base paths, controller processors and timeouts, repo-server limits, and restarts."
sources: ["https://github.com/argoproj/argo-cd/blob/master/docs/operator-manual/argocd-cmd-params-cm.yaml", "https://github.com/argoproj/argo-cd/blob/master/docs/operator-manual/argocd-cm.yaml", "https://argo-cd.readthedocs.io/en/stable/operator-manual/app-any-namespace/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# argocd-cmd-params-cm: server and controller flags

Most command-line flags of `argocd-server`, `argocd-application-controller`,
`argocd-repo-server`, `argocd-applicationset-controller` and `argocd-dex-server` have a key here,
so you do not need to patch Deployment args.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cmd-params-cm
  namespace: argocd
  labels: { app.kubernetes.io/part-of: argocd }
data:
  server.insecure: "true"                     # serve HTTP; TLS terminated at ingress/LB
  server.basehref: /argocd                    # UI under a sub-path
  server.rootpath: /argocd
  server.log.format: json
  controller.status.processors: "50"          # default 20
  controller.operation.processors: "25"       # default 10
  controller.repo.server.timeout.seconds: "180"   # default 60
  controller.diff.server.side: "true"
  reposerver.parallelism.limit: "10"          # cap concurrent manifest generations (default 1; below 1 means no limit)
  application.namespaces: "team-*"
```

## Rules
- Restart the affected workload after changing a key (for example `kubectl rollout restart -n argocd deployment argocd-server`; the application controller is a StatefulSet by default).
- Values are strings — quote numbers/booleans.
- `server.insecure: "true"` runs the server without TLS (default false), so use it only when something in front terminates TLS.
- `timeout.reconciliation` (default two minutes plus jitter, set `timeout.reconciliation.jitter`) lives in **argocd-cm**, not here.

## Tuning hints
- Many apps, slow refresh → raise status processors and controller CPU; consider sharding.
- Repo-server memory pressure on big Helm/Kustomize renders → lower `reposerver.parallelism.limit` and raise memory.

## Verify
- [ ] After the restart the component behaves as configured (for example the server serves plain HTTP with `server.insecure`).

## Checked

Argo CD documentation, master branch (latest release v3.5.6), repository argoproj/argo-cd, last commit 2026-10-24. Checked 2026-10-25. Confirmed: keys and defaults in the reference argocd-cmd-params-cm.yaml (`server.insecure` false, `server.basehref` /, `server.rootpath`, `server.log.format` json, `controller.status.processors` 20, `controller.operation.processors` 10, `controller.repo.server.timeout.seconds` 60, `controller.diff.server.side`, `reposerver.parallelism.limit` 1, `application.namespaces`), restart requirement, `timeout.reconciliation` in argocd-cm (default two minutes, the old 180 s figure was stale). Removed the Helm `configs.params` remark and the processors-per-app ratio.

Method: documentation only; no commands were run.
