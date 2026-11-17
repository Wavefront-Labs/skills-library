---
id: computing-software.cybersecurity-defensive.dex.dex-microsoft-connector-scopes-domainhint-email
name: dex-microsoft-connector-scopes-domainhint-email
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [microsoft, scopes, domainhint, emailtolowercase]
level: practitioner
status: docs-checked
description: "Tune the Microsoft connector with domainHint, scopes (default user.read) and emailToLowercase for Kubernetes username matching."
sources:
  - https://dexidp.io/docs/connectors/microsoft/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three smaller options on the Microsoft connector:

```yaml
config:
  tenant: example.onmicrosoft.com
  domainHint: example.com
  scopes:
  - openid
  - email
  emailToLowercase: true
```

- `domainHint`: streamlines login when all users share an email domain. Users with several Microsoft sessions are normally asked which account to use. With `domainHint` set, Microsoft selects the session with the matching email without the interactive prompt, for example choosing `John.Doe@example.com` over `John.Doe@live.com`.
- `scopes`: the initial scopes Dex requests from Microsoft. The default, when unset, is `user.read`. The list may be extended by the `groups` scope or when a refresh token is used. The docs example requests only `openid` and `email` to get the email address and nothing else.
- `emailToLowercase` (boolean): lowercases UPNs from Active Directory before they go into the ID token. Without it, matching the email claim is hard because clients cannot tell whether capitalisation was used.

Use case: Kubernetes RBAC role bindings that use email as the user name (`--oidc-username-claim=email`) are case sensitive, so lowercase the claim.

## Checked

2026-11-03: read against Dex docs, Microsoft connector (https://dexidp.io/docs/connectors/microsoft/).

Removed or corrected: The gotcha about restricting scopes (not on the page).

Method: documentation only; no commands were run.
