---
id: computing-software.it-support-helpdesk.intune-mdm.ios-company-portal-and-configurator-enrollment
name: ios-company-portal-and-configurator-enrollment
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, company-portal-ios-enrollment, apple-configurator-abm, ios-enrollment, apple-business-manager, byod]
level: practitioner
status: docs-checked
description: "Enroll personal iPhones and iPads in Intune: Company Portal, web-based and account-driven enrollment compared, user steps, requirements, ACME certificates and known issues."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/enrollment/ios-device-enrollment"
  - "https://learn.microsoft.com/en-us/mem/intune/user-help/enroll-your-device-in-intune-ios"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ios-company-portal-and-configurator-enrollment

Scope: user-initiated enrollment of personal iOS/iPadOS devices. Adding devices to Apple Business Manager with Apple Configurator is not covered (the Apple page that skill cited was not readable); see Apple's Business Manager guide.

## Options compared (Intune "Apple device enrollment")
Create the policy at Devices > By platform > iOS/iPadOS > Device onboarding > Enrollment > Enrollment types.
| | App-based (Company Portal) | Web-based |
|---|---|---|
| iOS/iPadOS version | 14 and later | 15 and later |
| Required apps | Company Portal, Microsoft Authenticator | Microsoft Authenticator |
| Where it runs | Company Portal app, Safari, Settings | Safari and Settings |
Both: personal/BYOD devices, single user, user-initiated, no device reset, not supervised, just-in-time (JIT) registration. Web enrollment with JIT registration and the Apple SSO extension is Microsoft's recommended method (no Company Portal install, strongest device attestation); enable JIT by deploying a device configuration profile with an SSO app extension policy. Account-driven user enrollment (Settings > General > VPN & Device Management, iOS/iPadOS 15 or later) is a third option, and the user can choose in Company Portal ("I own this device" > Secure entire device, or Secure work-related apps and data only).

## User steps (Company Portal)
Install Company Portal and the latest Authenticator; sign in; Get started; Safari opens and prompts to Allow the configuration profile download; Settings > Profile Downloaded (or General > VPN & Device Management) > Management Profile > Install (re-enter passcode, accept the warning, Trust); return to Company Portal > Notifications > register the device; accept required app installs (including a mobile threat defense app if required). Keep Wi-Fi on; pausing for more than a few minutes may close setup.
Web enrollment: in Safari go to the Company Portal web enrollment address, sign in, download the profile, install it in Settings, then wait for Authenticator (verify under Profile > Management Profile > Single Sign On Extension).

## What users can do afterwards
Rename (display name in Company Portal only), Remove, Remote lock, Check status.

## Known issues and failure causes
- The profile must be downloaded in Safari, and installed in Settings within a limited time; otherwise download it again.
- Signing in to a work app before Authenticator finishes deploying fails; wait a few minutes and retry.
- With web enrollment and JIT but no SSO extension policy, Company Portal for iOS may not recognise the enrolled device; deploy the SSO extension policy or use a web clip for the web Company Portal.
- If you use the Company Portal app for app deployment after web enrollment, send Authenticator and the SSO extension policy after enrollment.
- Only the settings supported by Apple device enrollment take effect on these devices; the page does not detail the MDM push certificate, device limit or enrollment restriction checks, so check Intune's iOS enrollment troubleshooting article for those.

## Certificates
Newly enrolling devices get an ACME certificate (iOS 16.0 or later, iPadOS 16.1 or later) in the management profile, preferred over SCEP for issuance validation. Already enrolled devices only get one after re-enrolling.

## Verify
Intune shows the device with the expected enrollment type and not supervised, policies apply, and the user can sign in to a work app without a compliance block.

## Checked
Method: documentation only; no commands were run. Checked 2026-11-08 against the Intune pages ios-device-enrollment and enroll-your-device-in-intune-ios (read in full). Removed: the Apple Configurator and 30-day provisional period section (Apple source unreadable), the push certificate and device limit failure causes, and the "user can remove management" claim as unsupported by these pages. Added: web-based and account-driven options and ACME support.
