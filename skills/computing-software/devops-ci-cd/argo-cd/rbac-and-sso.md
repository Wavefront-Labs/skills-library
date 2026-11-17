---
id: computing-software.devops-ci-cd.argo-cd.rbac-and-sso
name: rbac-and-sso
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, argocd, argocd-rbac, rbac, policy-csv, argocd-rbac-cm, policy-default, scopes, groups-claim, sso, argocd-sso, dex, dex-connectors, oidc-config, oidc, okta, entra-id, azure-ad, github-sso, gitlab-sso, project-roles, appproject-roles, jwt-tokens, argocd-proj-role, local-users, argocd-cm-accounts, api-keys, apikey-capability, admin-disable, policy-matchmode, glob-vs-regex, rbac-validation, argocd-admin-settings-rbac, applications-in-any-namespace]
level: advanced
status: docs-checked
description: "Lock Argo CD down: SSO via Dex or direct OIDC with group claims, argocd-rbac-cm policy.csv roles, AppProject roles with JWT tokens for CI, local accounts, policy tests."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/rbac/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/user-management/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/user-management/microsoft/", "https://argo-cd.readthedocs.io/en/stable/user-guide/projects/#project-roles"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RBAC and SSO

**Goal:** humans log in with the IdP, their group decides what they can sync, CI uses
scoped project tokens, and the built-in `admin` is disabled.

## 1. SSO: Dex vs direct OIDC
Dex (bundled) federates non-OIDC sources (GitHub, GitLab, LDAP, SAML, Microsoft):
```yaml
# argocd-cm
data:
  url: https://argocd.example.com
  dex.config: |
    connectors:
      - type: github
        id: github
        name: GitHub
        config:
          clientID: $dex.github.clientID            # $name → key in argocd-secret
          clientSecret: $dex.github.clientSecret
          orgs: [{ name: example-org }]              # restrict logins to these GitHub orgs
```
Direct OIDC (Okta, Entra ID, Keycloak, Google) skips Dex:
```yaml
  oidc.config: |
    name: Okta
    issuer: https://example.okta.com
    clientID: $oidc.okta.clientID
    clientSecret: $oidc.okta.clientSecret
    requestedScopes: [openid, profile, email, groups]
    requestedIDTokenClaims: { groups: { essential: true } }
    # enablePKCEAuthentication: true   # PKCE, see the User Management page
```
Group claims are the whole game: not every OIDC provider returns groups by default (Okta,
OneLogin and Microsoft support a `groups` scope); others can be asked with
`requestedIDTokenClaims`, and some (Okta) return groups only on the user info endpoint. Entra ID
ID tokens carry at most 200 groups: for more, set `enableUserGroupOverageClaim: true`
(Microsoft page). Redirect URI: `https://argocd.example.com/auth/callback` (direct)
or `/api/dex/callback` (Dex). CLI login: `argocd login argocd.example.com --sso`.

## 2. RBAC policy (argocd-rbac-cm)
```yaml
data:
  policy.default: role:readonly          # or '' for deny-all to unknown users
  scopes: '[groups, email]'              # OIDC scopes examined by RBAC (defaults to [groups])
  policy.matchMode: glob                 # glob | regex
  policy.csv: |
    # p, <subject>, <resource>, <action>, <object>, <effect>
    p, role:team-a-dev,  applications, get,      team-a/*, allow
    p, role:team-a-dev,  applications, sync,     team-a/*, allow
    p, role:team-a-dev,  applications, action/*, team-a/*, allow      # UI actions (restart, promote)
    p, role:team-a-dev,  logs,         get,      team-a/*, allow
    p, role:team-a-dev,  exec,         create,   team-a/*, deny
    p, role:team-a-lead, applications, *,        team-a/*, allow
    p, role:team-a-lead, repositories, get,      *,        allow
    p, role:platform,    *,            *,        *,        allow
    g, example-org:team-a,       role:team-a-dev
    g, example-org:team-a-leads, role:team-a-lead
    g, example-org:platform,     role:platform
```
Resources: `applications`, `applicationsets`, `clusters`, `projects`, `repositories`,
`certificates`, `accounts`, `gpgkeys`, `logs`, `exec`, `extensions`. Actions: `get`,
`create`, `update`, `delete`, `sync`, `override`, `action/<group>/<kind>/<action-name>`
(`action//Pod/name` for the core group), and fine-grained `update/*` and `delete/*` sub-resource forms. Object for
applications is `<project>/<app-name>` (`<project>/<namespace>/<app>` with apps-in-any-namespace).
Extra `policy.<name>.csv` keys are concatenated in order after `policy.csv`. Groups need a `g` role assignment
before their `p` policies count. `logs, get` is what lets users see pod logs; `exec, create` is exec.

Validate before applying:
```bash
argocd admin settings rbac validate --policy-file policy.csv
argocd admin settings rbac can role:team-a-dev sync applications 'team-a/web' --policy-file policy.csv
argocd admin settings rbac can role:team-a-dev delete applications 'team-b/web' --policy-file policy.csv   # expect no
```

## 3. Project roles for CI (no human login)
```yaml
kind: AppProject
metadata: { name: team-a }
spec:
  roles:
    - name: ci-sync
      policies:
        - p, proj:team-a:ci-sync, applications, sync, team-a/*, allow
        - p, proj:team-a:ci-sync, applications, get,  team-a/*, allow
      groups: []                     # optional SSO groups also getting this role
```
`argocd proj role create-token team-a ci-sync -e 10m` → JWT (`-e` sets expiry); CI passes it with
`--auth-token $TOKEN`. The token is bounded by the project role's policies. Prefer the
CI-pushes-Git + Argo-auto-syncs model; tokens are for `app wait`/`app sync` in gates.

## 4. Local accounts and admin
```yaml
# argocd-cm
  admin.enabled: "false"            # once SSO + a platform role work
  accounts.ci-readonly: apiKey      # capabilities: login, apiKey
  accounts.ci-readonly.enabled: "true"
```
`argocd account generate-token --account ci-readonly` creates API keys; grant via
`g, ci-readonly, role:readonly`. Passwords for local accounts:
`argocd account update-password --account <name>`. Store `argocd-secret` entries
(`admin.password`, OIDC secrets) via ESO/SOPS; **never** commit `argocd-secret` plain.

## 5. Gotchas
- Authenticated users get `policy.default`; with anonymous access enabled, unauthenticated
  users get it too, so use a dedicated default such as `role:unauthenticated` there.
- Groups come from the claims in the configured `scopes`; a scope named after an SCM org
  can collide with a local user of the same name if users can create orgs.
- Apps-in-any-namespace changes object strings to `project/namespace/app`.
- SSO logout can call the provider via `oidc.config.logoutURL`.

## Checked
2026-10-31. Confirmed against the Argo CD RBAC, User Management, Microsoft and Projects pages: policy syntax, resource and action table, matchMode, scopes, extra policy keys, callback paths, claims options, 200-group Entra overflow, local-account settings, project role tokens, logoutURL. Removed: version gates, Deny-precedence and logs-since claims, `can-i`, `get-user-info`, `/user-info`, `--sso-port`, `exec.enabled`, session duration default, Okta/Entra claim-config advice, token listing and header claims.
Method: documentation only; no commands were run.

## Verify
- [ ] SSO login lands with the expected groups in the token.
- [ ] `rbac can` tests pass for allow and deny cases and run in CI on the policy file.
- [ ] A CI token can sync only its project's apps and expires.
- [ ] `admin.enabled: "false"`; `policy.default` is deliberate.
