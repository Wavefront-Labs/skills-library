---
id: computing-software.it-support-helpdesk.apple-device-management.abm-roles-and-locations
name: abm-roles-and-locations
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, abm-setup, abm-roles-and-locations, locations, roles, asm]
level: practitioner
status: draft
description: "Set up Apple Business Manager or School Manager roles, locations and content settings so devices and apps are assigned to the right MDM and site."
sources:
  - "https://support.apple.com/guide/apple-business-manager/welcome/web"
  - "https://support.apple.com/guide/deployment/welcome/web"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# abm-roles-and-locations

Goal: structure an ABM/ASM organisation so purchases and devices land with the correct administrator and MDM.
- Admin roles: Administrator, People Manager, Device Enrolment Manager, Content Manager; give day-to-day staff the narrowest role and keep two Administrators.
- Locations (Settings > Locations) scope Apps and Books purchasing; each location can be tied to one VPP token.
- Enable Managed Apple Accounts, Shared iPad and content settings under Preferences.
- Domain verification (Accounts > Domains) needs a DNS TXT record before federation or account claiming.
Gotcha: the first Administrator is created against a verified organisation (D-U-N-S check); lose every Administrator and recovery goes through Apple support, not your MDM.
Verify:
- At least two Administrators exist with working mailboxes.
- Each location maps to the intended team and token.
- Domain shows Verified.
