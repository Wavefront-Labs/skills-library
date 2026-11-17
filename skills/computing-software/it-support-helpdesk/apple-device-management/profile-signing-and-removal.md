---
id: computing-software.it-support-helpdesk.apple-device-management.profile-signing-and-removal
name: profile-signing-and-removal
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, config-profiles, profile-signing-and-removal, profile-signing, remove-profile]
level: practitioner
status: draft
description: "Sign configuration profiles, tell user-removable from MDM-locked profiles and plan removal with RemoveProfile or a removal passcode."
sources:
  - "https://support.apple.com/guide/deployment/configuration-profiles-and-payloads-dep9c8f4f2a0/web"
  - "https://developer.apple.com/documentation/devicemanagement/profile-specific_payload_keys"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# profile-signing-and-removal

Goal: protect profiles from tampering and remove them cleanly.
- Sign with a trusted certificate: `security cms -S -N "Cert Name" -i in.mobileconfig -o signed.mobileconfig` so the profile shows Verified.
- PayloadRemovalDisallowed true stops removal on supervised devices; a RemovalPassword limits removal to people who know it.
- MDM-delivered profiles are removed with `RemoveProfile` or by removing scope in the console, applied at next check-in.
- Manually installed profiles are separate from MDM profiles and show under System Settings > Privacy & Security > Profiles.
Gotcha: removing the MDM enrolment profile removes every payload it installed, including Wi-Fi and certificates.
Verify:
- Signed profile displays Verified in System Settings.
- A removal test on a lab device clears its payloads.
