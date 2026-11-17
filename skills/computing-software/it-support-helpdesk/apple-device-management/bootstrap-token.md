---
id: computing-software.it-support-helpdesk.apple-device-management.bootstrap-token
name: bootstrap-token
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, provisioning, bootstrap-token, secure-token]
level: practitioner
status: docs-checked
description: "Check, escrow and remove the macOS bootstrap token with the profiles tool, and what it authorises: updates, Erase All Content and Settings and Platform SSO users."
sources:
  - "https://support.apple.com/guide/deployment/dep24dbdcf9e/web"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bootstrap-token

Goal: make sure the MDM service can authorise updates and grant secure tokens on Macs.

- macOS 10.15.4 or later generates a bootstrap token and escrows it to the MDM service when a secure token-enabled user first logs in, if the service supports the feature.
- On macOS 11 or later with Apple silicon, a managed Mac can use the bootstrap token to authorise installation of software updates, silently authorise an Erase All Content and Settings command (macOS 12.0.1 or later) and create new users at first login with Platform SSO (macOS 13 or later). It also grants secure tokens to local users who log in and did not get one at creation (macOS 11 or later).
- `profiles` tool, run with `sudo`:
  - `profiles status -type bootstraptoken` reports whether the MDM service supports the feature and the token's state on the Mac (`profiles validate -type bootstraptoken` reports the same).
  - `profiles install -type bootstraptoken` generates a new token and escrows it; it needs existing secure token administrator information and a service that supports the feature.
  - `profiles remove -type bootstraptoken` removes the token on the Mac and from the service.
- When bootstrap token is available it also becomes a volume owner on Apple silicon Macs and grants volume ownership as it grants secure tokens.

Gotcha: `profiles install -type bootstraptoken` cannot run without secure token administrator credentials, so a Mac with no secure token user cannot escrow a token by hand.

Verify:
- `sudo profiles status -type bootstraptoken` shows the MDM service supports it and a token is escrowed.

## Checked

Date: 2026-11-07. Read in full: Apple Platform Deployment "Use secure token, bootstrap token and volume ownership in deployments" (secure token, bootstrap token, volume ownership, `profiles` and `sysadminctl` sections). Removed as unconfirmed: the "supervised or ADE Mac" requirement for install, the Jamf Pro inventory field, the "silent update enforcement fails" claim, the sample "escrowed yes" output and the swiftDialog source (unrelated). Replaced the vague welcome-page source with the real page.
Method: documentation only; no commands were run.
