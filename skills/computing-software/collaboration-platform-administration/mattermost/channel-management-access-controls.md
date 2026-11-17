---
id: computing-software.collaboration-platform-administration.mattermost.channel-management-access-controls
name: channel-management-access-controls
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [channel-management, read-only-channel, guest-permissions, advanced-access-controls]
level: advanced
status: docs-checked
description: "Manage channels in the System Console and restrict posting, reactions, mentions, membership and bookmarks, with guest-readonly and announcement recipes."
sources: ["https://docs.mattermost.com/administration-guide/manage/team-channel-members.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Channel management and advanced access controls

System Console > Channels lists public, private and archived channels, channels synchronised to an AD/LDAP group, and channels with manually invited users. A channel is managed by Group Sync or Manual Invites. Selecting a channel shows its profile (name, description; Archive Channel then Save, and it stays searchable in the list; Unarchive Channel to restore), management (with Sync Group Members on you can add synced groups; otherwise set the channel Private or Public), groups, and members with role filter for Guest, Member, Channel admin and System admin.

Advanced access controls, set under User Management > Channels, let admins restrict: making the channel read-only, posting reactions, channel-wide mentions (@all, @channel, @here), channel member management (only admins add and remove members), and bookmarks management (only channel and system admins). They apply only to guests and members; system, team and channel admins are unaffected. To let a specific member post in a restricted channel, promote them to channel admin first. Existing system or team permission configuration can override channel settings.

Recipe, guests read and react only: Edit the channel, uncheck Guests in Create Posts and, if wanted, in Post Reactions, then Save.

Recipe, announcement channel: create the channel, Edit it, uncheck Guests and Members in both Create Posts and Post Reactions, Save. Only admins can then post.

From v11.5.2 a system admin can set a channel's complete membership in a single API call and the server computes the add and remove diff.

## Checked

Confirmed against the Manage team and channel members page (Channels section): filters, management modes, archive behaviour, the five advanced access controls and their guest and member scope, both recipes, and the v11.5.2 membership API note. Nothing removed.

Method: docs-checked 2026-11-09 against the full administration-guide/manage/team-channel-members page (source rst from the mattermost/docs repo).
