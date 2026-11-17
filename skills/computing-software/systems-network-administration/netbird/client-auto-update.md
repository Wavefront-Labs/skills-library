---
id: computing-software.systems-network-administration.netbird.client-auto-update
name: client-auto-update
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, auto-update, force-update, pinned-version, client-versions]
level: practitioner
status: docs-checked
description: "Configure NetBird client automatic updates: latest or pinned version, forced background installs, version requirements, check cadence and supported platforms."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/peers/auto-update.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Requirements: clients and Management server v0.61.0 or later.

Enable in the dashboard at Settings > Clients > Automatic Updates:
- Disabled (default).
- Latest Version: newest stable release.
- Custom Version: pin a version without the "v" prefix, e.g. 0.61.0.

Clients never downgrade; a pinned version older than the current one has no effect.

Force Automatic Updates installs in the background without prompting, even when the UI is not running. Needs v0.67.0+ on server and clients. It restarts the client and can briefly interrupt connections, so use cautiously in production.

Behaviour:
- Settings sync when a peer connects; changes reach connected peers immediately.
- Peers on the latest version re-check every 30 minutes.
- Prompted updates show as a system notification and tray entry; the background service downloads and installs, so no admin rights are needed. The UI must be running with notifications enabled.
- Failures show an error; forced updates retry automatically, prompted ones can be retried from the tray.

Platforms: Windows (EXE and MSI), macOS (PKG only; Homebrew installs are not auto-updated). Linux is not supported yet.

## Checked

2026-11-04: read the Client Automatic Updates page in full. Confirmed the v0.61.0 and v0.67.0 requirements, the three modes and default, no-downgrade rule, force update warning, 30 minute re-check, install path without admin rights, error handling and supported platforms. Nothing removed.

Method: documentation only; no commands were run.
