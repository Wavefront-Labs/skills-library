---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.openid-connect-plugin
name: openid-connect-plugin
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, openid-connect, oidc, oauth2, bearer-only, authentication, plugin]
level: advanced
status: docs-checked
description: "Configure the APISIX openid-connect plugin: client_id, client_secret, discovery, bearer_only, scope, redirect_uri, introspection and the headers passed upstream."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/openid-connect.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# openid-connect plugin

Required: `client_id`, `client_secret` (stored encrypted), `discovery` (provider well-known URL; individually set endpoints override it).

Defaults:
- `bearer_only`: false; true requires a bearer token and starts no login flow.
- `scope`: `openid` (needed to get a `sub` claim).
- `realm`: `apisix`, used in `WWW-Authenticate` on 401.
- `redirect_uri`: unset; APISIX then appends `/.apisix/redirect` to the request URI. If set, use an absolute URL that is a sub-path of the route URI.
- `introspection_endpoint`: unset, so the discovery document's endpoint is used.
- `timeout` 3 seconds; `unauth_action` `auth`; `ssl_verify` true (changed from false in 3.16.0).
- Upstream headers: `set_access_token_header` true (`X-Access-Token`), `set_id_token_header` true (`X-ID-Token`, unsigned), `set_userinfo_header` true (`X-Userinfo`), `set_raw_id_token_header` false (`X-Raw-ID-Token`), `set_refresh_token_header` false (`X-Refresh-Token`).

Minimal authorization code flow; `session.secret` is required and must be at least 16 characters:

```json
{
  "openid-connect": {
    "client_id": "apisix",
    "client_secret": "<CLIENT_SECRET>",
    "discovery": "http://keycloak:8080/realms/master/.well-known/openid-configuration",
    "redirect_uri": "http://127.0.0.1:9080/api/v1/redirect",
    "session": { "secret": "<SESSION_SECRET>" }
  }
}
```

## Checked

2026-11-04. Confirmed against the APISIX openid-connect plugin page: required attributes, scope, realm, redirect_uri behaviour including the /.apisix/redirect fallback, introspection fallback, timeout, unauth_action, ssl_verify default change in 3.16.0, the upstream header toggles and defaults, session.secret minimum length. Nothing removed.

Method: documentation only; no commands were run.
