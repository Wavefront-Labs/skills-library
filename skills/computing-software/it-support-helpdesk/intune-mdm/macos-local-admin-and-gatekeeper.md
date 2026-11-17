---
id: computing-software.it-support-helpdesk.intune-mdm.macos-local-admin-and-gatekeeper
name: macos-local-admin-and-gatekeeper
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, macos-local-admin, gatekeeper-notarization, macos-laps, gatekeeper, notarization, macos-security]
level: practitioner
status: draft
description: "Manage macOS local admin accounts (creation at enrollment, rotation, standard users) and handle Gatekeeper and notarization blocks for unsigned or unnotarized apps."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/enrollment/macos-laps"
  - "https://support.apple.com/guide/security/gatekeeper-and-runtime-protection-sec5599b66df/web"
  - "https://support.apple.com/en-us/102445"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# macos-local-admin-and-gatekeeper

## Local admin accounts
- Goal: users work as **standard** users; a managed local admin exists for IT with a
  unique, rotated password.
- Intune (macOS ADE): the enrollment profile's **Account settings** create a local admin
  account and a primary account (standard or admin). The admin password is random per
  device, stored in Intune, viewable under the device > **Passwords and keys**, and
  rotated (default every 6 months, or via **Rotate local admin password** action).
- Jamf: managed local administrator account in PreStage; LAPS via Jamf Pro API.
- Temporary elevation tools (e.g. Privileges app, Jamf Connect elevation) for users who
  occasionally need admin, with logging.
- Check an account: `dscl . -read /Groups/admin GroupMembership`; demote with
  `sudo dseditgroup -o edit -d <user> -t user admin`.
- Secure token / bootstrap token: the admin account needs a secure token to enable
  FileVault users and software updates on Apple silicon; MDM escrows the bootstrap
  token (`sudo profiles status -type bootstraptoken`).

## Gatekeeper and notarization
- Gatekeeper checks downloaded apps: signed with a Developer ID and **notarized** by
  Apple (macOS 10.15+). Unnotarized apps show "can't be opened because Apple cannot check
  it for malicious software".
- User override (macOS 15+): open the app, then System Settings > Privacy & Security >
  "Open Anyway" (the Control-click > Open bypass was removed in Sequoia).
- IT approach: don't teach users to bypass. Get a notarized build from the vendor, or
  deploy through MDM as a signed PKG (MDM-installed packages bypass the quarantine
  prompt).
- Check a file: `spctl --assess --verbose /Applications/App.app`,
  `codesign -dv --verbose=4 /Applications/App.app`, `xattr -l` shows
  `com.apple.quarantine`.
- Removing quarantine (`xattr -dr com.apple.quarantine`) is a last resort for verified
  internal tools only.

## Verify
Users are standard, the managed admin password is retrievable and rotates, and approved
apps launch without Gatekeeper prompts after MDM deployment.
