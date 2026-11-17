---
id: computing-software.cybersecurity-defensive.zitadel.login-policy-settings
name: login-policy-settings
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, login-policy, registration, domain-discovery, external-idp]
level: practitioner
status: docs-checked
description: "Tune ZITADEL's login behavior settings such as password login, registration, external IdPs, domain discovery and unknown-username handling."
sources:
  - https://zitadel.com/docs/guides/manage/console/default-settings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The login policy, shown as Login Behavior and Security, decides which authentication options users get. Key switches:

- Username Password allowed: if disabled, only external identity providers work.
- Register allowed: enables self-registration with username and password and with configured external providers.
- External IDP allowed: lets users log in with providers you add to the providers list.
- Hide password reset: removes the self-service password reset.
- Domain discovery allowed: the user does not need to exist when entering a username. It requires an organization domain on the organization, so a login name at the organization's domain can route to that organization's identity provider such as Entra ID.
- Ignore unknown usernames: no error for a missing user. The login proceeds to the password screen and only after a password is entered does the user get a "username or password wrong" error.
- Disable login with email address and Disable login with phone number: by default users can also log in with those attributes.

Set the policy on the instance for the default and override it on an organization when a tenant needs different rules. Remember that organization administrators can override these settings for their organization, which is why instance administrators should live in a dedicated organization.

## Checked

2026-11-08. Read the default settings page in full; reworded an unsupported enumeration claim.

Method: documentation only; no commands were run.
