---
id: computing-software.cybersecurity-defensive.authentik.oauth2-machine-to-machine
name: oauth2-machine-to-machine
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, client-credentials, m2m, app-password, jwt-federation, service-accounts]
level: advanced
status: docs-checked
description: "Machine-to-machine auth with the authentik OAuth2 provider: client_credentials with username and app password, auto service accounts, and federated JWT or Kubernetes tokens."
sources:
  - https://docs.goauthentik.io/add-secure-apps/providers/oauth2/machine_to_machine/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: obtain a signed JWT without a user. authentik identifies machine clients by username and authenticates by app password, because a provider holds only one client secret. `grant_type=password` is treated like `client_credentials`.

## Static request
```http
POST /application/o/token/ HTTP/1.1
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&client_id=<client_id>&username=<username>&password=<app_password>&scope=profile
```
Or pass `client_secret=<base64(username:token)>`. To get custom claims, select the scope mappings on the provider and request their names in `scope` (for example `profile custom-scope`). Passing the provider's own `client_secret` auto-creates a service account named `ak-<provider_name>-client_credentials` (settings cannot be changed).

## JWT authentication
authentik makes a service account from the provider name and the token's `sub`; accounts expire by the token's `exp`.
- External JWT: define a JWKS URL or raw JWKS in an OAuth Source, then select it under **Federated OIDC Sources** on the provider. Send `client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer`, `client_assertion=<inputJWT>`, `client_id`; or put the JWT in `client_secret`.
- Kubernetes projected service account tokens: create a generic OAuth Source with the issuer's `.well-known/openid-configuration` or JWKS URL, add it to Federated OIDC Sources, send the token as `client_assertion`. Carry claims with an OAuth Source property mapping returning `{"attributes": {"kubernetes_namespace": info.get("kubernetes.io", {}).get("namespace")}}` and an OAuth2 scope mapping returning `request.user.attributes.get("kubernetes_namespace")`.
- authentik-issued JWT: add the issuing providers under **Federated OAuth2/OpenID Providers**; tokens must be unexpired and unrevoked.

Limit access by claims with an expression policy: `return request.context["oauth_jwt"]["iss"] == "https://my.issuer"`. Also available: `oauth_scopes`, `oauth_grant_type`, `oauth_code_verifier`.

## Troubleshooting
Errors show only a generic message and `request_id`; search the server container logs for that id. Introspection needs a confidential provider. Events are logged as logins: method `token`, `oauth_client_secret` or `JWT`.

## Checked
2026-11-03. Every remaining option, endpoint, value and example was read against the authentik documentation page https://docs.goauthentik.io/add-secure-apps/providers/oauth2/machine_to_machine/.
Nothing was removed.
Method: documentation only; no commands were run.
