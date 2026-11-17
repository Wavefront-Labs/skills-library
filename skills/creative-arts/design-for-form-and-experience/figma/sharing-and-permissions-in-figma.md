---
id: creative-arts.design-for-form-and-experience.figma.sharing-and-permissions-in-figma
name: sharing-and-permissions-in-figma
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [figma-permissions, sharing, file-permissions, link-sharing, roles-and-seats, guest-access, dev-seat, figma]
level: practitioner
status: docs-checked
description: "Share Figma files safely: team and project access, link sharing, edit versus view permission, seats, guest access and ownership handover."
sources:
  - https://help.figma.com/hc/en-us/articles/1500007609322-Guide-to-sharing-and-permissions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sharing and permissions in Figma

## Model
- Collaborators have **Can view** (inspect properties, follow, comment) or **Can edit** (change files and folders).
- Sharing works at several levels, from team or plan down to folder, file or prototype. Permissions apply at file, folder and team levels; **team-level permissions exist only on Organization and Enterprise plans**.
- Links can be shared for prototypes, files and folders; on Organization and Enterprise plans also for a single team. Starter and Professional plans are a single team, so inviting someone makes them a full plan member. People without access can request it.
- On paid plans, editing a file needs both an appropriate seat and Can edit permission.
- Organization and Enterprise plans can add members and guests to the organization or to specific assets. For guest limits, seat types and link settings, read the current Help Center pages on seat types and share settings.

## Practice (team convention, not Figma rules)
- Keep production files in shared team projects, not personal drafts.
- Give external collaborators access only to the files they need, and remove it when the engagement ends.
- Review who has access regularly and keep library file edit rights tight (`creative-arts.design-for-form-and-experience.figma.publishing-and-updating-a-figma-library`).
- Hand over ownership of key files before people leave.

## Verify
- [ ] Access follows least privilege.
- [ ] Seat types match what each person must do.
- [ ] External collaborators are removed after projects end.

## Checked
2026-11-01. Confirmed on the Figma Help Center Guide to sharing and permissions: the permission levels, hierarchy, team-level plan limit, link sharing, single-team plans and the seat requirement. Removed: open/closed/secret team types, role names, link password and expiry, copy and export restrictions, seat-type descriptions, SSO and SCIM, and ownership-transfer steps, none stated on the page read.
Method: documentation only; no commands were run.
