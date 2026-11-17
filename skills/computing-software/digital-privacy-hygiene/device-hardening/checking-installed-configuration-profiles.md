---
id: computing-software.digital-privacy-hygiene.device-hardening.checking-installed-configuration-profiles
name: checking-installed-configuration-profiles
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, configuration-profiles, ios, stalkerware]
level: practitioner
status: draft
description: "Find and remove unexpected configuration profiles, MDM enrolment and trusted root certificates on iPhone and Mac that can proxy, monitor or restrict you."
sources:
  - "https://support.apple.com/guide/personal-safety/check-configuration-profiles-ips7e0aeb2d2/web"
  - "https://support.apple.com/en-us/102390"
  - "https://support.apple.com/guide/deployment/intro-to-mdm-profiles-depc0aadd3fe/web"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Checking installed configuration profiles

**Goal:** nobody has installed a profile that routes your traffic through their proxy/VPN, trusts their certificate
to read HTTPS, or manages your device.

## iPhone/iPad
- Settings > General > **VPN & Device Management**: lists configuration profiles and any MDM enrolment.
  If the section doesn't appear, no profiles are installed.
- Settings > General > About > **Certificate Trust Settings**: any root certificate with full trust enabled can
  intercept HTTPS. Unknown ones are a red flag.
- Remove: tap the profile > Remove Profile > passcode. Supervised/MDM-enrolled devices from your employer/school
  may not allow removal; that's their device control.

## Mac
- System Settings > General > **Device Management** (older: Profiles) lists profiles.
- Terminal: `sudo profiles show -type configuration` and `profiles status -type enrollment`.
- Keychain Access > System roots/System: look for unexpected certificates set to "Always Trust".

## What malicious profiles do
Install a VPN/proxy (traffic monitoring), a root CA (HTTPS interception), restrict settings, or enable MDM
(location, app inventory). Common in stalkerware and some "free VPN"/"ad-blocker" scams.

## After removal
Change passwords used while the profile was active, especially if a root cert was trusted.

## Gotchas
- Work/school profiles on personal devices give the organisation visibility; consider a separate device.
- Lockdown Mode blocks installing new configuration profiles.
