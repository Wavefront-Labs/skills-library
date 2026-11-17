---
id: computing-software.collaboration-platform-administration.vikunja.oidc-provider-setup
name: oidc-provider-setup
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, openid-connect, oidc-provider-key, authurl-discovery, confidential-client, disable-local-auth]
level: practitioner
status: docs-checked
description: "Configure Vikunja OpenID Connect login: the confidential client, redirect URL, providers map in YAML or env vars, discovery via authurl, and disabling local auth."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/openid.mdx
  - https://raw.githubusercontent.com/go-vikunja/vikunja/main/config-raw.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vikunja uses the Authorization Code Flow. At the identity provider create a confidential client, note client ID and secret, whitelist Vikunja's redirect URL (`/auth/openid/<provider-id>`) and support the `openid profile email` scopes.

```
auth:
  openid:
    enabled: true
    providers:
      <provider-id>:
        name: <provider-name>
        authurl: <issuer url>
        clientid: <client-id>
        clientsecret: <client-secret>
        scope: openid profile email
```

`authurl` is used for OIDC Discovery (`<authurl>/.well-known/openid-configuration`), typically the issuer URL. Discovered endpoints override any you configure by hand.

Env vars: `VIKUNJA_AUTH_OPENID_ENABLED=true` and `VIKUNJA_AUTH_OPENID_PROVIDERS_<PROVIDER_ID>_NAME`, `_AUTHURL`, `_CLIENTID`, `_CLIENTSECRET`, `_SCOPE` (quote values with spaces). Per the config reference, put at least one provider key in a config file if you want to read the rest from env.

Other provider options: `logouturl`, `forceuserinfo`, `requireavailability`.

Version 1.0 changed `providers` from a list to a map keyed by provider ID; convert pre-1.0 configs.

To force SSO, set `auth.local.enabled: false`. Desktop client login needs redirects to `127.0.0.1` allowed.

## Checked

2026-11-04: checked against the OpenID page (configuring section, env var block, 1.0 migration) and config-raw.json (provider options, desktop note).

Method: documentation only; no commands were run.
