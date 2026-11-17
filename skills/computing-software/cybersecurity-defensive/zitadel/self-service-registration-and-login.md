---
id: computing-software.cybersecurity-defensive.zitadel.self-service-registration-and-login
name: self-service-registration-and-login
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, self-service, registration, login, organization-scope]
level: practitioner
status: docs-checked
description: "Know what ZITADEL lets users do themselves at registration and login, and how to pin registration to one organization with a domain scope."
sources:
  - https://zitadel.com/docs/concepts/features/selfservice
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ZITADEL provides self-service interfaces, or APIs, for two audiences: users and administrators. All self-service interfaces are available in several languages.

Local registration lets anonymous users, or authenticated users who are not yet in the organization, register themselves. Steps are mandatory profile fields, setting a password, accepting terms of service and privacy policy, and entering a one-time code emailed to them. The code can be requested again. On first login the user is prompted to set up MFA, which can be mandatory if the login policy enforces it.

Registration with an existing identity uses an external provider. Profile data from the provider pre-fills the form, the user can edit it, and an account is created and linked.

When a user logs in with an external provider and no ZITADEL account exists, an autoregister flow offers two options: create a new account, or autolink by logging in with an existing local account so both identities belong to one user.

To force registration into one organization, pass the scope `urn:zitadel:iam:org:domain:primary:{domainname}` in the authorization request. This also shows that organization's branding and login settings, including its social providers.

## Checked

2026-11-08. Read the self service page in full.

Method: documentation only; no commands were run.
