---
id: computing-software.systems-network-administration.home-assistant.account-security
name: account-security
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [refresh-tokens, long-lived-token, password]
level: practitioner
status: docs-checked
description: "Manage Home Assistant account access from the profile Security page: password, MFA, refresh tokens that expire after 90 days, and long-lived access tokens."
sources:
  - https://www.home-assistant.io/docs/authentication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control how you and your devices sign in.

Open your profile Security page (User profile > Security). Settings there affect only your own account. You can:

- Change your password.
- Turn multi-factor authentication on or off (see the mfa-totp skill).
- Manage Refresh tokens.
- Create long-lived access tokens.

Refresh tokens: one is created each time you sign in from a device. Delete a token to force that device to sign out. Tokens not used to sign in within 90 days are removed automatically. If you need a token that does not expire that way, the docs recommend a long-lived access token.

Long-lived access tokens let scripts and apps talk to Home Assistant securely.

Treat a token like a password and delete the ones you no longer use.

User accounts themselves (adding people, display names, usernames) are handled in the user configuration docs, not on this page. The login screen asks for username and password.

Choose a strong, unique password, particularly if you reach Home Assistant from outside the local network.

## Checked

2026-11-04. Confirmed against the Authentication page. Removed the claim that the token format and auth API are in contributor docs linked from the page.

Method: documentation only; no commands were run.
