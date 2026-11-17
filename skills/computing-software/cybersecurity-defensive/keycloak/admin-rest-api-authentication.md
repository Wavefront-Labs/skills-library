---
id: computing-software.cybersecurity-defensive.keycloak.admin-rest-api-authentication
name: admin-rest-api-authentication
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, admin-rest-api, access-token, admin-cli, service-account]
level: practitioner
status: docs-checked
description: "Call the Keycloak Admin REST API with a bearer token from the admin-cli client or a service account instead of long-lived credentials."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_development/topics/admin-rest-api.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# admin rest api authentication
Every call to the Admin REST API needs an access token with the appropriate permissions (listed in the Server Administration Guide). Obtain one by enabling authentication for your application through Keycloak, or with a direct access grant.

Password grant with the built-in `admin-cli` client (the docs example assumes a user `admin` in the `master` realm):
```
curl -d "client_id=admin-cli" -d "username=admin" -d "password=<password>" -d "grant_type=password" \
  "http://localhost:8080/realms/master/protocol/openid-connect/token"
```
By default this token expires in 1 minute. Take `access_token` from the JSON result and send it in the `Authorization` header:
```
curl -H "Authorization: bearer <token>" "http://localhost:8080/admin/realms/master"
```
Service account (client credentials) per the docs:
1. The client belongs to the `master` realm, has *Client authentication* On and *Service account roles* enabled.
2. Assign it the `admin` realm role on the *Service accounts roles* tab.
3. Request a token with the client secret from the *Credentials* tab:
```
curl -d "client_id=<YOUR_CLIENT_ID>" -d "client_secret=<YOUR_CLIENT_SECRET>" -d "grant_type=client_credentials" \
  "http://localhost:8080/realms/master/protocol/openid-connect/token"
```
This avoids storing an admin user's password. The API reference is linked from the guide as the API docs.

## Checked
2026-11-03. Confirmed against server_development/topics/admin-rest-api.adoc: both curl flows, 1 minute expiry, service-account client settings and the `admin` role. Removed (not on the page): least-privilege `realm-management` advice, gotchas about password grants and masked secrets, `GET /admin/realms/<realm>` verify step.
Method: documentation only; no commands were run.
