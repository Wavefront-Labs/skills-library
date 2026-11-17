---
id: computing-software.collaboration-platform-administration.mattermost.system-wide-notifications
name: system-wide-notifications
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [announcement-banner, system-wide-notifications, banner-dismissal, site-configuration]
level: intro
status: docs-checked
description: "Show an announcement banner in every channel for all users and teams, with colours and optional dismissal, from the System Console."
sources: ["https://docs.mattermost.com/administration-guide/manage/system-wide-notifications.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# System-wide notifications

System admins can show a banner in all channels for all users across all teams.

Setup in System Console > Site Configuration > System-wide notifications:
1. Set Enable system-wide notifications to true.
2. Enter the Banner Text to display in channels.
3. Choose the background colour and text colour of the banner.
4. By default users can dismiss the banner, and it stays dismissed until they log in again or until you update it. To stop users dismissing it, set Allow Banner Dismissal to false.
5. Select Save.

To update the banner, either change its text or re-enable it after it was disabled; either action shows it again to users who dismissed the old one. To remove it, set Enable Announcement Banner to false.

## Checked

2026-11-03. Confirmed against the Mattermost documentation page https://docs.mattermost.com/administration-guide/manage/system-wide-notifications. Removed unsupported usage advice.

Method: documentation only; no commands were run.
