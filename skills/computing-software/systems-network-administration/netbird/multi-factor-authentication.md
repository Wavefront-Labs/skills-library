---
id: computing-software.systems-network-administration.netbird.multi-factor-authentication
name: multi-factor-authentication
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, mfa, recovery-codes, reset-mfa, cloud-authentication]
level: practitioner
status: docs-checked
description: "Manage NetBird Cloud MFA: enabling it under Settings > Authentication, double-prompt risk, remember-browser, recovery code handling and admin resets."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/settings/multi-factor-authentication.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Scope: second verification step at login on NetBird Cloud. It mainly targets email/password users; if your SSO provider already enforces MFA with interactive login, that applies automatically. Self-hosted users rely on their IdP or local MFA.

Toggle: Settings > Authentication in the Dashboard. Disabling does not remove enrolled devices; they return when re-enabled.

Points:
- If the SSO provider already requires MFA, enabling NetBird MFA may prompt twice.
- First-time sign-up needs no MFA; later logins do.
- Remember browser skips the code for 30 days.
- Users page: "Active" means setup complete, "Not Enrolled" means not.

Recovery codes: one is shown during setup, once only; store it outside the phone. Each works once and yields a new code that must be saved straight away. A recovery code signs you in but does not remove the lost authenticator, so the next login still asks.

Reset: an Owner or Admin selects the user on the Users page and clicks Reset MFA; the user scans a new QR at next login. If all Owners and Admins are locked out, contact support@netbird.io; keep more than one administrator.

## Checked

2026-11-04. Confirmed against the NetBird MFA page: cloud scope, Settings Authentication toggle, retained devices on disable, duplicate checks, first sign-up exemption, 30-day remember browser, Active and Not Enrolled states, recovery code handling, Reset MFA, support contact. Nothing removed.
Method: documentation only; no commands were run.
