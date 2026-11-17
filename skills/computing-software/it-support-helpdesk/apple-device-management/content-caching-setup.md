---
id: computing-software.it-support-helpdesk.apple-device-management.content-caching-setup
name: content-caching-setup
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, content-caching, content-caching-setup, bandwidth]
level: practitioner
status: docs-checked
description: "Turn on macOS Content Caching, choose storage and limits, set advanced keys with defaults and AssetCacheManagerUtil reloadSettings, and read the logs."
sources:
  - "https://support.apple.com/guide/deployment/depde72e125f/web"
  - "https://support.apple.com/guide/deployment/depe9b5c1aab/web"
  - "https://support.apple.com/guide/deployment/depc8f669b20/web"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# content-caching-setup

Goal: serve Apple software and iCloud data from a local Mac to save internet bandwidth.

- What it caches: software distributed by Apple and, optionally, data users store in iCloud. The first client downloads from Apple; later clients get the copy from the cache.
- Turn on: Apple menu > System Settings > General > Sharing > Content Caching (macOS 13 or later), or System Preferences > Sharing > Content Caching (macOS 12.0.1 or earlier). Hold the Option key and select Advanced Options for more settings.
- Host: a Mac with a single wired Ethernet connection as its only network connection gives best results; Wi-Fi works but performance might be affected (`AllowWirelessPortable` controls laptops with only Wi-Fi).
- Storage: cached content lives on the startup volume by default; you can choose another location and a maximum share. `CacheLimit` defaults to 0 (unlimited), `ReservedVolumeSpace` to 2 GB free, `DataPath` to `/Library/Application Support/Apple/AssetCache/Data`. Changing `DataPath` by hand does not move existing content; use the Content Caching settings to move it. When the limit or free space is reached, least recently used content is deleted. Pruning: unrequested content is removed after `PruneAssetsAge` (default 120 days).
- Keep it available: `KeepAwake` (default No) keeps the Mac awake while caching is on.
- Advanced keys live in `/Library/Preferences/com.apple.AssetCache.plist`. Set them with `sudo -u _assetcache defaults write /Library/Preferences/com.apple.AssetCache.plist Port -int 50000`, then run `sudo AssetCacheManagerUtil reloadSettings`. Only keys that can also be set in Content Caching preferences honour `reloadSettings`; others need caching stopped and restarted. Do not change keys that Apple's table does not list. `AssetCacheManagerUtil settings` shows the standard (non-advanced) settings.
- Logs: `log show --predicate 'subsystem == "com.apple.AssetCache"'`; `Verbose` adds detail but reduces performance. Metrics appear in the Cache pane of Activity Monitor.
- On managed Macs, use the MDM restriction to stop users turning caching on (this prevents the Mac downloading and storing Apple software and iCloud data).

Gotcha: clients that do not share a public IP (or a configured custom range) with the cache will not find it; see content-caching-network-requirements.

Verify:
- `AssetCacheManagerUtil settings` reflects the intended values after `reloadSettings`.
- The Cache pane in Activity Monitor shows served data after a second client downloads the same update.

## Checked

Date: 2026-11-07. Read in full: Apple Platform Deployment "Intro to content caching", "Plan for and set up content caching" and "Advanced content caching settings on Mac" (menu paths, defaults, the `AssetCacheManagerUtil` commands shown, key table rows used). Removed as unconfirmed: `sudo AssetCacheManagerUtil activate` and `status` (not on these pages; the command-line page was not found), the NAT-with-multiple-IPs gotcha, "monitor uptime" advice and the "check statistics after the first major release" practice.
Method: documentation only; no commands were run.
