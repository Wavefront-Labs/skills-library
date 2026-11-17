---
id: computing-software.digital-privacy-hygiene.privacy-configuration.journalist-source-protection
name: journalist-source-protection
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, source-protection, journalism, securedrop, metadata]
level: practitioner
status: draft
description: "Protect confidential sources: secure first contact, SecureDrop and Signal practice, metadata in documents and printers, devices, and handling legal demands."
sources:
  - "https://securedrop.org/"
  - "https://freedom.press/digisec/"
  - "https://ssd.eff.org/playlist/journalist-move"
  - "https://cpj.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Source protection for journalists

**Goal:** a source's identity can't be recovered from your communications, files or devices.

## First contact
- Publish secure contact options (Signal username, SecureDrop onion address, a dedicated email) on your profile so
  sources don't use work email, work phones or social media DMs.
- Sources should contact from personal devices on networks not linked to their employer.

## Channels
- **SecureDrop**: anonymous document submission over Tor; newsroom reads on an air-gapped Secure Viewing Station.
- **Signal** with usernames (hide phone numbers), disappearing messages, and verified safety numbers.
- Avoid ordinary phone calls and SMS; call records are easily subpoenaed.

## Documents
- Strip metadata before publishing (`mat2`, Dangerzone for converting).
- Don't publish original scans: printer **tracking dots** and unique formatting identified a source in 2017; retype or
  describe instead.
- Watch for canary traps (different versions sent to different people).

## Your devices and accounts
- Full-disk encryption, strong passcode, Lockdown Mode if high-risk, a separate device for sensitive work.
- Don't store sources in synced contacts; keep notes encrypted and minimal; consider what cloud backups contain.
- Plan for border crossings and device seizure.

## Legal
Know shield laws in your jurisdiction and your newsroom's lawyers' process for subpoenas; data you don't keep can't be
compelled.
