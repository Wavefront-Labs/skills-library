---
id: computing-software.digital-privacy-hygiene.device-hardening.apple-safety-check
name: apple-safety-check
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, safety-check, ios, iphone-security, emergency-reset, manage-sharing-and-access, location-sharing-audit, personal-safety, tech-safety-plan]
level: intro
status: docs-checked
description: "Use iPhone Safety Check to review or stop sharing information and app access with other people, with Quick Exit and a safety-first note."
sources:
  - "https://support.apple.com/guide/personal-safety/how-safety-check-works-ips2aad835e1/web"
  - "https://support.apple.com/en-us/105102"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Apple Safety Check

**Goal:** a single place to review and stop what other people and apps can access through your iPhone. Designed for people
in abusive relationships, useful for anyone after a breakup or shared-device period.

## Open
iPhone with iOS 16 or later: Settings > Privacy & Security > **Safety Check** (you may need to scroll). **Quick Exit**
(top-right on every Safety Check screen) closes Settings and returns to the Home Screen immediately; changes made before it
are saved.

## Two modes
- **Emergency Reset**: immediately and universally stops sharing with all people and apps, and lets you change your
  Apple Account password and review device and account security. Progress is saved as you go.
- **Manage Sharing & Access**: review and customise sharing with individual people and what apps can access, and update
  device and Apple Account security. Changes are saved as you go.

## Limits
- With Screen Time restrictions or an MDM profile installed, some options may not be available.
- With Stolen Device Protection on, Safety Check may work a little differently.
- It cannot review or change some types of shared information; Apple's page lists them under "Beyond Safety Check".
- On iPad or Mac use Apple's manual sharing checklists in the Personal Safety guide.
- To restart sharing later, share again from the app or service; some apps notify the other person.

## Before you act
Stopping sharing may be noticed. If safety is a concern, plan with an advocate first (see
`computing-software.digital-privacy-hygiene.privacy-configuration.tech-safety-plan-when-leaving-an-abusive-relationship`).

## Verify
- [ ] Reopen Safety Check afterwards and confirm no unexpected people or apps remain.

## Checked
2026-10-28. Confirmed in the Apple Personal Safety guide (How Safety Check works): iOS 16 requirement, path, Quick Exit,
both modes and what Emergency Reset does, MDM and Screen Time limits, Stolen Device Protection note, iPad and Mac checklists.
Removed (not confirmed): signing out of iCloud on other devices, resetting all app privacy permissions, the per-category
sharing list, and the AirTag and Messages follow-up checks.
Method: documentation only; no commands were run.
