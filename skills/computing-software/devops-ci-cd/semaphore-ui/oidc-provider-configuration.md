---
id: computing-software.devops-ci-cd.semaphore-ui.oidc-provider-configuration
name: oidc-provider-configuration
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [oidc, openid-connect, sso, oidc-providers, authentication, semaphore-ui]
level: practitioner
status: docs-checked
description: "Configure OpenID Connect providers in oidc_providers or SEMAPHORE_OIDC_PROVIDERS, with claim expressions and options."
sources:
  - https://semaphoreui.com/docs/admin-guide/authentication/openid
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# OpenID Connect providers

Goal: add single sign-on through an OIDC identity provider.

```json
{
  "oidc_providers": {
    "mysso": {
      "display_name": "Sign in with MySSO",
      "color": "orange",
      "icon": "login",
      "provider_url": "https://mysso-provider.com",
      "client_id": "***",
      "client_secret": "***",
      "redirect_url": "https://your-domain.com/api/auth/oidc/mysso/redirect"
    }
  }
}
```

In containers set one variable holding the same JSON: `SEMAPHORE_OIDC_PROVIDERS='{"github": {"client_id": "***", "client_secret": "***"}}'`.

In the page's examples `redirect_url` has the form `https://your-domain.com/api/auth/oidc/<provider-key>/redirect`, where the key is the name under `oidc_providers` (for example `mysso`).

Other options: `scopes`, `username_claim`, `email_claim`, `name_claim` (claim expressions), `groups_claim`, `order` (button position), `client_id_file` / `client_secret_file` (lower priority than the inline values), `allow_idp_initiated` (default false), `return_via_state` (default true), and `endpoint.issuer`, `endpoint.auth`, `endpoint.token`, `endpoint.userinfo`, `endpoint.jwks`, `endpoint.algorithms` (the page lists these without a description).

Claim expressions: `email | {{ .username }}@your-domain.com` falls back to the right side when the claim is empty. `"username_claim": "|"` generates a random username per login.

Enterprise only: `groups_claim` plus group mappings assign project roles from IdP groups; the groups must be in the ID token (some providers need the `groups` scope).

Verify: the login page shows an additional login button for each configured provider.

## Checked

2026-11-07. Read in full: the OpenID Connect page, from its markdown source in the semaphore-docs repository (admin-guide/authentication/openid.md; it includes no snippet files). Confirmed against it: the example provider block, the SEMAPHORE_OIDC_PROVIDERS container form, every option named above and the two defaults, the claim expression fallback and the random-username expression, and the Enterprise group mappings note with the groups scope remark. Removed: the claim that the endpoint options are for providers without discovery, the instruction to register the redirect path exactly, and an unsourced test-user Verify step.
Method: documentation only; no commands were run.
