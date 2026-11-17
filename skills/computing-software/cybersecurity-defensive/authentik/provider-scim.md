---
id: computing-software.cybersecurity-defensive.authentik.provider-scim
name: provider-scim
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, scim-provider, provisioning, backchannel, compatibility-mode, property-mappings]
level: advanced
status: docs-checked
description: "Reference for the authentik SCIM provider: auth modes, sync schedule, attribute mapping and SkipObject, scope filtering, compatibility modes and capabilities."
sources:
  - https://docs.goauthentik.io/add-secure-apps/providers/scim/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: push users and groups from authentik to another application over SCIM 2.0. Needs a SCIM base URL (usually ending in `/v2`) reachable from authentik and an auth credential. SCIM providers are always backchannel providers beside the main SSO provider of an application.

## Authentication
**Static token** (default) or **OAuth token** (Enterprise; needs an OAuth source; silent or interactive, extra parameters like `grant_type: client_credentials`).

## Sync
Changes sync on create, modify and delete; a full sync of all SCIM providers runs hourly in the worker, one task per batch of 100 objects. Mappings apply in name order and are deeply merged; the result is validated against SCIM and a failing mapping stops the sync.

Custom schema extension: return the URN in `schemas` and an object under it.
```python
CUSTOM_SCHEMA = "urn:ietf:params:scim:schemas:extension:custom:2.0:User"

return {
    "schemas": [CUSTOM_SCHEMA],
    "phoneNumbers": [{"primary": True, "value": request.user.attributes.get("phone", ""), "type": "work"}],
    CUSTOM_SCHEMA: {"github": request.user.attributes.get("github", "")},
}
```
Raise `SkipObject` in a mapping to skip a user or group.

## Scope
Users: only those bound to the application are synced (all users if none bound); unbinding deprovisions on the next sync; **Exclude service accounts** is available. Group filters limit groups only; changing them does not remove previously synced groups.

## Compatibility modes
Default, AWS (no PATCH), Slack (filtering), Salesforce (`/ServiceProviderConfigs`), GitLab, vCenter (skip `ServiceProviderConfig`), Webex. `ServiceProviderConfig` is cached 1 hour, cleared when the provider is updated. PATCH is used only for group membership changes when supported; other updates use PUT. Default `externalId` matches the OIDC hashed-ID subject and the SAML persistent NameID.

## Checked
2026-11-03. Every remaining option, endpoint, value and example was read against the authentik documentation page https://docs.goauthentik.io/add-secure-apps/providers/scim/.
Removed as not confirmed by that page: Basic authentication mode and HTTP 409 conflict handling.
Method: documentation only; no commands were run.
