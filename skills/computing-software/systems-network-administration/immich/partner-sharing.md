---
id: computing-software.systems-network-administration.immich.partner-sharing
name: partner-sharing
category: computing-software
field: systems-network-administration
product: immich
tags: [partner, timeline, one-way, sharing, privacy]
level: intro
status: docs-checked
description: "Share a whole Immich library with another user: what partner sharing includes and excludes, one-way behaviour, timeline integration and removal."
sources:
  - https://docs.immich.app/features/partner-sharing
  - https://docs.immich.app/features/sharing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: give another user on the same instance read access to your whole library.

Partners can view your library and download assets. Manage it in User Settings on the web.

Included:

- Access to all non-archived and trashed photos and videos (wording as in the docs).
- All metadata, including GPS information.
- The ability to share your assets via shared links, albums and so on.

Not included:

- Partner albums that already exist.
- Whether an asset is favorited.
- People and facial recognition data.

Notes:

- Sharing is one-way. To see their assets, your partner must also share with you.
- Duplicate detection runs per user, so partner assets can appear as duplicates of yours on the main timeline.

Manage partner sharing from the User Settings page on the web. View a partner's assets from the Sharing page.

Timeline integration: partner photos can be shown in your main timeline, enabled per partner on web and mobile. On web it is Account Settings > Partner Sharing > Show in timeline. In the mobile app, from the partner's view, toggle the button.

Removing access: User > Account Settings > Sharing and click the X button.

For per-album access or links for people without an account, use album sharing and shared links instead; partner sharing is for the whole library.

## Checked

2026-11-09. Confirmed against the Partner Sharing page: included and excluded items, one-way note, duplicates note, Sharing page, timeline integration on web and mobile, removal path. Removed: the unstated "add the user" procedure and the editor or viewer role wording (the sharing page was fetched but not summarised here).
Method: documentation only; no commands were run.
