---
id: computing-software.it-support-helpdesk.apple-device-management.jamf-connect-menu-bar
name: jamf-connect-menu-bar
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, jamf-connect, jamf-connect-menu-bar, password-sync]
level: practitioner
status: draft
description: "Use Jamf Connect Menu Bar to keep the Mac password in sync with the IdP and offer password change, Kerberos tickets and privilege elevation."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-connect-documentation-current/page/Jamf_Connect_Documentation.html"
  - "https://learn.jamf.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# jamf-connect-menu-bar

Goal: keep local and cloud passwords aligned after login.
- Preference domain `com.jamf.connect`; keys such as `OIDCProvider`, `PasswordChangeURL`, `SyncPasswords`.
- Menu Bar can handle Kerberos TGT retrieval and show password expiry.
- Privilege elevation (Jamf Connect Privilege Elevation or `SwiftDialog` flows) provides time-limited admin (confirm product).
- Roll out as a separate pkg and profile scoped by smart group.
- Test password change round-trip with a lab account.
Practice: Decide up front whether the IdP or the Mac is the password source of truth, and brief staff, because the sync direction determines what happens after a reset.
Gotcha: Keychain mismatches follow out-of-band password resets; instruct users to reset through the IdP flow so the login keychain re-wraps.
Verify:
- Menu bar icon shows signed-in state.
- Changing the IdP password updates the local one on next sign-in.
