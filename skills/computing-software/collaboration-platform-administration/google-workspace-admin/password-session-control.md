---
id: computing-software.collaboration-platform-administration.google-workspace-admin.password-session-control
name: password-session-control
category: computing-software
field: collaboration-platform-administration
product: google-workspace-admin
tags: [password-session-control]
level: practitioner
status: draft
description: Set password length, reauthentication and session duration.
sources: ['https://support.google.com/a/', 'https://cloud.google.com/learn/certification/google-workspace-administrator']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Password policy and session control
**Goal:** Set password length, reauthentication and session duration.

- Security > Authentication > Password management: minimum length (12+ is common), strength enforcement.
- Google session control: Security > Google Cloud session control for web session length.
- Revoke user sessions: Users > Security > Reset sign-in cookies.
- Reauthentication for Google Cloud / sensitive apps.

## Gotchas
- Google recommends long passphrases and 2SV over expiry (policy choice).
- Resetting cookies signs the user out of all devices.

## Self-check
Test account is asked to reauthenticate after the configured period.
