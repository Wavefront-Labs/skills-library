---
id: computing-software.systems-network-administration.immich.albums-and-shared-links
name: albums-and-shared-links
category: computing-software
field: systems-network-administration
product: immich
tags: [shared-album, public-link, editors, viewers, expiration]
level: intro
status: docs-checked
description: "Share Immich albums with local users as editors or viewers, and create public links with expiry and password options for people without accounts."
sources:
  - https://docs.immich.app/features/sharing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: pick the right sharing mode in Immich.

Local sharing, for users on the same instance:

- Albums: after creating an album, click the share icon, select users, and give each a role: editor (read-write) or viewer (read-only). Shared users can view and add their own photos and videos to the album. Works on web and mobile.
- Partners: share your entire library. See the partner sharing skill.

Public sharing, for anyone with the link, including people with no Immich account:

- Select photos or videos, or use the share icon on an album, and create a public link.
- The link is a random URL that acts as a secret so it cannot easily be guessed, for example `https://my.immich.app/share/<long-random-token>`.
- Customise the link: set an expiration date, password protection, and which actions the viewer can perform on the shared assets.
- A public link can allow the recipient to upload photos or videos into your account, which is handy for collecting guests' pictures.

Operational points:

- Anyone holding a public link can use it, so use a password and an expiry for sensitive material, and delete links you no longer need.
- Recipients outside your network can only open a link if your instance is reachable from the internet; see the remote access options skill.

## Checked

2026-11-09. Confirmed against the Sharing page: local album sharing with editor (read-write) and viewer (read-only) roles, partners, public links with random URL, expiry, password, allowed actions, and upload by recipients. The two operational points are practice guidance, not from the page.
Method: documentation only; no commands were run.
