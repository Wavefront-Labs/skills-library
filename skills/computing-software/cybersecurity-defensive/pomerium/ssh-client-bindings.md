---
id: computing-software.cybersecurity-defensive.pomerium.ssh-client-bindings
name: ssh-client-bindings
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [client-binding, session-binding-info, user-code, revoke-binding, remember-me]
level: practitioner
status: docs-checked
description: "Understand and manage Pomerium client bindings for SSH keys: first-time approval, cache lifetime, revocation, switching users and key-sharing risk."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/internals/client-binding.mdx
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/native-ssh-access.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A client binding links your OAuth user to a specific non-HTTP client (for SSH, the key used to connect), allowing standard web flows such as Authorization Code.

First use: the terminal prints a sign-in prompt with a link to `<authenticate-service-URL>/.pomerium/sign_in?user_code=...`. The verify page shows details so you can confirm the request is legitimate; approving creates the binding.

Lifetime: cached credentials last for the smaller of 48 hours or the session timeout (default 14 hours). "Remember me" ties the binding to the user until the session expires; with a cookie timeout above 48 hours, or after revocation, later requests auto-approve when the code link is opened.

Manage at `<authenticate-service-URL>/.pomerium/session_binding_info`. Revoking a binding immediately ends related connections. To switch users, also clear the remember field. Logging out revokes all of a user's bindings and terminates their connections.

SSH specifics:
- A user can have many SSH keys; each key can be bound to only one user.
- If the same key is shared across machines, those machines authenticate automatically with no sign-in confirmation, so do not share keys.
- Revoking a binding terminates all SSH connections started with that key.

See ssh-connect-syntax-and-cli for connecting.

## Checked

2026-11-04. Read the Client bindings page and the Native SSH Access page: purpose, lifetime (smaller of 48 hours or session timeout, default 14 hours), remember me, session_binding_info management, revocation, logout and key-sharing warning all confirmed. Reworded the key-to-user line to match the SSH page.

Method: documentation only; no commands were run.
