---
id: computing-software.cloud-infrastructure-engineering.kubernetes.argocd-appprojects-rbac-and-sso
name: argocd-appprojects-rbac-and-sso
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, argocd, appproject, argocd-rbac, argocd-sso, oidc, gitops, multi-tenancy]
level: advanced
status: docs-checked
description: "Make Argo CD safe for many teams: AppProjects restricting repos, destinations and kinds, policy.csv RBAC mapped to SSO groups via OIDC or Dex, and testing policies offline."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/projects/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/rbac/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/user-management/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Argo CD AppProjects, RBAC and SSO

Argo CD runs with cluster-admin-like rights. Without projects and RBAC, anyone who can
create an Application can deploy anything anywhere.

## AppProject per team
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata: {name: payments, namespace: argocd}
spec:
  description: Payments team
  sourceRepos: ["https://github.com/acme/payments-*"]
  destinations:
  - {server: https://kubernetes.default.svc, namespace: "payments-*"}
  clusterResourceWhitelist:                         # only these cluster-scoped objects
  - {group: "", kind: Namespace, name: "payments-*"}
  namespaceResourceBlacklist:
  - {group: "", kind: ResourceQuota}
  - {group: "", kind: LimitRange}
  - {group: networking.k8s.io, kind: NetworkPolicy}
  sourceNamespaces: [payments-apps]                 # apps-in-any-namespace
  roles:
  - name: ci
    policies: ["p, proj:payments:ci, applications, sync, payments/*, allow"]
  syncWindows:
  - {kind: deny, schedule: "0 22 * * 5", duration: 60h, applications: ["*"], manualSync: true}
```
Lock the built-in `default` project (empty `sourceRepos`/`destinations`) so nothing lands there by accident.

## RBAC (argocd-rbac-cm)
```yaml
data:
  policy.default: role:readonly            # or "" to deny by default
  scopes: "[groups, email]"
  policy.csv: |
    p, role:payments-dev, applications, get,      payments/*, allow
    p, role:payments-dev, applications, sync,     payments/*, allow
    p, role:payments-dev, applications, action/*, payments/*, allow
    p, role:payments-dev, logs, get,              payments/*, allow
    p, role:payments-dev, exec, create,           payments/*, deny
    g, acme:payments-engineers, role:payments-dev
    g, acme:platform, role:admin
```
Format: `p, subject, resource, action, project/object, effect`. Effect is `allow` or `deny`.
Resources include `applications`, `applicationsets`, `projects`, `repositories`, `clusters`,
`logs`, `exec`. Everyone authenticated gets at least `policy.default`, and a `deny` rule cannot
take that back; keep the default minimal (the docs suggest a minimal `role:authenticated`).

## SSO
Direct OIDC (argocd-cm):
```yaml
data:
  url: https://argocd.example.com
  oidc.config: |
    name: Okta
    issuer: https://acme.okta.com
    clientID: argocd
    clientSecret: $oidc.okta.clientSecret     # key in argocd-secret
    requestedScopes: [openid, profile, email, groups]
```
Or bundled Dex (`dex.config` with connectors such as GitHub or OIDC) when you want Dex to broker
the login. Ensure the IdP actually puts `groups` in the token (the `scopes` key in
`argocd-rbac-cm` says which claims RBAC examines); missing group claims = users only get
`policy.default`. Disable the local admin after SSO works (`admin.enabled: "false"`).

## Test before applying
```bash
argocd admin settings rbac validate --policy-file policy.csv
argocd admin settings rbac can role:payments-dev sync applications 'payments/api' --policy-file policy.csv
argocd admin settings rbac can role:payments-dev sync applications 'billing/api' --policy-file policy.csv   # expected output: No (other project)
argocd account can-i sync applications 'payments/*'    # as the logged-in user
```

## Verify
- [ ] A team member cannot create an Application targeting another namespace or a
  cluster-scoped kind; sync of their own app works; `argocd account get-user-info` shows groups.

## Checked

Documentation release: Argo CD stable docs (argo-cd repo docs/, latest release v3.5.6, repo commit 2026-10-25).
Confirmed: AppProject fields (`sourceRepos`, `destinations`, `sourceNamespaces`, `clusterResourceWhitelist` with `name`, `namespaceResourceBlacklist`, `syncWindows` with `kind`, `schedule`, `duration`, `manualSync`, project roles named `proj:<project>:<role>`); the permissive built-in `default` project and how to lock it; RBAC policy syntax, `policy.default`, `scopes`, `exec` and `action/` resources; `oidc.config` with `requestedScopes`, `dex.config`, `admin.enabled: "false"`; the `argocd admin settings rbac can` and `argocd account can-i` commands.
Removed or corrected: "deny wins over allow" (docs say default-policy access cannot be blocked by deny), the empty-whitelist comment, and the claim that Dex is only for non-OIDC IdPs.

Method: documentation only; no commands were run.
