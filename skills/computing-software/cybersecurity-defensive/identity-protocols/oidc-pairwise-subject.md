---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-pairwise-subject
name: oidc-pairwise-subject
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-pairwise-subject, oidc-userinfo-claims, pairwise, public, sector_identifier_uri, subject_type, correlation, identity-protocols]
level: advanced
status: docs-checked
description: "Use pairwise sub values and sector_identifier_uri to prevent RP correlation, and how to handle account linking and migration."
sources:
  - https://openid.net/specs/openid-connect-core-1_0.html
  - https://openid.net/specs/openid-connect-registration-1_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Public and pairwise subject identifiers

Goal: give each RP a different, stable `sub` for the same user.

Method: the OP lists `subject_types_supported` (`public`, `pairwise`) in discovery; `public` is the default when absent. A client may register `subject_type=pairwise`. The OP computes a unique `sub` per Sector Identifier that no party but the OP can reverse; the algorithm must be deterministic and distinct sectors must give distinct values (examples: SHA-256 of sector identifier, local account ID and a secret salt; encryption; or a stored GUID). The sector is the host of the registered `redirect_uri`s; if there are several hosts the client must register a `sector_identifier_uri`, an https URL to a JSON array of `redirect_uri` values that must include all registered redirect URIs (validated at registration).

Gotchas:
- Two RPs cannot compare `sub` values to correlate a user without permission.
- A `sector_identifier_uri` also lets a client change redirect domains without re-registering its users.
- Pairwise values are not reversible; store them as given.

Verify: register two clients with different sectors and confirm different `sub` values.

## Checked
2026-11-02. Confirmed against OpenID Connect Core 1.0 sections 8 and 8.1 and Dynamic Client Registration 1.0 section 5. Removed: "changing the sector identifier changes every user's sub; plan it" is kept only as implied by distinct sectors giving distinct values, so the explicit migration advice was dropped.
Method: documentation only; no commands were run.
