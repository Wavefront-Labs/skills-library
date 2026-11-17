---
id: computing-software.systems-network-administration.jellyfin.general-server-settings
name: general-server-settings
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, server-name, splash-screen, login-disclaimer, custom-css, dashboard]
level: intro
status: docs-checked
description: "Configure Jellyfin's server name, splash screen image, login disclaimer and custom CSS, noting the splash screen privacy exposure."
sources: ["https://jellyfin.org/docs/general/server/settings/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# General server settings

The general settings in the Dashboard cover options that do not have their own sidebar entry, mostly interface and user experience.

- **Server Name:** shown to users when they pick a server and used by clients elsewhere. The default is the computer's hostname.
- **Splash Screen Image:** some clients use it as a background for login screens. The default image is generated from artwork of content on your server and is visible without authenticating, so it can reveal what content exists. Only content rated PG-13 or lower is used, but that relies on accurate rating data.
- **Login Disclaimer:** a message shown to users when they log in.
- **Custom Style:** custom CSS rules for minor changes to the web interface that do not need their own theme.

These are runtime settings in the web UI, distinct from the static configuration files described in `computing-software.systems-network-administration.jellyfin.main-configuration-layers`.

## Checked

2026-11-03. Confirmed against the Jellyfin Settings page (server name default hostname, splash screen image and PG-13 caveat, login disclaimer, custom style) and the Configuration page (static versus runtime settings). Removed: unsupported practical advice and the invented check.

Method: documentation only; no commands were run.
