---
id: computing-software.web-development.ghost.ghost-admin-api-users-roles-and-invites
name: ghost-admin-api-users-roles-and-invites
category: computing-software
field: web-development
product: ghost
tags: [ghost, admin-api, staff, roles, invites, users]
level: practitioner
status: docs-checked
description: "Invite Ghost staff via the Admin API by fetching role IDs first, then posting an invite with role and email."
sources:
  - https://github.com/TryGhost/docs/blob/main/admin-api/users/roles.mdx
  - https://github.com/TryGhost/docs/blob/main/admin-api/users/invites.mdx
  - https://github.com/TryGhost/docs/blob/main/admin-api/users/overview.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: add a staff member programmatically.

Two resources are involved:
- Roles: a read endpoint that returns the roles defined on the site, each with an id.
- Invites: the resource used to invite staff users. To invite someone you must specify the ID of the role they should receive and the email address the invite link goes to.

Steps:
1. `GET /admin/roles/` and note the id of the role you want.
2. `POST /admin/invites/` with `{"invites":[{"role_id":"<role id>","email":"new.staff@example.com"}]}`.
3. The invitee receives an email link to complete signup.

The users resource fetches and edits staff user data. The endpoint table of integration-available resources lists only `/users/` (Browse, Read); roles and invites are not listed there.

Gotcha: staff tokens cannot transfer ownership or delete all content.

Verify: the invite request succeeds and the invitee receives the email.

## Checked

2026-11-04. Confirmed: role fetch, invite body with role_id and email, users resource purpose, the staff-token exceptions (roles, invites, users overview and Admin API overview pages). Removed: the delete operation, the 403-as-signal rule and the "browse invites" check, which no page states.

Method: documentation only; no commands were run.
