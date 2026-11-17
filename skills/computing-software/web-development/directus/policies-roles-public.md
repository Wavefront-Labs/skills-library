---
id: computing-software.web-development.directus.policies-roles-public
name: policies-roles-public
category: computing-software
field: web-development
product: directus
tags: [policies-roles, public-role, user-status, studio-users]
level: practitioner
status: docs-checked
description: "Understand Directus policies, roles, the administrator and public roles, user statuses and which users count as Studio seats."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/03.auth/2.access-control.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- **Policy**: group of permissions applied to users or roles (new in Directus 11). Applying policies is additive; they add, never subtract.
- **Role**: organizational tool; can hold any number of policies and child roles, and apply to many users.
- **Administrator role**: unrestricted; at least one admin user must exist.
- **Public role**: governs unauthenticated requests and users without a role. All public permissions are off by default.

Warning: collection-level read for the public role exposes all items, including unpublished ones, to anyone. Review the security best practices before enabling.

Policy toggles: App Access (Data Studio; leave off for API-only users), Admin Access, Require 2FA, IP allowlist.

User statuses: Draft, Invited, Unverified, Active, Suspended, Archived. Only Active can authenticate.

Seat counting: Studio users are those with at least one policy with Admin Access or App Access. API-only users do not consume a seat.

## Checked

2026-11-04: policy, role, administrator and public role definitions, public read warning, policy toggles, user statuses and Studio seat counting confirmed against the Directus Access Control page. Removed a Verify line the page does not state.

Method: documentation only; no commands were run.
