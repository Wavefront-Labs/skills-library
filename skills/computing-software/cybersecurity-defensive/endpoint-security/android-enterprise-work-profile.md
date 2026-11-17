---
id: computing-software.cybersecurity-defensive.endpoint-security.android-enterprise-work-profile
name: android-enterprise-work-profile
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [android-enterprise, work-profile, fully-managed, managed-google-play, mdm, app-protection, mobile-device-management]
level: practitioner
status: draft
description: "Manage Android with Android Enterprise: work profile vs fully managed, enrolment methods, managed Google Play, cross-profile data controls, compliance and Play Integrity."
sources: ["https://developers.google.com/android/work/overview", "https://learn.microsoft.com/en-us/mem/intune/enrollment/android-enroll", "https://developer.android.com/google/play/integrity/overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Android Enterprise work profile

## Modes
| Mode | Ownership | Control |
|---|---|---|
| Personally owned work profile (BYOD) | User | Separate encrypted work container; admin manages only the profile, cannot see personal apps/data or wipe the whole device |
| Corporate-owned work profile (COPE) | Company | Work profile plus limited device-level controls |
| Fully managed (COBO) | Company | Whole device |
| Dedicated (COSU) | Company | Kiosk / single-purpose, lock task mode |
Device administrator (legacy) mode is deprecated - migrate off it.

## Enrolment
- BYOD: Company Portal / Android Device Policy app.
- Corporate: zero-touch enrolment (reseller), QR code, NFC, or `afw#setup` token at setup.

## Policies to set
- Work profile: passcode separate from device (or unified with complexity), block copy/paste to personal profile, block screen capture of work apps, disallow cross-profile contacts search if required, block installing from unknown sources in work profile.
- Apps from **managed Google Play** only for work profile; private apps published to your organisation.
- Compliance: minimum OS and security patch level, **Play Integrity verdict** (MEETS_DEVICE_INTEGRITY / strong integrity) - replaces SafetyNet; rooted devices non-compliant.
- Conditional Access requires compliant device or app protection policy.

## Gotchas
- Security patch level lags on many OEMs; set realistic minimums per device model and replace devices out of support.
- Work profile does not protect against a compromised device OS - pair with mobile threat defence for high-risk users.
- Older devices without hardware-backed key attestation pass weaker integrity checks.

## Verify
- [ ] No device administrator enrolments remain.
- [ ] Rooted test device marked non-compliant and blocked from email.
