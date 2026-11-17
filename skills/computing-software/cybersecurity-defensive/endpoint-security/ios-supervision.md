---
id: computing-software.cybersecurity-defensive.endpoint-security.ios-supervision
name: ios-supervision
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [ios-supervision, supervised-mode, automated-device-enrollment, apple-business-manager, ipados, restrictions, mobile-device-management]
level: practitioner
status: docs-checked
description: "Supervise corporate iPhones and iPads: Automated Device Enrollment, manual supervision with Configurator, non-removable enrolment and supervised-only security restrictions."
sources: ["https://support.apple.com/guide/deployment/about-device-supervision-dep1d89f0bff/web", "https://support.apple.com/guide/deployment/automated-device-enrollment-dep73069dd57/web", "https://support.apple.com/guide/deployment/restrictions-for-iphone-and-ipad-devices-dep0f7dd3d8/web"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# iOS supervised device policies

Apple: supervision generally means the organisation owns the device, giving more control over configuration and restrictions. Check status on iPhone/iPad in Settings, where a supervision notice appears below the Search field; the notice says the organisation can monitor internet traffic and locate the device.

## Get devices supervised
- **Automated Device Enrollment (ADE)**: devices registered in Apple School Manager or Apple Business are supervised automatically on enrolment. Each setting has a minimum OS version; the service can also enforce a minimum OS, and below it the device is guided through an update before Setup Assistant continues.
- **Manual**: Apple Configurator for Mac, device physically in hand, for iPhone, iPad and Apple TV. This erases the device.
- ADE can prevent users removing the management enrolment profile (Prevent unenrollment, iOS 7+). Apple: a supervised device cannot be unenrolled by the user.
- Setup Assistant: choose which panes to skip; "Hold device in Setup Assistant" lets the service apply critical configuration or apps first; a configuration web URL can load during setup for authentication, branding or consent text.
- Highly Restricted Networks mode needs iOS/iPadOS 17+, Apple approval in Apple Business and a compatible management service.

## Supervised-only restrictions worth considering
From Apple's restrictions table (marked supervised):
- Install a configuration profile; Erase All Content and Settings; Modify passcode; Modify restrictions or Screen Time settings; Modify account settings.
- Allow accessory connections / connected accessories while locked; Pair with non-Apple Configurator hosts; Allow Recovery Mode from an unpaired host (on by default in iOS/iPadOS 14.5+).
- Allow NFC; AirDrop; Add VPN configurations; Join only Wi-Fi networks installed by a Wi-Fi payload (device cannot be managed if that network is unavailable).
- Modify Face ID/Touch ID; Share passwords; Password AutoFill; Proximity AutoFill; Force preservation of eSIM on erase.
- Allow app installation from a website or alternative marketplace; Install apps; Remove apps.
- Not requiring supervision, but useful: Force encrypted backups, Force fraud warning, Users accept untrusted TLS certificates, Trust new proprietary in-house app developers, Allow App to Request to Track.

## Gotchas
- Personal devices: Apple's supervision page does not cover User Enrolment; do not supervise personal devices.
- Joining only managed Wi-Fi can leave devices unmanageable off that network.
- Not covered by these pages, so verify elsewhere: Activation Lock handling, Lost Mode, software-update deadlines, a 30-day provisional period for Configurator, and Lockdown Mode enforcement.

## Verify
- [ ] MDM inventory shows Supervised and the enrolment profile non-removable for corporate devices.
- [ ] Chosen supervised restrictions confirmed on a test device.

## Checked
Method: 2026-11-08 read the three Apple deployment pages; removed unsupported claims (30-day removal window, Activation Lock, Lost Mode, DDM update deadlines, Lockdown Mode, allowHostPairing key, managed open-in) and rebuilt the restriction list from Apple's table. ADE and supervision claims unchanged in substance.
