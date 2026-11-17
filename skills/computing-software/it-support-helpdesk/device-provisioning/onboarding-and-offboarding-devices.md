---
id: computing-software.it-support-helpdesk.device-provisioning.onboarding-and-offboarding-devices
name: onboarding-and-offboarding-devices
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, onboarding, offboarding, joiners-movers-leavers, windows-autopilot, pre-provisioning, white-glove, hardware-hash, zero-touch, apple-ade, apple-business-manager, android-zero-touch, knox-mobile-enrollment, imaging, mdt, sccm, configuration-manager, naming-convention, asset-tag, cmdb, mfa-enrolment, revoke-sessions, shared-mailbox, remote-wipe, activation-lock, factory-reset-protection, nist-800-88, data-sanitisation, chain-of-custody, leaver-checklist]
level: practitioner
status: draft
description: "Provision and retire end-user devices: modern provisioning vs imaging, Autopilot hash and pre-provisioning, naming and CMDB, a day-one checklist, ordered offboarding, wipe, NIST 800-88 sanitisation."
sources:
  - "https://learn.microsoft.com/en-us/autopilot/overview"
  - "https://csrc.nist.gov/pubs/sp/800/88/r1/final"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Onboarding and offboarding devices

**Goal:** a new starter gets a secure, working device on day one with no manual build,
and a leaver's access and data are cut off in the right order with the hardware either
safely reused or provably sanitised.

## 1. Standard build: modern provisioning over imaging
- **Modern / zero-touch:** the device ships from the vendor, the user signs in, and MDM
  applies config and apps — Windows Autopilot, Apple Automated Device Enrollment (via
  Apple Business Manager), Android zero-touch or Samsung Knox Mobile Enrollment.
- **Imaging (legacy):** capture-and-deploy with MDT or Configuration Manager (SCCM/MECM)
  task sequences. Microsoft has announced MDT's retirement (verify current support
  status); keep it only for estates that can't yet go cloud-native. ConfigMgr is still
  supported, commonly in co-management with Intune.
- Define the **standard build** as config, not as an image: OS edition/version, security
  baseline, BitLocker/FileVault, core apps, Defender/EDR, update rings.

## 2. Windows Autopilot specifics
- Vendors/resellers can register devices for you; otherwise capture the **hardware hash**:
  ```
  Install-Script -Name Get-WindowsAutopilotInfo
  Get-WindowsAutopilotInfo -OutputFile AutopilotHWID.csv
  ```
  then import the CSV in Intune (Devices › Enrollment › Windows Autopilot devices). The
  community script has changed over time (newer versions use Microsoft Graph and an
  `-Online` switch); check the current version's parameters.
- Newer **Autopilot device preparation** profiles don't require hash pre-registration;
  check which flavour your tenant uses.
- **Pre-provisioning** (formerly *white glove*): IT or the reseller presses the Windows
  key **five times** at the OOBE screen, chooses pre-provision, and device-targeted apps
  and policies install before shipping; the user only does the user phase. Needs TPM 2.0
  with attestation and wired network is advised.
- **Naming:** Autopilot profiles accept templates like `<PREFIX>-%SERIAL%` or
  `<PREFIX>-%RAND:5%`; Windows names max out at **15 characters**. Encode
  org/site/type, never a person's name (devices get reassigned).

## 3. Asset tagging and CMDB
Record serial, asset tag, model, purchase date, warranty end, assigned user, state
(*In stock › Assigned › In repair › Retired › Disposed*). Prefer automated import from
Intune/ABM into the CMDB so it isn't hand-maintained. Every state change has a ticket.

## 4. Day-one checklist
- [ ] Account active, licensed, in the right groups (drives apps and policies).
- [ ] Temporary Access Pass or supervised first sign-in; **MFA/passkey registered** on
  day one.
- [ ] Device enrolled, compliant, encryption confirmed (recovery key escrowed in
  Entra/Intune or ABM).
- [ ] Required apps installed; mailbox, Teams, OneDrive syncing.
- [ ] Printers, VPN, Wi-Fi certs, phone/softphone working.
- [ ] User shown the self-service portal and how to raise a ticket.

## 5. Offboarding sequence (order matters)
1. **Disable the account** at the agreed time (coordinate with HR; for hostile exits,
   while the meeting happens). Reset password.
2. **Revoke sessions and tokens:** Entra user › *Revoke sessions* (or
   `Revoke-MgUserSignInSession`), remove MFA methods, revoke app passwords and OAuth
   grants, disable on-prem AD too if hybrid.
3. **Transfer data:** convert the mailbox to **shared** and grant the manager access (a
   shared mailbox needs no licence up to the size limit — check current limits); set
   auto-reply; grant OneDrive access before its retention period expires. Check legal
   holds before deleting anything.
4. **Device action:** corporate → **wipe**; personal BYOD → **retire** (company data only).
5. **Collect hardware**, then remove licences and groups.
6. If the device is being **disposed of or resold**: delete it from Autopilot, release it
   from ABM and zero-touch, otherwise it re-enrols into your tenant for the next owner.

## 6. Locks that brick reused devices
- **Apple Activation Lock:** supervised devices allow an MDM bypass code; personal Apple
  accounts must sign out of Find My before return.
- **Android Factory Reset Protection:** a reset outside MDM demands the last Google
  account. Remove accounts or use an MDM wipe; corporate devices can set enterprise FRP.

## 7. Data sanitisation (NIST SP 800-88)
- **Clear** — logical overwrite/factory reset; fine for reuse inside the org.
- **Purge** — cryptographic erase or firmware sanitize commands; for leaving your control.
  For SSDs, overwriting is not a reliable purge; use crypto erase/ATA/NVMe sanitize.
- **Destroy** — shred/disintegrate; for failed drives or the highest sensitivity.
Use a vendor providing **certificates of sanitisation** per serial. Maintain **chain of
custody**: who held the device, when, sealed containers, signed handovers. NIST published
Rev. 1 in 2014 and has since issued a revision; check the current edition.

## Gotchas
- Wiping before revoking sessions leaves cloud tokens alive on other devices.
- Deleting a user immediately can delete OneDrive data on the retention clock.
- Hash-registered but unassigned devices get no profile; check group membership.

## Verify
- [ ] New device: compliant, encrypted, MFA registered, apps present, CMDB updated.
- [ ] Leaver: sign-ins blocked, sessions revoked, mailbox shared, data owner named.
- [ ] Disposed device removed from Autopilot/ABM/zero-touch and lock-free.
- [ ] Sanitisation certificate and custody record attached to the ticket.
