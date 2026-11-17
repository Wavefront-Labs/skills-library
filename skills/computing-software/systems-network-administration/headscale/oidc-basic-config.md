---
id: computing-software.systems-network-administration.headscale.oidc-basic-config
name: oidc-basic-config
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, oidc, issuer, client-id, pkce, sso]
level: practitioner
status: docs-checked
description: "Configure OpenID Connect login for Headscale: issuer, client credentials, PKCE, the callback URL, and the one-provider limit."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/oidc.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/config-example.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OIDC basics

```yaml
oidc:
  issuer: "https://sso.example.com"
  client_id: "headscale"
  client_secret: "generated-secret"
  pkce:
    enabled: true
```

- Register the redirect URI with the provider: `https://headscale.example.com/oidc/callback`.
- PKCE is recommended and must be enabled in Headscale and at the identity provider; set the provider's challenge method to `S256` (the example config says `pkce.method` defaults to `S256`; `pkce.enabled` defaults to false).
- `client_secret_path` is an alternative to `client_secret` (mutually exclusive).
- `scope` defaults to `["openid", "profile", "email"]` and must include `openid`.
- `only_start_if_oidc_is_available` blocks startup until the provider is healthy.

## Gotchas

- Headscale supports one OIDC provider at a time.
- Registration approval can be delegated to the identity provider (register-web-auth).
- Profile updates from the provider are supported; OIDC groups cannot be used in policy.
- Node expiry can follow the token (node-expiry).
- Vendor-neutral OIDC with limited handling of provider quirks: see oidc-provider-notes.

## Verify

Log a client in with `tailscale up --login-server <YOUR_HEADSCALE_URL>`, complete the browser login, then check `headscale nodes list` and `headscale users list`.

## Checked

2026-11-04. Confirmed against the Headscale OIDC page (issuer, client ID and secret, callback URL, PKCE, single provider, claims, limitations), config-example.yaml (`client_secret_path`, `scope`, `only_start_if_oidc_is_available`, `pkce` defaults) and the registration page (delegating approval to OIDC).

Method: documentation only; no commands were run.
