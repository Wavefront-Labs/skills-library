---
id: computing-software.cybersecurity-defensive.security-operations.mobile-device-forensic-acquisition
name: mobile-device-forensic-acquisition
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [mobile-forensics, digital-forensics, ios, android, mobile-verification-toolkit, evidence-acquisition, mdm]
level: advanced
status: draft
description: "Acquire mobile device evidence (iOS, Android): isolation, logical/full-file-system extraction options, backups, MDM data, iVerify/MVT checks and documentation."
sources: ["https://csrc.nist.gov/pubs/sp/800/101/r1/final", "https://docs.mvt.re/en/latest/", "https://www.swgde.org/documents/published-complete-listing"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Mobile device acquisition

## Seizure and isolation
- Keep the device powered as found when possible; if unlocked, keep it unlocked (disable auto-lock
  if policy allows) because "After First Unlock" state permits far richer extraction than "Before
  First Unlock".
- Isolate from networks: Faraday bag or airplane mode (document the action) to stop remote wipe;
  for corporate devices, also block remote wipe in MDM.
- Photograph screen state, record model, OS version, IMEI/serial, SIM.

## Acquisition levels (NIST SP 800-101)
1. **Manual**: photograph screens (last resort).
2. **Logical**: iTunes/Finder encrypted backup (iOS, set a backup password to include keychain
   and health data), Android ADB backup (deprecated), vendor tools' logical extraction.
3. **Full file system**: commercial tools (Cellebrite, GrayKey, Magnet) via exploits/agents;
   requires authorisation and vendor tooling.
4. **Physical/chip-off**: rarely possible on modern encrypted devices.

## Corporate context
- MDM (Intune, Jamf) data: device inventory, app list, compliance history, location if enabled.
- Cloud accounts: iCloud/Google Takeout exports with user consent or legal process; Entra sign-in
  logs for the device.
- Spyware checks: Mobile Verification Toolkit (`mvt-ios check-backup --iocs <stix2> <backup_dir>`,
  `mvt-android check-adb`) with Amnesty/Citizen Lab IOCs.

## Documentation
Every action timestamped, tools and versions, hashes of extraction outputs, chain of custody form.

## Gotchas
- Personal devices need consent or legal authority; do not image BYOD without it.
- Rebooting an iPhone returns it to BFU state; avoid unless necessary.
- Encrypted iOS backup password lost = backup unusable; record it in case notes.

## Verify
Extraction hash recorded and re-verified at analysis start; acquisition report lists method,
device state, and any data categories not obtainable.
