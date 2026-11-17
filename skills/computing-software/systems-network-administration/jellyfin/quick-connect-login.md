---
id: computing-software.systems-network-administration.jellyfin.quick-connect-login
name: quick-connect-login
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, quick-connect, login, authorization, six-character-code, tv-clients]
level: intro
status: docs-checked
description: "Sign a new Jellyfin client in with a six-character Quick Connect code and disable the feature server-wide if unwanted."
sources: ["https://jellyfin.org/docs/general/server/quick-connect/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Quick Connect

Quick Connect signs users in to clients without typing a username or password. A temporary code is generated on the new device and authorised from a client that is already logged in. It suits devices with limited input, such as TVs.

**Use it (two devices)**
- Device A, the new client: choose **Quick Connect** on the login screen (some clients need **Manual Login** first). A 6-character code appears; keep the screen open.
- Device B, already authenticated: open `Settings` > `Quick Connect`, enter the code and confirm. Device A logs in automatically. An invalid or expired code gives an error and you start again.

**Disable it.** It is enabled by default. In the Admin Dashboard open the General tab and untick "Enable Quick Connect on this server".

**Client support** per the docs: signing in works on JellyCon, Jellyfin Android, Android TV, Media Player, Mobile (iOS), Roku, Web, WebOS, Xbox, Swiftfin (iOS and tvOS); authorising others works on Android, Media Player, Mobile (iOS), Web, WebOS, Xbox and Swiftfin (iOS). Jellyfin Kodi, MPV Shim and Vue support neither.

## Checked

2026-11-03. Confirmed against the Jellyfin Quick Connect page: two-device flow, 6-character code, Settings > Quick Connect, enabled by default and the General tab checkbox, the client support table. Removed: invented check step.

Method: documentation only; no commands were run.
