---
id: computing-software.collaboration-platform-administration.google-workspace-admin.marketplace-allowlisting
name: marketplace-allowlisting
category: computing-software
field: collaboration-platform-administration
product: google-workspace-admin
tags: [marketplace-allowlisting, gws-apps-api-controls]
level: practitioner
status: draft
description: Limit which Marketplace apps users can install.
sources: ['https://support.google.com/a/', 'https://cloud.google.com/learn/certification/google-workspace-administrator']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Marketplace allowlisting
**Goal:** Limit which Marketplace apps users can install.

- Apps > Google Workspace Marketplace apps > Settings: allow all, allow listed only, or block.
- Review and add vetted apps to the allowlist; assign to OUs.
- Domain-wide install gives all users the app.
- Review app scopes before approving.

## Gotchas
- Allowing all apps lets any user grant data access to third parties.
- App removal may leave granted tokens; revoke them too.

## Self-check
Apps outside the list cannot be installed by a test user.
