---
id: computing-software.collaboration-platform-administration.google-workspace-admin.oauth-api-access-control
name: oauth-api-access-control
category: computing-software
field: collaboration-platform-administration
product: google-workspace-admin
tags: [oauth-api-access-control]
level: advanced
status: draft
description: Restrict third-party and internal apps' access to Google data.
sources: ['https://support.google.com/a/', 'https://cloud.google.com/learn/certification/google-workspace-administrator']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OAuth app access control
**Goal:** Restrict third-party and internal apps' access to Google data.

- Security > Access and data control > API controls > App access control: set Restricted, Limited for sensitive scopes.
- Mark apps Trusted, Limited or Blocked; use domain-wide delegation carefully.
- Review Domain-wide delegation client IDs and scopes regularly.
- Revoke tokens from the user's Security tab.

## Gotchas
- Blocking an app can break integrations; announce first.
- Domain-wide delegation grants a service account broad impersonation; keep minimal.

## Self-check
Test app consent prompts are blocked for restricted scopes.
