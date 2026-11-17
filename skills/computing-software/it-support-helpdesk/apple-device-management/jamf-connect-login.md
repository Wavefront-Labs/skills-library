---
id: computing-software.it-support-helpdesk.apple-device-management.jamf-connect-login
name: jamf-connect-login
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, jamf-connect, jamf-connect-login, login-window]
level: practitioner
status: draft
description: "Configure Jamf Connect Login for IdP-based macOS account creation and password sync at the login window, including preference domain keys."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-connect-documentation-current/page/Jamf_Connect_Documentation.html"
  - "https://learn.jamf.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# jamf-connect-login

Goal: create and sync local accounts from the cloud IdP.
- Install Jamf Connect pkg (Login and Menu Bar), then deploy preferences to `com.jamf.connect.login`.
- Key examples: `OIDCProvider`, `OIDCClientID`, `OIDCRedirectURI`, `CreateAdminUser`, `DenyLocal`, `MigrateUsers`.
- Use the Jamf Connect Configuration app to build the profile.
- Replace the Apple login window by authchanger: `sudo /usr/local/bin/authchanger -reset -JamfConnect`.
- Add Jamf Connect in the ADE flow via DEP Notify or a prestage package.
Practice: Test with a throwaway account for first login, password change and offline login, and keep a local administrator reachable in case the IdP is down.
Gotcha: if authchanger is not reset after an OS update, users land at the stock login window; keep a reset policy on Recurring Check-in.
Verify:
- New user can sign in with IdP credentials and gets a local account.
- `authchanger -print` lists Jamf Connect mechanisms.
