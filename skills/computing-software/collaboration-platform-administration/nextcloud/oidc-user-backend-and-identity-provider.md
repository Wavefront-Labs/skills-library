---
id: computing-software.collaboration-platform-administration.nextcloud.oidc-user-backend-and-identity-provider
name: oidc-user-backend-and-identity-provider
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [oidc, user-oidc, single-sign-on, bearer-token, identity-provider]
level: advanced
status: draft
description: "Use the user_oidc app to log in with an external OpenID Connect provider, the oidc app to make Nextcloud a provider, and the bearer validation flag."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_user/user_auth_oidc.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: pick the right OpenID Connect app for the direction of trust.

Nextcloud as relying party (users log in elsewhere): install the OpenID Connect user backend app, `user_oidc`. It lets users authenticate through external OIDC identity providers. It can optionally also provision users, creating them at first connection, or it can rely on other user backends and handle only authentication.

Nextcloud as identity provider: install the community app `oidc` (OIDC Identity Provider). It allows any Nextcloud user, from any user backend, to authenticate in an OIDC login flow. Use it when Nextcloud should be the authority for authentication and profile data across several services.

Bearer tokens for API requests: Nextcloud can accept OIDC ID tokens and access tokens as bearer tokens.
- External provider: only `user_oidc` is needed.
- Nextcloud as provider: you need `oidc` to be the provider and also `user_oidc` to validate API request authentication. In `user_oidc`, set the config flag `oidc_provider_bearer_validation` to true so it asks the `oidc` app to validate received tokens.

Choose:
1. Existing company identity provider: `user_oidc` only.
2. Nextcloud is the master directory: add `oidc`.

Detailed options, including provisioning and token validation, are in each app's README on GitHub; this admin page only covers the roles.

Check: a login through the provider lands on a Nextcloud account, and a test API call with a bearer token is accepted.
