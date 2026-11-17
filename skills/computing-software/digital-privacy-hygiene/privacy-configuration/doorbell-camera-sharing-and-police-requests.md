---
id: computing-software.digital-privacy-hygiene.privacy-configuration.doorbell-camera-sharing-and-police-requests
name: doorbell-camera-sharing-and-police-requests
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, doorbell-camera-privacy, ring, police-requests, neighbors-app]
level: practitioner
status: draft
description: "Control how doorbell camera footage is shared with neighbours apps and police, what emergency requests allow, and settings that limit disclosure."
sources:
  - "https://www.eff.org/deeplinks"
  - "https://support.ring.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Doorbell camera sharing and police requests

**Goal:** you decide when footage leaves your account, and you know when the company can share it without asking.

## How footage reaches others
1. **You share** it: neighbourhood apps (Ring Neighbors, Nextdoor), social media, or direct to police.
2. **Police request through the platform**: Ring's Request for Assistance tool was retired in January 2024; since then
   Ring has introduced new partner-based public safety request features. Check the app's current settings
   (Control Center or privacy settings) for any "public safety" or "community requests" options and opt out if
   desired.
3. **Legal process**: warrants and subpoenas served on the company.
4. **Emergency disclosure**: Ring disclosed in 2022 that it had given footage to police without owner consent in
   emergency cases; Google Nest has similar emergency exceptions.

## Limit disclosure
- Enable **end-to-end encryption** (Ring Video E2EE; HomeKit Secure Video): the company can't decrypt stored video,
  so it cannot hand it over. Some features stop working.
- Use **local storage** where possible.
- Shorten cloud retention (video history length) and delete old clips.
- Turn off audio recording if you don't need it; recording conversations can also breach wiretap laws.
- Don't auto-post to Neighbors; review each clip before sharing and blur faces of passers-by.

## Placement
Point the camera at your door and path, not the street or neighbours; footage of public spaces is more likely to be
requested.

## Gotchas
Sharing a clip with police once may include metadata like your address and allow further requests.
