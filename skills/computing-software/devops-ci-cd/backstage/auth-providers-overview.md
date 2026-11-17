---
id: computing-software.devops-ci-cd.backstage.auth-providers-overview
name: auth-providers-overview
category: computing-software
field: devops-ci-cd
product: backstage
tags: [authentication, auth-providers, sign-in-page, backstage]
level: intro
status: docs-checked
description: "Understand Backstage authentication: sign-in versus delegated access and the built-in provider list."
sources:
  - https://backstage.io/docs/auth/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Authentication in Backstage serves two purposes: signing users in and identifying them, and delegating access to third-party resources on their behalf.

The core library lists these built-in providers: Auth0, Atlassian, Azure, Azure Easy Auth, Bitbucket, Bitbucket Server, Cloudflare Access, GitHub, GitLab, Google, Google IAP, Keycloak (community-maintained), Okta, OAuth 2 Custom Proxy, OneLogin, OpenShift and VMware Cloud. Proxy providers (Amazon Application Load Balancer, Azure EasyAuth, Cloudflare Access, Google IAP, OAuth2 Proxy) use `ProxiedSignInPage` instead of an interactive sign-in page. Generic OAuth2 and SAML providers also exist for custom providers.

Setup always has three parts:

1. Install the provider module in the backend.
2. Configure the provider under `auth.providers.<name>.<environment>` in `app-config.yaml`.
3. Add the provider to the frontend sign-in page.

```ts
backend.add(import('@backstage/plugin-auth-backend'));
backend.add(import('@backstage/plugin-auth-backend-module-github-provider'));
```

```yaml
auth:
  environment: development
  providers:
    github:
      development:
        clientId: ${AUTH_GITHUB_CLIENT_ID}
        clientSecret: ${AUTH_GITHUB_CLIENT_SECRET}
```

`auth.environment` selects which environment block is used, so keep `development` and `production` credentials separate.

Identity management and the sign-in page block external access only with the new backend system, as long as `backend.auth.dangerouslyDisableDefaultAuthPolicy` is not set. A provider that signs a user in needs a sign-in resolver, covered separately, to map the external account to a catalog User entity.

## Checked

2026-11-03. Confirmed against the Backstage Authentication overview page: the two purposes, the provider list, the per-environment config block, `auth.environment` selection, the SignInPage requirement and the `dangerouslyDisableDefaultAuthPolicy` note. Removed: AWS ALB and generic OIDC from the built-in list (the page lists them differently).

Method: documentation only; no commands were run.
