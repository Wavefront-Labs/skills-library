---
id: computing-software.digital-forensics-incident-response.evidence-handling.mobile-device-acquisition-and-forensics
name: mobile-device-acquisition-and-forensics
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [mobile-forensics, cellebrite, ufed, oxygen-forensics, xry, logical-extraction, filesystem-extraction, physical-extraction, ios-forensics, android-forensics, full-disk-encryption, lock-bypass, faraday-bag, airplane-mode, itunes-backup, adb-backup, chip-off, jtag, dfir]
level: advanced
status: draft
description: "Acquire mobile devices soundly: isolate from the network, pick logical/filesystem/physical extraction, know what each tier actually recovers, and when backup-based acquisition is the ceiling."
sources: ["https://www.cellebrite.com/en/ufed-ultimate/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mobile device acquisition and forensics

**Goal:** get the most complete, legally sound extraction a device and its lock state
actually permit, and know the ceiling before promising a client/court more than modern
full-disk encryption allows.

## 1. First contact: isolation, not acquisition
- **Network-isolate immediately**: airplane mode if the screen is accessible and
  unlocked, or a Faraday bag/box if not. The goal is preventing remote wipe (Find
  My/Find My Device), new data arriving mid-acquisition, and the device re-locking via
  a remote lock command — not preserving battery.
- If the device is **on and unlocked**, do not let it lock before you've either
  captured the passcode in device settings, enabled USB debugging (Android) /
  trusted-computer pairing (iOS), or started extraction. A locked modern device with
  FDE and no known passcode is frequently unrecoverable at full-filesystem depth.
- Note exact state at seizure (on/off, locked/unlocked, airplane mode, SIM present) in
  the chain-of-custody record — see
  computing-software.digital-forensics-incident-response.evidence-handling.forensic-acquisition-and-chain-of-custody.

## 2. The three extraction tiers (know what each buys you)
- **Logical extraction** — pulls data through the OS's own APIs/backup mechanism
  (iTunes/Finder encrypted backup, Android `adb backup` or vendor backup agents).
  Fastest, works without jailbreak/root, but limited to what the backup format
  exposes — no deleted data, often missing third-party app data the backup excludes.
- **Filesystem extraction** — a full copy of the accessible filesystem (via an
  agent pushed to the device, exploit-based access, or a vendor tool's extraction
  profile). Recovers far more: app sandboxes, SQLite databases (many apps' real
  message/call history lives here, not in the OS's own logs), caches. Requires some
  level of device cooperation (often still passcode-unlocked or jailbroken/rooted).
- **Physical extraction** — a bit-for-bit image of the flash storage, done offline of
  the OS (JTAG, chip-off, or a tool-specific low-level exploit). On older/unencrypted
  devices this recovers deleted data via the same unallocated-space techniques as disk
  forensics (see
  computing-software.digital-forensics-incident-response.autopsy-sleuthkit.file-carving-and-unallocated-space-recovery).
  On a modern iOS/Android device with FDE tied to a Secure Enclave/TEE and the
  passcode, a physical image without the key is encrypted ciphertext — physical
  extraction regained real value only where a specific, versioned exploit chain
  exists; this moves constantly and must be checked against current vendor
  (Cellebrite/GrayKey/Oxygen) support matrices for the exact device/OS build, not
  assumed.

## 3. When you can't get past the lock
Logical/backup-based acquisition is often the ceiling on a modern, locked, patched
device. Don't let "we have a tool" create an expectation the specific device/OS
version can't meet — check the vendor's current device support matrix for that exact
model and OS/security-patch level before committing to a timeline or a client
promise. A backup-based extraction, while limited, still yields contacts, messages
(for apps that back up database content), call logs, photos and app data for apps
that don't explicitly exclude themselves from backup.

## 4. Parsing
Run extraction output through a parser (Cellebrite Physical Analyzer, Oxygen Forensic
Detective, or open tools like `iLEAPP`/`ALEAPP` for logical/filesystem iOS/Android
extractions) rather than manually walking SQLite databases — app database schemas
change between versions and a maintained parser tracks that; manual SQL queries
against `sms.db`/`contacts2.db`-style files are a reasonable fallback when no parser
supports a specific app, but validate column interpretation against a test device on
the same app version first.

## Verify
- Document the extraction tier obtained (logical/filesystem/physical) and why — this
  determines what conclusions ("no messages exist" vs "no messages exist in the
  backup, physical extraction was not possible") are actually supportable.
- Hash the extraction output file itself where the tool supports it, same as any other
  acquisition.
- Validate at least one parsed artefact (a known message, a known contact) against the
  device's own UI (if still accessible) or a second parser before relying on parsed
  output for a key finding.

Unconfirmed: current exploit/jailbreak support for specific iOS/Android build numbers
changes monthly — verify against the vendor's live support matrix at the time of the
case, never from memory or an older engagement.
