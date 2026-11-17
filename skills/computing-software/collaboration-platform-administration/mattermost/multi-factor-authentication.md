---
id: computing-software.collaboration-platform-administration.mattermost.multi-factor-authentication
name: multi-factor-authentication
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [mfa, totp, enforce-mfa, authentication]
level: practitioner
status: docs-checked
description: "Enable, enforce and disable Mattermost TOTP multi-factor authentication, with the time-sync requirement and rollout advice."
sources: ["https://docs.mattermost.com/administration-guide/onboard/multi-factor-authentication.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multi-factor authentication

MFA adds a one-time code on top of the username and password (email-password or AD/LDAP login) for all users on all teams. It is smartphone based: iOS, Android or any device with a software authenticator such as FreeOTP, Google Authenticator, Microsoft Authenticator, 1Password or LastPass. Because it uses time-based one-time passwords (TOTP), the server clock must be accurate or users may fail to log in.

Enable: System Console > Authentication > MFA, set Enable Multi-factor Authentication to true. Users then opt in from Profile > Security > Multi-factor Authentication.

Disable: set Enable Multi-factor Authentication to false; users can then neither use nor disable MFA themselves. An admin can disable MFA for a specific user account through the users MFA API endpoint (the documentation points to the API reference for the PUT on /users/{user_id}/mfa).

Enforce (for compliance, applies to email and LDAP accounts): set Enforce Multi-factor Authentication to true in the same page. Users without MFA are sent to the setup page on login and cannot reach the site until it is complete, and they cannot remove MFA while enforcement is on. The docs recommend switching enforcement on during non-peak hours.

## Checked

Confirmed against the Multi-factor authentication page: TOTP and supported authenticator apps, the clock accuracy note, enable, disable and enforce paths and behaviour, the API reference for disabling a user's MFA, and the non-peak-hours recommendation. Removed the guest account and SSO statements, which that page does not make.

Method: docs-checked 2026-11-09 against the full administration-guide/onboard/multi-factor-authentication page (source rst from the mattermost/docs repo).
