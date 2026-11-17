---
id: computing-software.systems-network-administration.jellyfin.user-permissions-and-playback
name: user-permissions-and-playback
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, users, permissions, transcoding-permission, live-tv, remote-control, downloads]
level: practitioner
status: docs-checked
description: "Control what a Jellyfin user may do: remote access, Live TV, playback and transcoding, bitrate limit, deletion, remote control and downloads."
sources: ["https://jellyfin.org/docs/general/server/users/adding-managing-users/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# User permission settings

On a user's Profile tab, the options (checkboxes, unticked blocks the feature) are:

- **Allow remote connections to this Jellyfin Server:** unticked, logins from outside the networks defined as local are blocked. By default local is only your subnet, but more can be added.
- **Live TV:** `Allow Live TV access` and `Allow Live TV recording management`. If you never set up Live TV, users are blocked regardless.
- **Media playback:** `Allow media playback` blocks library access but not Live TV. `Allow audio/video playback that requires transcoding` and `Allow video playback that requires conversion without re-encoding` block those paths. `Internet streaming bitrate limit (Mbps)` caps each stream for out-of-network devices.
- **Allow Media Deletion From:** all libraries or per library. Be careful, since some plugins delete media after watching.
- **Remote control:** `Allow remote control of other users` (control what others play and send messages, without admin rights) and `Allow remote control of shared devices` (unclaimed DLNA devices and devices they are logged in to).
- **Download & Sync:** allows downloading media; syncing and transcoding are not available.
- **Additional:** `Allow social media sharing` lets the user share page URLs. `Disable this user` blocks login and abruptly ends existing connections. `Hide this user from login screens` suits private admin accounts; new users are hidden by default. `Allow media conversion` is not available.

Changes need `Save`.

## Checked

2026-11-03. Confirmed against the Jellyfin Managing Users page, Profile section: every option name and description listed above. Nothing removed.

Method: documentation only; no commands were run.
