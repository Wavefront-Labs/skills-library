---
id: computing-software.digital-privacy-hygiene.device-hardening.installing-and-living-with-grapheneos
name: installing-and-living-with-grapheneos
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, grapheneos, android, pixel, verified-boot, sandboxed-google-play, auditor, hardened-os]
level: advanced
status: draft
description: "Install GrapheneOS on a supported Pixel with the web installer, re-lock the bootloader, verify with Auditor, and set up profiles and sandboxed Google Play."
sources:
  - "https://grapheneos.org/install/web"
  - "https://grapheneos.org/usage"
  - "https://grapheneos.org/features"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Installing and living with GrapheneOS

**Goal:** a hardened, privacy-focused Android on Pixel hardware, without losing the security model of a
locked bootloader.

## Before you start
- Supported devices only: recent Google Pixels (check grapheneos.org/faq#supported-devices). Carrier-locked
  Pixels (some Verizon models) cannot unlock the bootloader.
- Back up: unlocking wipes the phone.
- Check your banking/government apps against community compatibility lists; apps demanding Play Integrity
  "strong" attestation with Google certification may refuse to run.

## Install (web installer)
1. Update stock Android once; Settings > System > Developer options > **OEM unlocking** on.
2. Boot to fastboot (power + volume down), connect to a Chromium browser at grapheneos.org/install/web.
3. **Unlock bootloader**, download and flash the factory images.
4. **Lock the bootloader** from the installer (essential; an unlocked bootloader removes verified boot).
5. Boot, then turn **OEM unlocking** back off in Developer options.
At each boot a yellow notice shows a key fingerprint; compare it with the one published on the install page.

## Verify the install
Install **Auditor** on a second Android phone; pair to get hardware attestation that the OS is genuine and the
bootloader locked. Scheduled remote attestation is available.

## Configure
- **Sandboxed Google Play** (App Store app) only where needed, ideally in a secondary user profile.
- Per-app **Network** and **Sensors** permissions; **Storage Scopes** and **Contact Scopes** to give apps fake/limited views.
- Settings > Security & privacy > Exploit protection > **Auto reboot** timer; **USB-C port** set to charging only when locked.
- Duress PIN/password wipes the device when entered.

## Gotchas
- Never relock the bootloader with a non-GrapheneOS image flashed; it can brick.
- Updates are OTA and automatic; reboot when prompted.

## Verify
- [ ] Bootloader locked (no orange warning); Auditor reports genuine; OEM unlocking off.
