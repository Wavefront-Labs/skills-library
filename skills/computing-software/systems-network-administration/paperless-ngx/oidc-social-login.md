---
id: computing-software.systems-network-administration.paperless-ngx.oidc-social-login
name: oidc-social-login
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, oidc, openid-connect, social-login, allauth, paperless-socialaccount-providers]
level: advanced
status: docs-checked
description: "Add OpenID Connect or social login via django-allauth with PAPERLESS_APPS and PAPERLESS_SOCIALACCOUNT_PROVIDERS, including the v3 token_auth_method fix."
sources:
  - "https://docs.paperless-ngx.com/advanced_usage/"
  - "https://docs.paperless-ngx.com/migration-v3/"
  - "https://docs.paperless-ngx.com/usage/"
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/api/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenID Connect and social login

Paperless-ngx integrates other authentication systems through the django-allauth package. Two settings enable a provider: the Django application in `PAPERLESS_APPS` and its JSON config in `PAPERLESS_SOCIALACCOUNT_PROVIDERS`.

## GitHub example
```bash
PAPERLESS_APPS="allauth.socialaccount.providers.github"
PAPERLESS_SOCIALACCOUNT_PROVIDERS='{"github": {"APPS": [{"provider_id": "github","name": "Github","client_id": "<CLIENT_ID>","secret": "<CLIENT_SECRET>"}]}}'
```

## OIDC example (Keycloak)
```bash
PAPERLESS_APPS="allauth.socialaccount.providers.openid_connect"
PAPERLESS_SOCIALACCOUNT_PROVIDERS='{"openid_connect": {"APPS": [{"provider_id": "keycloak","name": "Keycloak","client_id": "paperless","secret": "<CLIENT_SECRET>","settings": {"server_url": "https://<KEYCLOAK_SERVER>/realms/<REALM>/.well-known/openid-configuration"}}]}}'
```
Provider-specific options are in the django-allauth documentation.

## Linking accounts
An existing user logs in with regular credentials, opens "My Profile" from the user dropdown and connects the social account. If sign-up is enabled (`PAPERLESS_SOCIALACCOUNT_ALLOW_SIGNUPS`, default true), signup options appear on the login page.

## v3 callback error
If OIDC login fails at the callback with an `invalid_client` error after upgrading to v3, add `token_auth_method` to the provider `settings`:
```json
"settings": {"server_url": "https://login.example.com", "token_auth_method": "client_secret_basic"}
```

## MFA
If the OIDC provider already enforces multi-factor authentication, `PAPERLESS_SOCIAL_ACCOUNT_MFA_TRUSTED_AMR` lists `amr` claim values that make Paperless skip its own two-factor prompt for those logins (default `mfa`). Only list values that mean a second factor was actually used.

Headless OIDC for apps uses allauth endpoints under `api/auth/`.

## Disabling regular login
`PAPERLESS_DISABLE_REGULAR_LOGIN` disables the frontend username and password login once SSO is set up; it does not disable the Django admin login or local-credential logins via the API. `PAPERLESS_REDIRECT_LOGIN_TO_SSO` redirects users to the first SSO provider login.

## Checked
Date: 2026-11-07
Pages read in full: advanced_usage, migration-v3, usage, configuration, api (docs/*.md).
Removed as unconfirmed: the redirect URI pattern `/accounts/<provider_id>/login/callback/`, the claim that a mismatched `PAPERLESS_URL` rejects the callback, and "keep the JSON on one line". Added the DISABLE_REGULAR_LOGIN caveats from configuration, and configuration and api to sources.
Method: documentation only; no commands were run.
