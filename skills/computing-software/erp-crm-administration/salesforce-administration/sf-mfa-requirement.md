---
id: computing-software.erp-crm-administration.salesforce-administration.sf-mfa-requirement
name: sf-mfa-requirement
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-security-login, sf-mfa-requirement]
level: practitioner
status: draft
description: "Require MFA for UI logins."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Enforce multi-factor authentication
**Goal:** Require MFA for UI logins.

- Salesforce requires MFA for direct logins to the UI; enforce via SSO provider MFA or Salesforce Authenticator/TOTP/security keys.
- Use the "Multi-Factor Authentication for User Interface Logins" permission (profile or permission set) or Session Security Level policies.
- Provide an emergency access path.

## Gotchas
- Integration users use API access; MFA does not apply to them but IP and OAuth controls do.

## Self-check
A test user is prompted for a second factor.
