---
id: computing-software.networking-hardware-and-wireless.tailscale.client-updates-auto-update
name: client-updates-auto-update
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [auto-update, tailscale-update, update-track]
level: practitioner
status: docs-checked
description: "Check versions, enable auto-updates and use tailscale update."
sources: ["https://tailscale.com/kb/1067", "https://tailscale.com/kb/1080"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Updating clients

Goal: keep every device on a current version.

**Check versions.** Machines page, Version column; the Version filter with Update available lists only outdated devices.

**Auto-updates.**

- Owner, Admin or IT admin: Device management page, under Auto-update Tailscale enable Auto-update new devices.
- That toggle does not change settings of existing devices; devices can individually opt in or out any time.
- iOS, macOS App Store and Android Google Play versions may not have auto-update configured by default; verify it.
- If you enforce updates with system policies, those policies decide when updates occur.
- Updates apply even while the client is disconnected from Tailscale.

**CLI**
```
tailscale update --dry-run
tailscale update --track=stable
tailscale update --version=<x.y.z> --yes
```
- `--track` is `stable`, `release-candidate` or `unstable`; default is the track in effect. You cannot combine `--track` and `--version`.
- `--version` is not available on the macOS client.
- Minimum versions for the command differ by platform (v1.36 on Windows and Ubuntu/Debian, v1.48.0 for the Mac App Store version and Synology, v1.54.0 for QNAP and standalone).
- Downgrading below a version without `tailscale update` removes your ability to use it.

**Checklist**

1. Auto-update enabled.
2. Mobile defaults verified.
3. Dry-run before manual updates.

## Checked

2026-11-03. Read Update clients (kb/1067) and the CLI reference (kb/1080) and confirmed the Auto-update new devices toggle, `tailscale update` flags and tracks, and the per-platform minimum versions. Nothing else was removed.

Method: documentation only; no commands were run.
