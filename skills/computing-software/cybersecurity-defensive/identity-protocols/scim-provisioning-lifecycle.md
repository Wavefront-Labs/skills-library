---
id: computing-software.cybersecurity-defensive.identity-protocols.scim-provisioning-lifecycle
name: scim-provisioning-lifecycle
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [scim-provisioning-lifecycle, scim-operations-security, lifecycle, deprovisioning, active-false, externalid, joiner-mover-leaver, soft-delete, identity-protocols]
level: practitioner
status: docs-checked
description: "Implement joiner, mover and leaver semantics over SCIM: correlate by externalId or userName, soft-deactivate with active false, group sync and re-hire."
sources:
  - https://www.rfc-editor.org/rfc/rfc7644#section-7
  - https://www.rfc-editor.org/rfc/rfc7642
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Provisioning lifecycle: create, deactivate, delete

Goal: keep downstream accounts aligned with the IdP.

RFC 7642 frames provisioning flows around joiner, mover, leaver and just-in-time (JIT) triggers. Mapping onto the SCIM protocol (RFC 7644, RFC 7643):
- Joiner: the client can locate a resource by its own identifier with `filter=externalId eq "..."` (that is what `externalId` is for); if none, POST (201). A duplicate `userName` returns 409 `uniqueness`.
- Mover: PATCH attributes and group memberships.
- Leaver: `active` is the user's administrative status; its meaning is defined by the service provider, typically `false` means the account is suspended and `true` means the user can log in. DELETE returns 204; the server MAY keep the data but MUST return 404 for later operations, and a later create with the same `userName` SHOULD NOT fail with 409.
- Keep `id` stable: it is server-issued and non-reassignable, and the client can store it as the link.

Gotchas:
- RFC 7642 also describes change notification: attributes may change when an account is disabled or a relationship ends, and a relying party that cached them needs to learn of it.
- What deactivation does to sessions and tokens in the target application is defined by the service provider, not by SCIM; check the application's own behaviour.

Verify: deactivate a test user and confirm the target application refuses login.

## Checked
2026-11-02. Confirmed against RFC 7642 (2.3 joiner/mover/leaver, 3.5 change notification), RFC 7643 sections 3.1 and 4.1.1 (`active`, `externalId`, `id`) and RFC 7644 sections 3.3, 3.6 and 7. Removed: retention-period, re-hire, session and token revocation rules, full-sync threshold advice and the "cascading deletes" gotcha, none of which the RFCs state.
Method: documentation only; no commands were run.
