---
id: computing-software.collaboration-platform-administration.vikunja.oidc-local-account-fallback
name: oidc-local-account-fallback
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, usernamefallback, emailfallback, account-linking, duplicate-accounts, email-verified]
level: advanced
status: docs-checked
description: "Link OIDC logins to existing local Vikunja accounts with usernamefallback and emailfallback, with the matching rules and account-takeover risks."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/openid.mdx
  - https://raw.githubusercontent.com/go-vikunja/vikunja/main/config-raw.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Per provider, `usernamefallback` and `emailfallback` (both default false) let an OIDC login attach to an existing local user.

The setup page says both must be true for fallback matching. The config reference describes finer behaviour: when both are on, a local account matching username and email is preferred, then one matching email alone; `emailfallback` requires the provider to send `email_verified: true`.

For username matching the OIDC subject must equal the local username. In Authentik set the provider's subject mode to "Based on the User's username".

Fallback only links to local accounts; it does not merge users across different OIDC issuers, and a new provider creates a separate account even with the same email.

Risks, stated in both docs: a misconfiguration creates duplicate SSO users that block login to the intended account until deleted, and the provider can authenticate as any local user whose username or email it controls (account hijacking). Enable only with trusted providers.

Example block under `providers.authentiklogin`: `usernamefallback: true`, `emailfallback: true`.

## Checked

2026-11-04: checked against the OpenID page (login existing local user section) and config-raw.json (usernamefallback, emailfallback). Removed the generic "test on your version" advice. The two sources differ in detail (setup page: both must be true; config reference: finer matching order), which the skill states.

Method: documentation only; no commands were run.
