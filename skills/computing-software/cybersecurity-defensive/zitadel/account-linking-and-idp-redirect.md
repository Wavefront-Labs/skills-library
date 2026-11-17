---
id: computing-software.cybersecurity-defensive.zitadel.account-linking-and-idp-redirect
name: account-linking-and-idp-redirect
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, account-linking, identity-providers, login, federation]
level: practitioner
status: docs-checked
description: "Understand how linked external identities redirect login automatically, and enable automatic linking by email or username on an identity provider."
sources:
  - https://zitadel.com/docs/concepts/features/account-linking
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
One ZITADEL user can have several external identities linked to it. This lets people use different providers yet appear as the same user in your applications, with one audit trail and a fallback if a provider is unavailable.

The behavior that surprises administrators: once a user is linked to an external identity provider and types their username, ZITADEL redirects straight to that provider. The user is not offered a choice between local password and external login. Only if the external login fails, for example because the IdP secret expired or is invalid, does ZITADEL fall back to local authentication.

Users see a choice of local login or providers only during registration, when no account exists. If one external provider is configured and username/password login is disabled, every authentication request goes directly to that provider.

For automatic linking, set "Account linking allowed" in the identity provider template settings. ZITADEL can then link a new external identity to an existing local account when the email address or username matches.

Because the link decides the login method, turn automatic linking on only for providers whose email claims you trust.

## Checked

2026-11-08. Read the account linking page in full.

Method: documentation only; no commands were run.
