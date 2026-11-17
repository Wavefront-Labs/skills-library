---
id: computing-software.collaboration-platform-administration.vikunja.teams-management
name: teams-management
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, teams, team-admin, team-members, team-sharing]
level: intro
status: docs-checked
description: "Create Vikunja teams, add and remove members, use the team admin role and share projects with a team; note how SSO and LDAP team sync differ."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/help/sharing-and-teams.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Teams group users so a project can be shared with all of them at once. Open Teams from the left sidebar, use the create button, give a name (and optionally a description); it exists immediately.

Members: add or remove in team settings. Finding a user depends on their privacy settings: exact username always works, name or email only sometimes.

Team admin: each member can be flagged team admin. A team admin can add and remove members and change who else is team admin. This is about managing the team only. Project access is separate and set in the project's sharing settings.

Sharing a project with a team: project sharing settings, team section, pick level (Read, Read & Write, Admin), add. Current and future members of that team get access.

## Checked

2026-11-04. Confirmed against the Vikunja Sharing & Teams help page (help/sharing-and-teams): creating teams, member management and privacy-dependent search, the team admin role and its limits, and sharing a project with a team. Removed: the removal-revokes-access inference and the note about synced teams being overwritten, which that page does not state.

Method: documentation only; no commands were run.
