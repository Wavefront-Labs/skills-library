---
id: computing-software.digital-privacy-hygiene.device-hardening.detecting-stalkerware-on-phones
name: detecting-stalkerware-on-phones
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, stalkerware, malware, malware-protection, intimate-partner-surveillance, device-admin-apps, accessibility-abuse, mdm-profile, safety-check]
level: practitioner
status: draft
description: "Check a phone for stalkerware or abusive monitoring (device admin, accessibility, MDM profiles, shared accounts) safely, considering that removal can alert the abuser."
sources:
  - "https://stopstalkerware.org/"
  - "https://ssd.eff.org/module/how-do-i-protect-myself-against-malware"
  - "https://support.apple.com/guide/personal-safety/welcome/web"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Detecting stalkerware on phones

**Goal:** find covert monitoring apps or account-level spying installed by someone with
physical access (often a partner), without escalating danger.

## Safety first
If you suspect an abusive partner, **removing** monitoring can alert them and escalate.
Contact a domestic violence advocate (e.g. via the Coalition Against Stalkerware's
resources) and plan before acting; consider using a different, safe device for research.

## Android checks
- Settings > Security > **Device admin apps**: anything you don't recognise.
- Settings > Accessibility > **installed services** with full control (stalkerware abuses
  this to read screens).
- Settings > Apps > show system apps: unfamiliar names ("System Service", "Sync Services"),
  apps with no icon; check **Special app access** (notification access, usage access,
  display over other apps).
- Play Protect > scan; it flags known stalkerware.
- "Unknown sources" permission granted to a browser or file manager.

## iPhone checks
Stalkerware apps are rare on non-jailbroken iPhones; abuse is usually **account-level**:
- Settings > General > **VPN & Device Management**: unknown profiles.
- Settings > Privacy & Security > **Safety Check** > Manage Sharing & Access: review who
  sees your location, shared albums, and which devices are signed in.
- Apple Account device list; Find My sharing; iCloud password known by someone else.
- Jailbreak signs: Cydia/Sileo apps.

## Account-level spying (both)
Shared Google/Apple passwords, family-sharing location, forwarding rules in email,
linked WhatsApp/Signal devices.

## Remedies
Change account passwords from a safe device, sign out other sessions, remove profiles/apps
(when safe), or factory reset and set up as new (don't restore a backup that may contain
the app).

## Verify
- [ ] No unknown device admin, accessibility services, profiles, or linked devices.
