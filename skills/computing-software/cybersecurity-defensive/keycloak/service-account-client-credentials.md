---
id: computing-software.cybersecurity-defensive.keycloak.service-account-client-credentials
name: service-account-client-credentials
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, service-account, client-credentials, grant-type, token-endpoint]
level: practitioner
status: docs-checked
description: "Obtain access tokens for a service account with the client_credentials grant and understand which roles end up in the token."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/clients/oidc/proc-using-a-service-account.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# service account client credentials
A client with a service account can obtain tokens for machine-to-machine calls. Enable it: *Clients* > your client > *Settings*, toggle *Client authentication* On, tick *Service account roles*, save, and configure client credentials. Then open the *Client Scopes* tab, the dedicated client scope and its *Scope* tab to verify the client role scope mappings include the roles the service account needs (the docs say not to enable *Full Scope Allowed*, which is deprecated; configure role scope mappings explicitly), and use the client's *Service Account Roles* tab to configure the roles available to the service account.

Roles in the resulting token are the intersection of (1) the client's role scope mappings combined with those inherited from linked client scopes and (2) the service account roles.

Token request: POST to `/realms/<realm>/protocol/openid-connect/token` with the client credentials and `grant_type=client_credentials`. By default credentials are the client id and secret in an `Authorization: Basic` header, but a signed JWT assertion or a custom mechanism can be used, and `client_id` / `client_secret` can be sent as POST parameters instead.
```
POST /realms/demo/protocol/openid-connect/token
Authorization: Basic cHJvZHVjdC1zYS1jbGllbnQ6cGFzc3dvcmQ=
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
```
The header value is the Base64 of `clientId:clientSecret`; the example (`product-sa-client` / `password`) was produced with `echo 'product-sa-client:password' | base64`. The response is an OAuth 2.0 Access Token Response (`access_token`, `token_type`, `expires_in`, `scope`).

## Checked
2026-11-03. Confirmed against server_admin/topics/clients/oidc/proc-using-a-service-account.adoc. Fixed: `echo` without `-n` as on the page, the checkbox name, and the Full Scope statement (page says do not enable it). Removed: the gotchas and decode/introspect Verify step.
Method: documentation only; no commands were run.
