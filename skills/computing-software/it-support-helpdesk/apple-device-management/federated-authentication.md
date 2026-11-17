---
id: computing-software.it-support-helpdesk.apple-device-management.federated-authentication
name: federated-authentication
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, abm-accounts, federated-authentication, federation, sso, entra]
level: practitioner
status: draft
description: "Federate ABM or ASM with Entra ID, Google Workspace or a SAML IdP so staff sign in with work credentials and accounts provision automatically."
sources:
  - "https://support.apple.com/guide/apple-business-manager/welcome/web"
  - "https://support.apple.com/guide/deployment/welcome/web"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# federated-authentication

Goal: let work usernames and passwords authenticate Managed Apple Accounts.
- Accounts > Domains: verify the domain first, then Federated Authentication > Connect to Entra ID (or Google Workspace).
- Sign in as a Global Administrator from the IdP tenant and consent; Apple tests with a sample user.
- Use the IdP username (UPN) as the Managed Apple Account; mail attribute mismatches break first sign-in.
- Optionally enable directory sync so new users appear without CSV imports.
- Account-driven User Enrollment relies on this for sign-in prompts.
Gotcha: federating a domain converts existing accounts and users may be asked to reauthenticate; pilot with a test domain or subset first, and keep a non-federated Administrator for break-glass.
Verify:
- Pilot user signs in under Settings with the work UPN.
- Federation status shows Connected in ABM.
- Break-glass Administrator still signs in with its own password.
