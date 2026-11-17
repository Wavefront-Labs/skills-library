---
id: computing-software.cloud-infrastructure-engineering.zot.social-login-openid
name: social-login-openid
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, openid, oauth2, social-login, callback-ui, external-url]
level: practitioner
status: docs-checked
description: "Configure Zot OpenID/OAuth2 web login with GitHub, Google, GitLab or generic OIDC: credentials files, login and callback URLs, callback allowlist, externalUrl."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/authn-authz.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Providers under `http.auth.openid.providers`: `github`, `google`, `gitlab` and generic `oidc` (for example dex). Each takes a `credentialsFile`, `scopes`, and (except GitHub) an `issuer`.

Credentials file:

```json
{ "clientid": "<client_id>", "clientsecret": "<client_secret>" }
```

Flow:
- Login: `http://<zot-server>/auth/login?provider=<provider>&callback_ui=<path>`
- Callback: `http://<zot-server>/zot/auth/callback/<provider>`
- Google, GitHub and GitLab require `callback_ui`, a same-origin relative path. Absolute URLs are rejected unless allowlisted:
  ```json
  "openid": { "callbackAllowOrigins": ["https://ui.example.com", "http://localhost:3000"], "providers": { } }
  ```
- Since v2.1.23 providers initialise on first login; if discovery is unreachable the provider's endpoints return `503` and retry next time.
- Behind a proxy or load balancer set `http.externalUrl` (for example `https://zot.example.com`) so callbacks return to the public address.
- `discoveryurl` is a custom discovery location for browser login only (not `bearer.oidc`); the discovery document's `issuer` must still match the configured one.

Scopes for GitLab in the docs: `openid`, `read_api`, `read_user`, `profile`, `email`.

## Checked

2026-11-04. Read against the zot authn-authz article (social login section); every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
