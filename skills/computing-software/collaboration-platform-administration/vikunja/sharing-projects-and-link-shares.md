---
id: computing-software.collaboration-platform-administration.vikunja.sharing-projects-and-link-shares
name: sharing-projects-and-link-shares
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, project-sharing, link-shares, permission-levels, share-with-team]
level: intro
status: docs-checked
description: "Share Vikunja projects with users, teams or password-protected link shares, choose Read, Read and Write or Admin, and revoke or replace shares."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/help/sharing-and-teams.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Open the three-dot menu on a project, choose Share, then pick user, team or link share. All three use the same permission levels: Read, Read & Write, Admin.

Users: search by username; name or email search works only if the target allows it in their privacy settings.

Teams: share with any team you belong to; all current and future members get the chosen level. If the instance enables public teams you can also share with a public team you are not in.

Link shares give access without an account. Options: optional name (labels comments made through the link), optional password, permission level. Listing them needs Admin on the project, because a link grants whatever level it was created with. Per share you can copy the link, set which view opens by default, or delete it, which revokes access immediately. Link shares cannot be edited: to change name, password or level, delete and recreate.

## Checked

2026-11-04. Confirmed against the Vikunja Sharing & Teams help page (help/sharing-and-teams): share menu path, the three methods and permission levels, user search and privacy, team sharing and public teams, link share options, Admin needed to list them, copy, default view and delete, and no editing. Removed: the service.enablelinksharing tip and the webhook remark, which that page does not state.

Method: documentation only; no commands were run.
