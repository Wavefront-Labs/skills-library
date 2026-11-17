---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-attribute-mapping
name: saml-attribute-mapping
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-attribute-mapping, saml-attributes, attribute-release, jit, group-claim, mapping, claims, identity-protocols]
level: practitioner
status: draft
description: "Design SAML attribute release: minimum set, stable identifier, group claims, just-in-time provisioning mapping and trust of IdP-asserted data."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Attribute release and mapping to local users

Goal: pass enough to authorise, nothing more.

Method:
1. Choose the account key: persistent NameID or an immutable internal ID attribute, not mutable email.
2. Release only needed attributes (email, name, groups or roles).
3. For groups, send group names or IDs relevant to the app only; large group claims overflow headers or cause token bloat.
4. At the SP, map assertion attributes in a table, define behaviour for missing attributes, and decide whether attributes overwrite local data on every login.

Gotchas:
- Trusting email_verified-like claims: SAML has no such standard; the IdP must be the authority for the domain.
- Role claims from the user's own directory object can be user-editable on some IdPs; confirm.
- Reject logins where required attributes are empty rather than creating blank accounts.

Verify: log in as a user with missing optional attributes.
