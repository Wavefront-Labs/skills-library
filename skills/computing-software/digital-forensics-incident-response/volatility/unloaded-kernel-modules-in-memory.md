---
id: computing-software.digital-forensics-incident-response.volatility.unloaded-kernel-modules-in-memory
name: unloaded-kernel-modules-in-memory
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [unloadedmodules, volatility3, kernel-drivers, byovd, rootkit-detection, dfir]
level: advanced
status: docs-checked
description: "Find drivers that loaded and unloaded before capture with Volatility 3 windows.unloadedmodules, treat them as BYOVD and rootkit leads, and corroborate."
sources: ["https://volatility3.readthedocs.io/en/latest/volatility3.plugins.windows.unloadedmodules.html", "https://www.loldrivers.io/", "https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/design/microsoft-recommended-driver-block-rules"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unloaded kernel modules in memory

Attackers may load a vulnerable or malicious driver, use it, then unload it to reduce traces. Windows keeps a
record of recently unloaded kernel modules, and the Volatility 3 plugin `windows.unloadedmodules` lists the
unloaded kernel modules (it also supports the timeliner interface).

## Run
```bash
vol -f mem.raw windows.unloadedmodules
```

## What to look for
- Names matching known vulnerable or abused drivers. Use the LOLDrivers project and Microsoft's recommended
  driver block rules as reference lists; the block rules page describes the Microsoft vulnerable driver
  blocklist, which is enabled by default since the Windows 11 2022 update.
- Unload times clustered just before security tooling stopped or before destructive activity.
- Driver files that no longer exist on disk.

## Corroborate
- Service-install and driver-load telemetry around the same time, and the driver file's hash and
  signature from disk, Amcache or endpoint logs.
- Microsoft recommends the Attack Surface Reduction rule "Block abuse of exploited vulnerable signed
  drivers" (stops such a driver being written to disk) and applying the vulnerable driver blocklist or an
  App Control policy to stop an existing driver loading.

## Gotchas
- Legitimate unloads are common; judge by name, timing and corroboration.
- If the plugin returns nothing on a build you expect to work, check symbols before concluding the list
  is empty.

## Verify
Each suspicious unloaded driver is matched to a file hash and to the time window of attacker activity.

## Checked
2026-11-08. Read: unloadedmodules plugin reference page and the Microsoft recommended driver block rules
page (blocklist default, ASR rule, App Control). The LOLDrivers site loaded only as a short landing page, so
no driver names from it are kept. Removed unconfirmed claims: MmUnloadedDrivers name and 50-entry size,
output columns, the driver file name list, event IDs (7045, 7036, 3077, 3033, Sysmon 6), registry and Amcache
locations, and the callbacks and ssdt cross-check.
Method: documentation only; no commands were run.
