---
id: computing-software.devops-ci-cd.semaphore-ui.oidc-github-keycloak-examples
name: oidc-github-keycloak-examples
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [oidc, github, keycloak, sso, group-mapping, semaphore-ui]
level: practitioner
status: docs-checked
description: "Working oidc_providers snippets for Keycloak and GitHub, plus the Keycloak mapper for group claims."
sources:
  - https://semaphoreui.com/docs/admin-guide/authentication/openid/keycloak
  - https://semaphoreui.com/docs/admin-guide/authentication/openid/github
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# OIDC examples for Keycloak and GitHub

Goal: copy a proven provider block.

Keycloak (`provider_url` is the realm URL):

```json
{
  "oidc_providers": {
    "keycloak": {
      "display_name": "Sign in with keycloak",
      "provider_url": "https://keycloak.example.com/realms/master",
      "client_id": "***",
      "client_secret": "***",
      "redirect_url": "https://semaphore.example.com/api/auth/oidc/keycloak/redirect"
    }
  }
}
```

The GitHub page sets the endpoints explicitly (no `provider_url`):

```json
{
  "oidc_providers": {
    "github": {
      "icon": "github",
      "display_name": "Sign in with GitHub",
      "client_id": "***",
      "client_secret": "***",
      "redirect_url": "https://your-domain.com/api/auth/oidc/github/redirect",
      "endpoint": {
        "auth": "https://github.com/login/oauth/authorize",
        "token": "https://github.com/login/oauth/access_token",
        "userinfo": "https://api.github.com/user"
      },
      "scopes": ["read:user", "user:email"],
      "username_claim": "|"
    }
  }
}
```

The GitHub docs also set an `email_claim` expression with a fallback built from the user id; follow the full page for it.

Keycloak groups (Enterprise group mappings): in the client's dedicated scope add a mapper By configuration, choose Group Membership, set Token Claim Name to `groups` and enable Add to ID token. Full group path on sends paths such as `/devops` or `/platform/sre`, and the group mapping must then use the path; off sends only the name, such as `sre`. Then set `groups_claim` to `groups` in Semaphore. Do not add `groups` to `scopes`; Keycloak refuses a scope it does not know.

Other documented providers: Google, GitLab, Gitea, Authelia, Authentik, Okta, PingFederate, Azure, Zitadel, Pocket-ID.

Verify: sign in through the button and check the created user's name and email.

## Checked

2026-11-04: checked against the Keycloak and GitHub OpenID pages. Removed the unconfirmed no-discovery claim, added the full group path rule and the scopes warning, and added Gitea to the provider list.

Method: documentation only; no commands were run.
