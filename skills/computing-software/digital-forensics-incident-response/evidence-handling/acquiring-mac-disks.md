---
id: computing-software.digital-forensics-incident-response.evidence-handling.acquiring-mac-disks
name: acquiring-mac-disks
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [mac-disk-acquisition, macos-forensics, apfs-forensics, disk-imaging, dfir]
level: advanced
status: draft
description: "Acquire Mac storage on T2 and Apple silicon: why removal fails, target disk / share disk mode, live logical collection, FileVault and APFS snapshot handling."
sources: ["https://support.apple.com/guide/mac-help/transfer-files-between-two-mac-computers-mchlb37e8ca7/mac", "https://support.apple.com/guide/security/secure-enclave-sec59b0b31ff/web", "https://developer.apple.com/support/downloads/Apple-File-System-Reference.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Acquiring Mac disks

**Goal:** on Macs with T2 or Apple silicon, internal storage is soldered and hardware-encrypted
by the Secure Enclave; physical chip-off yields nothing. Acquisition must go through macOS.

## Decide first
- Is the Mac running and logged in? A live, unlocked Mac is the best opportunity: collect
  logically now (FileVault keys are in use).
- Do you have the user's password / FileVault recovery key? Without it, a powered-off Mac with FileVault is generally inaccessible.

## Methods
| Method | When | Result |
|---|---|---|
| Live logical collection (Aftermath, mac_apt live, commercial tools like Cellebrite Digital Collector / Recon ITR) | Running, unlocked | Decrypted files, unified logs, user data |
| **Target Disk Mode** (Intel/T2) | Powered off, password known | Mac appears as disk to another Mac over Thunderbolt; image the unlocked APFS volume |
| **Share Disk mode** (Apple silicon, macOS Recovery > Share Disk) | Powered off, user password known | Exposes the volume over SMB-like file sharing; logical (file-level) only |
| Recovery-mode boot with signed tooling | Approved tools only | Logical acquisition of APFS volumes |

## APFS specifics
- Image or collect the **Data** volume; System volume is sealed and identical to Apple's release.
- List and preserve local snapshots (`tmutil listlocalsnapshots /`); they hold earlier file versions.
- Record `diskutil apfs list` output (container, volumes, encryption state, FileVault status).

## Gotchas
- Powering off a running unlocked Mac loses access if you lack credentials.
- Share Disk gives files, not a block image: no unallocated space (which on APFS SSDs with TRIM has little value anyway).
- Activation Lock / MDM may block Recovery tools; coordinate with the MDM admin.

## Verify
Collection logs show method, volumes collected, encryption status, and hash manifest of collected files.
