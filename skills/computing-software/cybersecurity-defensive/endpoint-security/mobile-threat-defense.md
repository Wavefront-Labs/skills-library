---
id: computing-software.cybersecurity-defensive.endpoint-security.mobile-threat-defense
name: mobile-threat-defense
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [mobile-threat-defense, mtd, mobile-security, defender-for-endpoint-mobile, lookout, zimperium, mobile-device-management]
level: practitioner
status: draft
description: "Deploy mobile threat defence: MTD apps on iOS and Android, risk signals into MDM compliance and Conditional Access, phishing protection, privacy limits and BYOD app protection."
sources: ["https://learn.microsoft.com/en-us/mem/intune/protect/mobile-threat-defense", "https://learn.microsoft.com/en-us/defender-endpoint/mobile-endpoints-overview", "https://csrc.nist.gov/pubs/sp/800/124/r2/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mobile threat defence (MTD)

MDM manages configuration; MTD detects threats on the device - malicious apps, OS compromise
(jailbreak/root), risky networks (MITM, rogue Wi-Fi), phishing links, out-of-date OS with known exploits.

## Products
Microsoft Defender for Endpoint (iOS/Android), Lookout, Zimperium, Check Point Harmony Mobile,
Jamf Protect/Threat Defense, etc. NIST SP 800-124r2 covers mobile enterprise security.

## Integration flow
1. Connect MTD to the MDM (Intune: Tenant administration -> Connectors -> Mobile Threat Defense).
2. Deploy MTD app silently (managed app, auto-launch for Defender via app configuration).
3. Compliance policy: "Require the device to be at or under the Device Threat Level: Low/Medium" -> non-compliant devices blocked by Conditional Access.
4. Unenrolled (BYOD MAM-only) devices: app protection policy condition "Max allowed device threat level" with MTD for MAM.

## Features to enable
- Web/phishing protection (local VPN loopback on iOS/Android filters malicious URLs in all apps).
- Network protection (rogue Wi-Fi, certificate anomalies).
- App scanning (Android) for malicious/sideloaded apps; iOS app inventory limited by platform.
- Jailbreak/root detection.

## Privacy
Explain to BYOD users what the MTD app sees (no personal content); privacy-preserving modes (e.g. disable
URL logging for personal profile); legal/HR review.

## Gotchas
- The local-VPN web protection conflicts with other VPN apps; plan coexistence.
- Users who never open the MTD app on iOS may not activate it; use app configuration for zero-touch onboarding.
- Threat levels too strict cause access issues on travel networks; tune.

## Verify
- [ ] Test phishing URL (vendor test page) blocked on a test device.
- [ ] Jailbroken/rooted test device marked high threat and blocked.
