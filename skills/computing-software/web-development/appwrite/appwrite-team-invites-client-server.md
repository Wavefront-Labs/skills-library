---
id: computing-software.web-development.appwrite.appwrite-team-invites-client-server
name: appwrite-team-invites-client-server
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, auth, teams, invites, memberships]
level: practitioner
status: docs-checked
description: "Choose between emailed client-side team invites that need acceptance and server-side memberships that activate immediately."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/auth/team-invites/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: add people to teams the right way.

Client-side email invites: creating a membership with a Client SDK makes Appwrite create a user account if none exists for the email, send an invitation email using built-in templates (with localization), and create a pending membership. The email link contains a secret; your app receives the redirect and calls `teams.updateMembershipStatus({ teamId, membershipId, userId, secret })`. Accepting activates the membership and the user gains immediate access.

Server-side custom flows: with a Server SDK, `teams.createMembership` with a `userId` bypasses the email and creates an active membership at once, with no acceptance. Use it for bulk user management, automated team assignment or integration with external systems.

Manage lifecycle: list memberships (`teams.listMemberships`), update roles (`teams.updateMembership`; only members with the owner role can update other members' roles), remove members (`teams.deleteMembership`; team owners can remove members or users can leave).

Checking status differs by side. Client SDK: list teams, then `listMemberships` for a team and find the user; `membership.confirm` is `false` when invited and `true` when joined. Server SDK: the data is not filtered per user, so iterate teams and their memberships; `membership.joined` is `null` when invited and a timestamp when joined.

Gotcha: a client-side invite stays pending until the user accepts it; a server-created membership is active immediately.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): products/auth/team-invites. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Removed the invites-auth-method toggle claim (not on the page), the "Role.team checks fail until acceptance" Gotcha as worded, and the invented Verify; added the client/server status fields (confirm vs joined), that only owners update roles and that owners can remove members or users can leave.

Method: documentation only; no commands were run.
