---
id: computing-software.cloud-infrastructure-engineering.azure.app-registration-optional-claims-and-token-configuration
name: app-registration-optional-claims-and-token-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, app-registrations, optional-claims, token-configuration, app-manifest, groups-claim, group-overage]
level: practitioner
status: docs-checked
description: "Shape Entra tokens for an app: optional claims, groups claim and the 200-group overage, access token version and manifest edits via portal, az and Graph."
sources: ["https://learn.microsoft.com/entra/identity-platform/optional-claims", "https://learn.microsoft.com/entra/identity-platform/reference-microsoft-graph-app-manifest", "https://learn.microsoft.com/security/zero-trust/develop/configure-tokens-group-claims-app-roles"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optional claims and token configuration

**Goal:** the ID/access token contains exactly the claims the app needs, in the format it expects.

## Optional claims
Portal: App registration > **Token configuration** > Add optional claim (ID / access / SAML).
```json
// claims.json
{ "idToken": [ { "name": "email" }, { "name": "family_name" } ],
  "accessToken": [ { "name": "ipaddr" }, { "name": "acct" } ],
  "saml2Token": [] }
```
```bash
az ad app update --id <appId> --optional-claims @claims.json
```

## Groups claim
- Token configuration > Add groups claim: including **Groups assigned to the
  application** (`ApplicationGroup`, keeps the list small). Emit as object ID, or sAMAccountName / on-prem SID for synced groups.
- Overage: more than **200** groups (JWT) -> token has `_claim_names`/`hasgroups` instead; the app must call
  Microsoft Graph for membership. SAML (150) and the implicit flow have lower limits; implicit flow signals overage with `hasgroups`.
- Prefer **app roles** for authorisation; groups claim for coarse membership.

## Access token version
Manifest `requestedAccessTokenVersion` (under `api` in the Graph application resource): `2` for v2 tokens.
It sets the token version your API receives regardless of endpoint; your API's issuer/audience validation must match.
```bash
az rest --method PATCH --url https://graph.microsoft.com/v1.0/applications/<objectId> \
  --body '{"api":{"requestedAccessTokenVersion":2}}'
```

## Customising beyond optional claims
Claims mapping policies / custom claims providers (directory extension attributes, transformed values) - for
apps these require `acceptMappedClaims` (use claims mapping without a custom signing key) or a custom signing key; prefer directory extension optional
claims (`extension_<appIdNoDashes>_attr`) where possible.

## Gotchas
- Decode a freshly issued token to check changes; older tokens keep their old claims.

## Verify
- [ ] Decode a fresh token (jwt.ms) and confirm claims and token version.

## Checked

Date: 2026-10-28.

Confirmed against Learn (optional-claims, app manifest reference, group claims guide): optional-claims JSON shape (idToken/accessToken/saml2Token), ApplicationGroup, sAMAccountName/SID emit options, 200-group JWT limit and 150 for SAML, hasgroups/_claim_names overage signals, requestedAccessTokenVersion, acceptMappedClaims meaning, extension_<appid>_<name> naming.
Removed: Graph-token and email/upn behaviour, the groups option list, the Graph overage endpoints, the legacy accessTokenAcceptedVersion name, issuer/audience specifics, token-refresh and appRoleAssignmentRequired notes.

Method: documentation only; no commands were run.
