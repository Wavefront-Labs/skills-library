---
id: computing-software.digital-privacy-hygiene.device-hardening.icloud-advanced-data-protection
name: icloud-advanced-data-protection
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, icloud-advanced-data-protection, advanced-data-protection, e2ee-cloud-storage, icloud, end-to-end-encryption, recovery-contact, recovery-key, ios]
level: practitioner
status: docs-checked
description: "Turn on iCloud Advanced Data Protection: prerequisites, recovery methods, sharing limits and web access, so most iCloud data is end-to-end encrypted."
sources:
  - "https://support.apple.com/en-us/108756"
  - "https://support.apple.com/guide/security/advanced-data-protection-for-icloud-sec973254c5f/web"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# iCloud Advanced Data Protection

**Goal:** protect most iCloud data (iCloud Backup, Photos, Notes and more) with end-to-end encryption, so Apple does not
hold the keys.

## Prerequisites
- An Apple Account with two-factor authentication, and a passcode or password on the device.
- Updated software on every device signed in to the account: iOS or iPadOS 16.2, macOS 13.1, watchOS 9.2, tvOS 16.2,
  HomePod software 16.0, iCloud for Windows 14.1 (or later). A device that does not qualify can be removed from the Apple
  Account device list; while ADP is on, you can sign in only on devices that meet these versions.
- At least one recovery method set up during turn-on: a **recovery contact** or a **recovery key** (a 28-character code
  used with a trusted phone number and an Apple device).
- Managed Apple Accounts and child accounts are not eligible.
- See `computing-software.digital-privacy-hygiene.two-factor-auth.apple-recovery-key-and-recovery-contact`.

## Turn on
- iPhone or iPad: Settings > your name > iCloud > Advanced Data Protection > Turn on Advanced Data Protection.
- Mac: System Settings > your name > iCloud > Advanced Data Protection > Turn On.
Turning it on for one device enables it for the whole account and all compatible devices. Follow the onscreen recovery
setup. You can turn it off at any time; the keys are then uploaded to Apple servers again.

## Limits
- With ADP on, Apple cannot help recover your end-to-end encrypted data; use your device passcode or password, recovery
  contact or recovery key.
- iCloud.com web access is disabled; if you turn it back on, a trusted device approves temporary access.
- End-to-end encryption for shared content holds while all participants have ADP. iWork collaboration, Shared Albums in
  Photos and "anyone with the link" sharing do not support ADP and stay on standard data protection.

## Verify
- [ ] Settings > your name > iCloud shows Advanced Data Protection on.
- [ ] Recovery contact or recovery key set up and stored safely.

## Checked
2026-10-28. Confirmed on Apple Support 108756: prerequisites and versions, recovery methods, turn-on and turn-off paths,
web access, sharing limits. Removed (not confirmed on the fetched pages): the country availability and UK claim, the list of
non-end-to-end-encrypted categories, metadata claims, the "20+ categories" count.
Method: documentation only; no commands were run.
