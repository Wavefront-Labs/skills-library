---
id: computing-software.it-support-helpdesk.apple-device-management.local-admin-laps
name: local-admin-laps
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, local-admin, local-admin-laps, laps, password-rotation]
level: practitioner
status: draft
description: "Provide a LAPS-like unique local admin password per Mac using Jamf Pro LAPS or an MDM-managed account with rotation."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Local_Accounts.html"
  - "https://support.apple.com/guide/deployment/welcome/web"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# local-admin-laps

Goal: unique, rotating break-glass admin passwords.
- Jamf Pro has a LAPS configuration for the managed local account (confirm availability and version).
- Alternative: a policy with a script that sets a random password and stores it in an EA or secrets vault.
- Native Apple option: Managed local accounts with `AccountConfiguration` at ADE time create the first admin.
- Rotate after each view and after use.
- Use `sysadminctl -resetPasswordFor user -newPassword - -adminUser admin -adminPassword -` carefully.
Practice: Limit who can view passwords, log retrievals, and rotate immediately after use so a shared password never stays valid; test recovery on a spare Mac every quarter.
Gotcha: an account without Secure Token cannot be used to unlock FileVault; use it for local admin tasks only.
Verify:
- Retrieval returns a password that works on a test Mac.
- Audit log shows the view.
