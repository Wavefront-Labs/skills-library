---
id: computing-software.digital-privacy-hygiene.device-hardening.hardware-encrypted-usb-drives
name: hardware-encrypted-usb-drives
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, hardware-encrypted-usb, encrypted-storage, fips-140-3, removable-media]
level: practitioner
status: draft
description: "Choose and use a keypad PIN hardware-encrypted USB drive: certification to look for, brute-force wipe, admin and user PINs, and its limits."
sources:
  - "https://csrc.nist.gov/projects/cryptographic-module-validation-program"
  - "https://www.kingston.com/en/usb-flash-drives"
  - "https://apricorn.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Hardware-encrypted USB drives with keypad PIN

**Goal:** encrypted portable storage that works on any computer without software or admin rights.

## When to use one
- Moving data between machines you don't control (printers, lab PCs, TVs, cars).
- Giving files to a non-technical person who can type a PIN but won't install VeraCrypt.
- Otherwise, software encryption (BitLocker To Go, FileVault, LUKS, VeraCrypt) on a normal drive is cheaper.

## What to buy
- Look for **FIPS 140-3 Level 3** (or 140-2 Level 3) validation listed on NIST's CMVP site, not just "AES-256" on the
  box. Examples: Kingston IronKey Keypad 200, Apricorn Aegis Secure Key, iStorage datAshur.
- Epoxy-filled internals and a firmware that cannot be updated by the host (resists BadUSB).
- Brute-force protection that wipes after N wrong PINs.

## Setup
1. Set the **admin PIN** (long, stored in your password manager) and optionally a separate **user PIN**.
2. Configure auto-lock timeout and read-only mode if you only need to distribute files.
3. Set the brute-force limit; know that hitting it destroys the key and data.
4. Format the drive after unlocking (exFAT for cross-platform).

## Use
Type the PIN on the keypad, plug in within the timeout, eject before unplugging. The drive locks when unplugged.

## Limits
- Data is readable by the host while unlocked; malware on that PC can copy it.
- Keypads wear: the most-used digits show; use a longer PIN and wipe the keypad.
- The drive is a single copy; back up the data elsewhere.
- Batteries in some models need occasional charging; a dead battery can prevent unlock until charged.
