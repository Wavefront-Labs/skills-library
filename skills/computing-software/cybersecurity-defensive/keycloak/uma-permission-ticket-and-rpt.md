---
id: computing-software.cybersecurity-defensive.keycloak.uma-permission-ticket-and-rpt
name: uma-permission-ticket-and-rpt
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, uma, permission-ticket, rpt, uma-ticket-grant]
level: practitioner
status: docs-checked
description: "Obtain a requesting party token (RPT) from Keycloak with the uma-ticket grant using a permission ticket or direct resource#scope permission."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/authorization_services/topics/service-authorization-obtaining-permission.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uma permission ticket and rpt
Clients ask the token endpoint for permissions with the UMA grant. Keycloak evaluates all policies associated with the requested resources and scopes and issues a Requesting Party Token (RPT) holding the permissions granted.

Request parameters (all optional except `grant_type`):
- `grant_type` (required): `urn:ietf:params:oauth:grant-type:uma-ticket`.
- `ticket`: the most recent permission ticket from the UMA authorization process.
- `permission`: `RESOURCE_ID#SCOPE_ID`, repeatable, an extension that allows requests without a ticket (examples on the page: `Resource A#Scope A`, `Resource A#Scope A, Scope B, Scope C`, `Resource A`, `#Scope A`).
- `audience`: client id of the resource server; mandatory when `permission` is defined.
- `claim_token` with `claim_token_format` (`urn:ietf:params:oauth:token-type:jwt` for an access token, or the OIDC ID token format `https://openid.net/specs/openid-connect-core-1_0.html#IDToken`) to push extra claims into evaluation.
- `rpt`: a previously issued RPT whose permissions are evaluated and added to the new one (incremental authorization).
- `permission_resource_format` (`id` default, or `uri`), `permission_resource_matching_uri` (default false), `response_include_resource_name`, `response_permissions_limit`, `submit_request` (only with `ticket`) and `response_mode` (`decision` returns `{"result": true}`, or a 403 if nothing maps; `permissions` returns the granted permissions).

Example request (access token in the `Authorization` header):
```
curl -X POST http://localhost:8080/realms/hello/protocol/openid-connect/token \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  --data "grant_type=urn:ietf:params:oauth:grant-type:uma-ticket" \
  --data "audience=my-resource-server" --data "permission=Resource A#Scope A"
```

## Checked
2026-11-03. Confirmed against authorization_services/topics/service-authorization-obtaining-permission.adoc: every parameter, default and `response_mode` value above. Removed (not on that page): the claim that the policy enforcer answers 401 with a ticket, that an RPT is bound to evaluation time, that a non-resource-server audience fails, the `authorization.permissions` Verify step. The curl example follows the page's `Authorization: Bearer` pattern.
Method: documentation only; no commands were run.
