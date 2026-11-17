---
id: computing-software.digital-privacy-hygiene.privacy-configuration.clearing-iphone-significant-locations
name: clearing-iphone-significant-locations
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, significant-locations, location, ios, macos, location-history, stalkerware]
level: intro
status: docs-checked
description: "Find and turn off iPhone Significant Locations, the record of places you visit most; know its Stolen Device Protection side effect and use Safety Check."
sources:
  - "https://ssd.eff.org/module/how-to-get-to-know-iphone-privacy-and-security-settings"
  - "https://support.apple.com/en-us/102515"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clearing iPhone Significant Locations

**Goal:** stop the iPhone keeping a list of the places you go most (home, work, clinic, a friend's house). Labels
follow the EFF guide (written for iOS 26); the exact Clear History button is not described in the cited pages, so
look for it on the Significant Locations screen.

## Where it is
iPhone: Settings > Privacy & Security > Location Services > scroll to the bottom > **System Services** >
**Significant Locations** (EFF: it stores the locations you go to most often, and is worth considering turning off).

## Side effect to know first
If you use **Stolen Device Protection** (Settings > Face ID & Passcode > Turn On Protection) with the security delay set
to **Away from Familiar Locations**, it is not applied at Significant Locations; EFF notes that turning Significant
Locations off means that option will not work.

## Why it matters
EFF describes System Services as operating-system-level services that mostly communicate with Apple directly, and
Significant Locations as the one that stores the places you visit most. Weigh it against your threat model, for example
a device you share or a partner who can unlock your phone.

## Review sharing at the same time
Settings > Privacy & Security > **Safety Check** offers:
- **Emergency reset**: stops sharing everything, including information with other people and app permissions,
  immediately.
- **Manage Sharing & Access**: a three-step review of data shared with people, app access and other information such
  as emergency contacts, with an option to reset your passcode and account password.
A **Quick Exit** button returns to the Home Screen and keeps progress. People you stop sharing location with may notice.

## Verify
- [ ] Significant Locations is off (or you chose to keep it, knowingly).
- [ ] Stolen Device Protection setting reviewed.

## Checked
Checked 2026-11-08 against the full text of the EFF "Get to Know iPhone Privacy and Security Settings" guide (last
reviewed 2025-09-15) and Apple Support 102515. Removed what they do not state: the Clear History behaviour and
cross-device scope, the Mac path, Calendar, Maps and Photos side effects, the end-to-end encryption claim, the Maps
Recents, camera geotag and Find My steps, and the Apple Personal Safety guide's checklist (the cited page is only a
contents page, and the iPhone guide link redirected to a welcome page, so both were dropped from sources).
Method: documentation only; no commands were run.
