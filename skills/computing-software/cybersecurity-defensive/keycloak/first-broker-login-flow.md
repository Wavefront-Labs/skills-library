---
id: computing-software.cybersecurity-defensive.keycloak.first-broker-login-flow
name: first-broker-login-flow
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, first-broker-login, account-linking, review-profile, create-user-if-unique]
level: practitioner
status: docs-checked
description: "Control Keycloak first brokered login: review profile, create user if unique, verified linking, auto-link and existing-user-only flows, override of broker links."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/identity-broker/first-login-flow.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# first broker login flow
After authenticating at an external IdP, either Keycloak already has a linked account (the user is logged in as that user) or it has none. Automatically linking an existing local account with the same email to the external account is a potential security hole, because information from the external IdP cannot always be trusted. The IdP's *First Login Flow* option picks the workflow; it defaults to the `first broker login` flow, shown under *Authentication*. You can reconfigure the flow (disable, require or configure authenticators) or use other flows per provider.

Default authenticators:
- **Review Profile**: shows the profile retrieved from the IdP. *Update Profile On First Login*: ON shows the page, `missing` shows it only if mandatory data (email, first name, last name) is missing, OFF hides it unless the user follows the "Review profile info" link from Confirm Link Existing Account.
- **Create User If Unique**: if no account has the same email or username, creates a local account, links it and ends the flow; otherwise continues to the Handle Existing Account sub-flow. Mark it REQUIRED to guarantee no duplicates: the user then gets an error page and must link through Account management.
- **Confirm Link Existing Account**: tells the user an account with the same email exists; they can review the profile (restarting at Review Profile) or confirm linking. Disable it to go straight to verification.
- **Verify Existing Account By Email**: ALTERNATIVE by default, used if the realm has SMTP configured; emails the user to confirm linking.
- **Verify Existing Account By Re-authentication**: login screen to prove ownership, for when email is unavailable; users can also re-authenticate with another linked IdP; OTP can be forced.

Variants:
- Automatic linking: a new flow with Create User If Unique (Alternative) and Automatically Set Existing User (Alternative), which sets the existing user without verification. The docs warn the AutoLink authenticator is dangerous where users self-register arbitrary usernames or emails.
- Disable automatic user creation (for example a read-only LDAP store): set Create User If Unique and Confirm Link Existing Account to DISABLED; re-authentication then asks for both username and password. This is independent of the realm User Registration switch.
- Existing users only: a new flow with Detect Existing Broker User (REQUIRED) and Automatically Set Existing User (REQUIRED), set as the IdP's First Login Flow; Sync Mode force can refresh profile attributes.
- Override broker link: add Confirm Override Existing Link (REQUIRED) after authenticators that have already established the user.

## Checked
2026-11-03. Confirmed against server_admin/topics/identity-broker/first-login-flow.adoc. Removed: the "built-in flows cannot be changed" claim, the generic attacker narrative beyond the page's warnings, and the Verify step.
Method: documentation only; no commands were run.
