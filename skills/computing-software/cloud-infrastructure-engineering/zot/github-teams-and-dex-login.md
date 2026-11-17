---
id: computing-software.cloud-infrastructure-engineering.zot.github-teams-and-dex-login
name: github-teams-and-dex-login
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, github-teams, github-enterprise, dex-oidc, claim-mapping-username, read-org-scope]
level: advanced
status: docs-checked
description: "Use GitHub teams as Zot groups with the read:org scope, point Zot at GitHub Enterprise endpoints, and register Zot as a dex static client."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/authn-authz.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
GitHub teams: with the `read:org` scope, teams appear as `<org>/<team-slug>` and can be used in policy `groups`:

```json
"infra/**": { "policies": [ { "groups": ["MyOrg/platform-team"], "actions": ["read", "create", "update"] } ] }
```

Without the scope Zot still authenticates, but team groups may be missing.

GitHub Enterprise: set custom endpoints and optionally map the username claim:

```json
"github": { "clientid": "<client_id>", "clientsecret": "<client_secret>",
  "authurl": "https://github.company.com/login/oauth/authorize",
  "tokenurl": "https://github.company.com/login/oauth/access_token",
  "scopes": ["read:org", "user", "repo"],
  "claimMapping": { "username": "preferred_username" } }
```

dex:
1. Register Zot as a dex `staticClients` entry with redirect URI `http://zot.example.com:8080/zot/auth/callback/oidc`.
2. Configure the `oidc` provider with `issuer` (for example `http://<zot-server>:5556/dex`) and scopes `openid`, `profile`, `email`, `groups`.
3. Log in via `http://zot.example.com:8080/auth/login?provider=oidc`.

## Checked

2026-11-04. Read against the zot authn-authz article (GitHub teams, GitHub Enterprise, dex sections); every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
