---
id: computing-software.cybersecurity-defensive.endpoint-security.disable-autorun-and-autoplay
name: disable-autorun-and-autoplay
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [device-control, autorun, autoplay, removable-media, group-policy, nodrivetypeautorun, cis-control-10]
level: intro
status: draft
description: "Disable AutoRun and AutoPlay on Windows via policy so removable and network media cannot execute content automatically, and verify the setting."
sources: ["CIS Control 10.3 (disable autorun and autoplay for removable media)", "Microsoft Learn - AutoPlay and AutoRun policy settings", "CIS Microsoft Windows benchmarks (AutoPlay Policies)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Disable AutoRun and AutoPlay

**Goal:** inserting a USB stick, CD or mapping a share never runs or offers to run content
automatically.

## Policy (GPO: Computer Configuration > Administrative Templates > Windows Components > AutoPlay Policies)
| Setting | Value |
|---|---|
| Turn off AutoPlay | Enabled, All drives |
| Set the default behavior for AutoRun | Enabled, Do not execute any autorun commands |
| Disallow AutoPlay for non-volume devices | Enabled |
Intune: Settings catalog > Administrative Templates > Windows Components > AutoPlay Policies (same names).

Registry result (for verification):
```
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer
  NoDriveTypeAutoRun = 0xFF (255)
  NoAutorun = 1
```
Check: `reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer`.

## Context
- Modern Windows already ignores `autorun.inf` executables on USB drives (since Windows 7 update KB971029), but CD/DVD and ISO-mounted media and AutoPlay prompts remain - users clicking "Run setup.exe" from the prompt is the risk.
- Mounted ISO/VHD files behave like optical media: combine with blocking ISO/IMG attachments at the mail gateway.

## Gotchas
- User-level policy can be overridden by machine-level and vice versa; set at machine level.
- Kiosks and specialised devices may rely on AutoPlay (media players); document exceptions.

## Verify
- [ ] Policy present on sample machines (registry values above).
- [ ] Inserting a test USB and test ISO shows no AutoPlay prompt.
