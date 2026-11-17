---
id: computing-software.cybersecurity-defensive.endpoint-security.macos-edr
name: macos-edr
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [macos-edr, endpoint-security-framework, full-disk-access, system-extensions, pppc-profile, mdm, edr-operations]
level: practitioner
status: draft
description: "Deploy EDR on macOS: Endpoint Security framework system extensions, MDM profiles for FDA, PPPC, network filters and background items, plus health checks after macOS upgrades."
sources: ["https://developer.apple.com/documentation/endpointsecurity", "https://support.apple.com/guide/deployment/privacy-preferences-policy-control-payload-dep38df53c2a/web", "https://learn.microsoft.com/en-us/defender-endpoint/mac-install-with-intune", "https://support.apple.com/guide/deployment/system-extensions-payload-settings-dep0d1b4a4ae/web"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EDR on macOS

Modern macOS EDR agents use Apple's **Endpoint Security (ES) framework** via a system extension, plus a
network extension for network filtering. They need explicit approval, which on managed Macs is
delivered via MDM profiles - user prompts are unreliable.

## MDM profiles to deploy (before the agent package)
1. **System Extensions** payload: allow the vendor's team ID and bundle IDs (e.g. Defender `UBF8T346G9`, `com.microsoft.wdav.epsext`, `com.microsoft.wdav.netext`).
2. **Privacy Preferences Policy Control (PPPC)**: grant **Full Disk Access** (SystemPolicyAllFiles) to the agent daemon and ES extension (code requirement from `codesign -dr - <path>`).
3. **Content filter / network extension** payload if the agent filters traffic (Defender network protection).
4. **Service Management - Managed Login Items** (macOS 13+) so background items are not disabled by users.
5. Notifications payload for the agent UI.
6. Vendor configuration (onboarding/licence plist).

## Health checks
- Defender: `mdatp health` (healthy, real_time_protection_enabled, full_disk_access_enabled).
- General: `systemextensionsctl list` shows the extension `[activated enabled]`; `sudo eslogger` is Apple's ES test client.
- Report devices missing FDA - without it the agent is largely blind.

## Upgrades
Test major macOS releases in beta with the vendor's support matrix; ES API changes can break agents on
day one. Use MDM software update deferral for the fleet until the agent is supported.

## Gotchas
- Profiles must arrive before the package or the user gets prompts and the extension stays unapproved.
- A user with admin rights can remove profiles not marked non-removable; deploy via MDM with removal disallowed.
- Two ES-based security tools can conflict on the same events; check vendor coexistence guidance.

## Verify
- [ ] Fleet report: 100% FDA and extension activated.
- [ ] Test detection (vendor test file/EICAR) raises an alert from a Mac.
