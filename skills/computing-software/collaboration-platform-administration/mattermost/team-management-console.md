---
id: computing-software.collaboration-platform-administration.mattermost.team-management-console
name: team-management-console
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [team-management, archive-team, group-sync, system-console-teams]
level: practitioner
status: docs-checked
description: "Manage Mattermost teams in the System Console: group sync vs invite only, archive and unarchive (console and mmctl), groups and member roles."
sources: ["https://docs.mattermost.com/administration-guide/manage/team-channel-members.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Managing teams in the System Console

System admins manage teams in System Console > Teams (User Management > Teams). A team is managed either by Group Sync or Invite Only, and the mode changes which options are available. Select a team to open its configuration.

Profile: the team name and description. Archiving a team makes its contents inaccessible to all users, including its posts and related information. To archive, select Archive Team, Save, then confirm Archive. To restore, select Unarchive Team and Save. The mmctl equivalents are mmctl team archive and mmctl team restore.

Team management: when Sync Group Members is enabled the Synced Groups list appears and more groups can be added; when it is not enabled, you choose invitation limitations instead.

Groups: add and remove groups, and promote or demote group members between team admin and member.

Members: system admins see the full member list of a team, can add or remove members, and promote or demote between member and team admin. The role filter narrows the list to Guest, Member, Team admin or System admin.

System admins can also view channel membership and member counts, archive channels without joining them, and demote team and channel admins from the console. Prefer group sync for LDAP-backed teams so membership follows directory groups, and invite-only for ad hoc teams.

## Checked

Confirmed against the Manage team and channel members page (Teams section): management modes, profile and archive steps, mmctl team archive and restore, team management, groups, members and role filters. The group-sync advice in the last sentence is the author's.

Method: docs-checked 2026-11-09 against the full administration-guide/manage/team-channel-members page (source rst from the mattermost/docs repo).
