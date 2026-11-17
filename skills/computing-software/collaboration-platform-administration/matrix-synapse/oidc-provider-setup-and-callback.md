---
id: computing-software.collaboration-platform-administration.matrix-synapse.oidc-provider-setup-and-callback
name: oidc-provider-setup-and-callback
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, oidc, openid-connect, sso, oidc-providers, authlib, callback, public-baseurl, backchannel-logout]
level: advanced
status: docs-checked
description: "Wire Synapse to an OpenID Connect provider: authlib install, oidc_providers entry, the /_synapse/client/oidc/callback redirect URI, back-channel logout."
sources:
  - https://element-hq.github.io/synapse/latest/openid.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Synapse can authenticate against an OpenID Connect provider (OP) instead of its local password database. Any OP that supports the authorization code flow should work. The docs name Hydra and Dex for local testing (an OP must be served under HTTPS; a self-signed CA works if you start Synapse with `SSL_CERT_FILE` pointing at it) and Google and Auth0 as tested SaaS options. Plain OAuth2 providers that offer the authorization code grant, such as GitHub, may also work.

Dependencies: the Docker images and matrix.org Debian packages already include the `authlib` library. In a virtualenv install it with pip using the `matrix-synapse[oidc]` extra.

Then add an entry to `oidc_providers` in the config. Every provider's redirect (callback) URI is:

```
[synapse public baseurl]/_synapse/client/oidc/callback
```

Register exactly that at the provider. For setups using `.well-known` delegation, set `public_baseurl` correctly, because if unset Synapse defaults to `https://<server_name>/` and uses that to build the callback URL.

The sample shape in the docs for a provider carries `idp_id`, `idp_name`, `issuer`, `client_id`, `client_secret`, `scopes`, and a `user_mapping_provider.config` block with `localpart_template` and `display_name_template`. Optional `idp_brand` is a styling hint for clients, and `discover: true` uses OIDC discovery.

**Back-channel logout.** Synapse can receive OpenID Connect Back-Channel Logout notices so that logging out at the OP ends the user's Synapse session. Set `backchannel_logout_enabled: true` on the provider and register this URL as the destination at the OP:

```
[synapse public baseurl]/_synapse/client/oidc/backchannel_logout
```

Provider-specific quirks are in the sample configs skill. Attribute mapping is covered in the mapping provider skill.

## Checked

Method: docs-checked 2026-11-09 against docs/openid.md (Synapse develop branch, raw markdown, read in full).
