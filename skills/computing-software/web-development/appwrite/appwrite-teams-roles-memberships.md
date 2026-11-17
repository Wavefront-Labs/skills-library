---
id: computing-software.web-development.appwrite.appwrite-teams-roles-memberships
name: appwrite-teams-roles-memberships
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, auth, teams, memberships, roles, permissions]
level: practitioner
status: docs-checked
description: "Create teams with custom roles, invite members, grant access with Role.team and hide private membership fields."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/auth/teams/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: share resources between groups of users.

Basics:
- Create a team with `teams.create(...)`, supplying roles such as `maths`, `sciences`, `arts`, `literature`. The creator automatically gets the `owner` role, and only owners can invite and remove members.
- Invite by creating a membership (`teams.createMembership`). The invitee accepts to gain access and loses it if removed.
- CLI: `appwrite teams create-membership [options]` invites a member; you can also get, update and delete memberships but cannot configure permissions for team members from the CLI.

Permissions: `Role.team('<TEAM_ID>')` grants every member; `Role.team('<TEAM_ID>', ['<ROLE>', ...])` limits access to listed roles.

Memberships privacy: in Console go to Auth > Security > Memberships privacy to mark `userName`, `userEmail` and `mfa` as private.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): products/auth/teams. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Removed team preferences (64kB, updatePrefs/getPrefs; not on the page), the free-form roles Gotcha and the invented Verify; kept create/invite/CLI/permissions/privacy as on the page.

Method: documentation only; no commands were run.
