---
id: computing-software.devops-ci-cd.spinnaker.fiat-github-teams-role-provider
name: fiat-github-teams-role-provider
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [fiat, authorization, github-teams, role-provider, github-app, personal-access-token]
level: practitioner
status: docs-checked
description: "Use GitHub organization teams as Fiat roles: GitHub App or read:org token, and the fiat-local.yml group-membership github block with authMethod AUTO, GITHUB_APP or PAT."
sources:
  - https://spinnaker.io/docs/setup/other_config/security/authorization/github-teams/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
With the GitHub Teams provider, roles are mapped from the teams under one configured GitHub organization.

**GitHub App (recommended; the page says available in releases after 2025.4.0).** Advantages over a PAT: a 15,000 requests per hour rate limit versus 5,000, short-lived auto-refreshed tokens, and granular permissions. As an org admin: Organization Settings, Developer settings, GitHub Apps, New GitHub App; untick webhook Active; grant Organization Permissions, Members: Read-only; create it and note the App ID; generate and save a private key `.pem`; install the app at organization level (not per repo) and note the Installation ID from the install URL. Installation tokens last 1 hour and Fiat caches them in memory, never on disk.

**PAT (legacy, lower rate limits).** From an administrator's account generate a token with the `read:org` scope (the page suggests naming it "spinnaker-fiat"). PATs are stored in Fiat configuration, so rotate them like any long-lived secret.

**Configure Fiat** in `fiat-local.yml`:

```yaml
auth:
  group-membership:
    service: github
    github:
      membershipCacheTTLSeconds: 600
      membershipCacheTeamsSize: 1000
      paginationValue: 100
      authMethod: AUTO
      baseUrl: https://api.github.com/
      organization: my-org
      accessToken: <PAT>
      appId: <app id>
      installationId: <installation id>
      privateKeyPath: encryptedFile:orVolumePath
```

`authMethod`: `AUTO` (default) prefers the GitHub App when app id, installation id and private key path are set and falls back to the PAT; `GITHUB_APP` forces the app and fails if credentials are missing or invalid; `PAT` forces the token and fails if `accessToken` is missing. The page shows `membershipCacheTTLSeconds` as when to refresh group info and `paginationValue` as defaulting to 100.

## Checked

2026-11-04. Confirmed against the GitHub Teams page. Removed: the `hal config security authz github` commands, the account-permission flag example and the Gate identity/Front50 prerequisites (not on this page).

Method: documentation only; no commands were run.
