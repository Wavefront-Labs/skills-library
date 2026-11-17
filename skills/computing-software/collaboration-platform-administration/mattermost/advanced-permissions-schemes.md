---
id: computing-software.collaboration-platform-administration.mattermost.advanced-permissions-schemes
name: advanced-permissions-schemes
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [permission-schemes, team-override-scheme, mmctl-permissions, system-scheme]
level: advanced
status: docs-checked
description: "Control who can do what in Mattermost with the System Scheme and Team Override Schemes, plus recipes for member visibility, channel creation and read-only channels."
sources: ["https://docs.mattermost.com/administration-guide/onboard/advanced-permissions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Advanced permissions

Admins on Cloud or self-hosted Mattermost use permission schemes to decide which users can perform actions such as creating teams, managing channels or configuring webhooks. Two schemes exist.

System Scheme (System Console > User Management > Permissions > System Scheme): default permissions for system admins, team admins, channel admins, guests (if enabled) and all members, applied in every team and channel. Team Override Scheme (same area): permissions that apply only to the teams assigned to it; the System Scheme does not apply to those teams, and a team can belong to only one override scheme. Channel-level controls live under User Management > Channels.

Recipes:
- Hide members from each other outside shared teams or channels: use mmctl permissions remove to revoke the view_member permission from the system_user role.
- Only admins may add members in one team, everyone elsewhere: in the System Scheme tick Add Team Members for All Members and save; create a New Team Override Scheme, add the team, untick Add Team Members under All Members and tick it under Team Administrators; save.
- Restrict renaming and editing channels: in the System Scheme untick Manage Public Channels > Manage Channel Settings for All Members.
- Restrict channel creation in one team: tick Create Channels in the System Scheme, then in an override scheme for that team untick it for All Members and tick it for Team Administrators.
- Allow anyone to convert public channels to private: edit the scheme and adjust Manage Public Channels > Convert Channels for All Members; when it is not enabled for members, give it to team and channel admins manually.
- Restrict deleting messages: untick Delete Own Posts and Delete Others' Posts for All Members and Channel Administrators, and tick them for Channel and Team Administrators as needed.
- Guest read-only and announcement channels: set Create Posts and Post Reactions per channel under User Management > Channels.

## Checked

Confirmed against the Advanced permissions page: the two schemes and their console paths, the override scheme rules, and each recipe listed (view_member via mmctl, add team members, rename and edit channels, channel creation, convert channels, delete posts, guest read-only and announcement channels). Nothing removed.

Method: docs-checked 2026-11-09 against the full administration-guide/onboard/advanced-permissions page (source rst from the mattermost/docs repo).
