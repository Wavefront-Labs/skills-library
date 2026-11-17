---
id: computing-software.collaboration-platform-administration.google-workspace-admin.create-users-bulk
name: create-users-bulk
category: computing-software
field: collaboration-platform-administration
product: google-workspace-admin
tags: [create-users-bulk, gws-user-provisioning]
level: practitioner
status: draft
description: Add users individually, by CSV, or API.
sources: ['https://support.google.com/a/', 'https://cloud.google.com/learn/certification/google-workspace-administrator']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Create users and bulk upload
**Goal:** Add users individually, by CSV, or API.

- Directory > Users > Add new user, or More options > Bulk update users with CSV.
- Email domain must be verified first (TXT or CNAME record).
- Assign licences automatically with 'Automatic licensing' on an OU.
- Force password change at first sign-in and enrol in 2SV.

## Gotchas
- Use a primary domain alias for naming consistency.
- Deleted users can be restored for 20 days.

## Self-check
The user signs in and sees Gmail, with the correct OU and licence.
