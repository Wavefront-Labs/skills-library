---
id: computing-software.digital-privacy-hygiene.device-hardening.preparing-devices-for-a-border-crossing
name: preparing-devices-for-a-border-crossing
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, border-device-search, travel, border, cbp, before-first-unlock, data-minimization]
level: practitioner
status: draft
description: "Prepare phones and laptops for possible border device searches: minimise data, back up, log out of cloud apps, power off, and handle the inspection and aftermath."
sources:
  - "https://www.eff.org/wp/digital-privacy-us-border-2017"
  - "https://www.cbp.gov/travel/cbp-search-authority/border-search-electronic-devices"
  - "https://ssd.eff.org/module/things-consider-when-crossing-us-border"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Preparing devices for a border crossing

**Goal:** limit what can be read if a device is searched or detained at a border, without lying to officials.

## Legal context (check your route)
- US CBP may search devices at the border without a warrant: a **basic** (manual) search, or an **advanced**
  (forensic copy) search with reasonable suspicion under CBP Directive 3340-049A. Officers are told not to access
  cloud-only data and to ask for airplane mode.
- Refusing to unlock can mean the device is detained, and non-citizens may be refused entry. UK Schedule 7 and
  some other regimes criminalise refusal to give passwords.
- Lawyers, doctors and journalists: declare privileged material; officials have special handling procedures.

## Before travel
1. **Back up** everything; you may lose the device for weeks.
2. **Minimise**: remove or log out of apps you do not need on the trip (email, social, messaging histories,
   photos). Consider a dedicated travel device with fresh accounts.
3. Enable full-disk encryption (BitLocker/FileVault/LUKS; phones by default) with a strong passcode.
4. Turn off biometrics before the checkpoint so only a passcode can unlock.
5. **Power off** devices before arrival: they return to Before First Unlock, the hardest state to extract.
6. Remove saved passwords from browsers; keep the password manager locked with a long master password.

## At the checkpoint
- Stay calm and polite; do not lie (false statements are a separate offence). You can ask whether a search is
  basic or advanced, and request a receipt (CBP Form 6051D) if detained.
- If you unlock, you may ask to unlock it yourself rather than state the passcode.
- Note officers' names, times and what was done.

## Afterwards
- If the device left your sight, treat it as potentially tampered: reset or reflash where feasible, change
  passwords for accounts that were logged in, check for unknown profiles/apps.
- Restore data from backup once across.

## Verify
- [ ] Backup done, travel set minimal, biometrics off, devices powered off before the border.
