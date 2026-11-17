---
id: computing-software.cybersecurity-defensive.keycloak.uma-protection-api-permission-tickets
name: uma-protection-api-permission-tickets
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, protection-api, permission-ticket, pat, resource-owner]
level: practitioner
status: docs-checked
description: "Understand the Keycloak Protection API permission endpoint where resource servers get permission tickets for UMA clients."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/authorization_services/topics/service-protection-permission-api-papi.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uma protection api permission tickets
Resource servers using the UMA protocol use the permission endpoint of the Protection API to register permission requests and obtain a permission ticket:
```
http://${host}:${port}/realms/${realm-name}/authz/protection/permission
```
A permission ticket is a special token type representing a permission request; per the UMA specification it is a correlation handle conveyed from the authorization server to the resource server, to the client and back to the authorization server so it can assess the correct policies. In most cases you do not call this endpoint yourself: Keycloak's policy enforcer obtains the ticket when a client tries to access a protected resource without the necessary grants, returns it to the client, and enforces decisions on the final RPT. Tickets are obtained by resource servers, not regular client applications.

Create a ticket with a POST authorised with the Protection API token (`$pat`):
```
curl -X POST http://${host}:${port}/realms/${realm-name}/authz/protection/permission \
  -H 'Authorization: Bearer '$pat -H 'Content-Type: application/json' \
  -d '[{"resource_id": "{resource_id}", "resource_scopes": ["view"], "claims": {"organization": ["acme"]}}]'
```
The optional `claims` are available to your policies when evaluating the permissions tied to the ticket.

Benefits listed by the docs: resource servers abstract resource data from clients, can register authorization requests in Keycloak for later workflows granting access on the resource owner's consent, and are decoupled from authorization servers. A ticket is opaque to clients.

## Checked
2026-11-03. Confirmed against authorization_services/topics/service-protection-permission-api-papi.adoc. Removed (not on the page in what was read): the `resource_set` and `uma-policy` path mention, the PAT, single-purpose and Remote Resource Management gotchas, and the `WWW-Authenticate` Verify step.
Method: documentation only; no commands were run.
