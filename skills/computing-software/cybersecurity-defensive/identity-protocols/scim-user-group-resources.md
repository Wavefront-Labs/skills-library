---
id: computing-software.cybersecurity-defensive.identity-protocols.scim-user-group-resources
name: scim-user-group-resources
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [scim-user-group-resources, scim-schema, scim-user, scim-group, username, externalid, emails, members, meta, identity-protocols]
level: practitioner
status: docs-checked
description: "Model users and groups: id, externalId, userName, name, emails, active, groups, members, meta fields and the primary and type conventions."
sources:
  - https://www.rfc-editor.org/rfc/rfc7643
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SCIM User and Group resources

Goal: produce well-formed resources.

User (`urn:ietf:params:scim:schemas:core:2.0:User`): `id` (issued by the service provider, read-only), `externalId` (identifier from the provisioning client), `userName` (required, unique, case insensitive), `name{givenName,familyName,formatted}`, `displayName`, `emails[{value,type,primary}]`, `phoneNumbers`, `active`, `groups` (read-only), `roles`, `entitlements`, `x509Certificates`, `meta{resourceType,created,lastModified,location,version}`.
Group (`urn:ietf:params:scim:schemas:core:2.0:Group`): `displayName` (required), `members[{value (the member's id), $ref, type}]`; members may be users or groups (nested groups).

Gotchas:
- A multi-valued attribute's `primary: true` MUST appear no more than once.
- Group membership changes are made on the Group resource because `User.groups` is read-only.
- The `schemas` attribute is required in every resource.
- `externalId` lets a client locate a resource with a filter, avoiding a local id mapping.

Verify: create a user and group, add a member, then GET both and check consistency.

## Checked
2026-11-02. Confirmed against RFC 7643 sections 3.1, 4.1.1, 4.1.2, 4.2 and 8. Removed: the advice to match `userName` or `externalId` before creating (the RFC states only what `externalId` is for).
Method: documentation only; no commands were run.
