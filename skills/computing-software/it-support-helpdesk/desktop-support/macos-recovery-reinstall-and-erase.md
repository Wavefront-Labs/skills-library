---
id: computing-software.it-support-helpdesk.desktop-support.macos-recovery-reinstall-and-erase
name: macos-recovery-reinstall-and-erase
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, macos-reinstall, macos-recovery, erase-all-content-and-settings, apple-silicon, activation-lock, dfu, macos-startup-options, dfu-restore]
level: practitioner
status: draft
description: "Reinstall or erase macOS correctly on Apple silicon and Intel: Recovery startup keys, reinstall that keeps data, Erase All Content and Settings, activation lock and DFU revive."
sources:
  - "https://support.apple.com/en-us/102655"
  - "https://support.apple.com/en-us/102664"
  - "https://support.apple.com/en-us/102506"
  - "https://support.apple.com/guide/apple-configurator-mac/revive-or-restore-a-mac-with-apple-silicon-apdd5f3c75ad/mac"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# macos-recovery-reinstall-and-erase

## Get into Recovery
| Mac | How |
|---|---|
| Apple silicon | Shut down, hold the power button until "Loading startup options", choose Options |
| Intel | `Cmd`+`R` (installed version), `Option`+`Cmd`+`R` (latest compatible), `Shift`+`Option`+`Cmd`+`R` (original/closest) |

If local Recovery is damaged, Intel Macs fall back to Internet Recovery; Apple silicon
uses fallback recovery (press power twice and hold) or a DFU revive.

## Reinstall without erasing
Recovery > Reinstall macOS. Keeps users and data, replaces the system. Use for a broken
OS, failed update, or missing system files. Needs network; FileVault volumes need a user
password or recovery key to unlock first.

## Erase and reset
- Preferred (Apple silicon or T2, macOS 12+): System Settings > General > Transfer or
  Reset > **Erase All Content and Settings**. It removes data, users and Apple ID while
  keeping the OS, and signs out of Find My.
- Otherwise: Recovery > Disk Utility > select the internal volume group (View > Show All
  Devices) > Erase as APFS, then Reinstall macOS.
- MDM-managed: an Intune/Jamf wipe does the same remotely; ADE devices re-enrol at Setup
  Assistant.

## Activation Lock
A Mac tied to a personal Apple ID stays locked after erase. Remove the Mac from the
user's Find My before reissue, or use the MDM activation lock bypass code for supervised
devices (see clearing-activation-lock-and-account-locks).

## DFU revive / restore (Apple silicon)
Connect to another Mac running Apple Configurator, enter DFU mode, then **Revive**
(reinstalls firmware/recoveryOS, keeps data) or **Restore** (erases everything).

## Gotchas
- Erasing just "Macintosh HD" leaves the Data volume; erase the volume group.
- Apple silicon needs an admin user from that Mac to authorise Recovery actions
  ("owner"); a wiped user list makes this harder.

## Verify
Mac boots to Setup Assistant (erase) or to the user's login (reinstall), shows the
expected macOS version, and re-enrols in MDM where applicable.
