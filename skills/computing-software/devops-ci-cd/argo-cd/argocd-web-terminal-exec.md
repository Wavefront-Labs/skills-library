---
id: computing-software.devops-ci-cd.argo-cd.argocd-web-terminal-exec
name: argocd-web-terminal-exec
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, exec-enabled, web-terminal, argocd-cm]
level: practitioner
status: docs-checked
description: "Enable or lock down the Argo CD web terminal (exec.enabled): RBAC exec create permission, server ClusterRole pods/exec, allowed shells and the audit risk."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/web_based_terminal/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/rbac/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Web terminal (exec.enabled)

Since v2.4 the UI can open a shell into pods of an application, like `kubectl exec`. Disabled by default.

## Enable
```yaml
# argocd-cm
data:
  exec.enabled: "true"
  exec.shells: "bash,sh"          # optional; default order is bash, sh, powershell, cmd
```
Restart Argo CD after setting `exec.enabled`. On Kubernetes 1.31 and later the `get` privilege is enough to exec;
before 1.31 patch the `argocd-server` Role (namespaced install) or ClusterRole (cluster install) so it can exec into pods:
```yaml
- apiGroups: [""]
  resources: [pods/exec]
  verbs: [create]
```

## RBAC
Exec is a separate RBAC resource (an application-specific policy), granted with the `create` action:
```csv
p, role:sre, exec, create, prod/*, allow
p, role:developer, exec, create, dev/*, allow
g, org:sre-team, role:sre
```
Format: `p, <role>, exec, create, <project>/<app>, allow`.

## Risks
- Exec lets the user run arbitrary code in any pod of an application they hold `exec/create` for. If the pod mounts a
  ServiceAccount token (the Kubernetes default), the user effectively has that ServiceAccount's privileges.
- Restrict exec to break-glass roles; consider leaving it disabled in prod and enabled in dev.

## Verify
- [ ] An SRE sees the Terminal tab; a developer in prod gets "permission denied".

## Checked

Argo CD documentation, master branch (latest release v3.5.6), repository argoproj/argo-cd, last commit 2026-10-24. Checked 2026-10-25. Confirmed: `exec.enabled` and `exec.shells` in `argocd-cm`, default shell order, introduction in v2.4, Kubernetes 1.31 `pods/exec` permission note, `exec` RBAC resource with `create` action, risk statement. Removed unconfirmed audit-log and websocket claims.

Method: documentation only; no commands were run.
