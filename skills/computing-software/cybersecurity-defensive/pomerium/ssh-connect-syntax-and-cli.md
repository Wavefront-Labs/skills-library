---
id: computing-software.cybersecurity-defensive.pomerium.ssh-connect-syntax-and-cli
name: ssh-connect-syntax-and-cli
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [ssh-client, internal-cli, routes-portal, whoami, session-length]
level: intro
status: docs-checked
description: "Connect to Pomerium native SSH with user@route@pomerium, understand first-login and cached sessions, and use the internal CLI."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/native-ssh-access.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Syntax: `ssh user@route@pomerium`
- `user`: Linux username on the upstream.
- `route`: the name after `ssh://` (for `ssh://route1`, `route1`).
- `pomerium`: DNS name or IP of the Pomerium server.

**First connection**: authenticate in the browser, then return to the terminal. Access requires meeting the route policy. This creates a client binding between the SSH key and the OAuth user. A key maps to one user; a user can have many keys.

**Later connections**: no browser step; cached credentials are used. Session length defaults to 14 hours (cookie expiration) with a maximum of 48 hours. Credentials can be revoked in the Pomerium UI. Policy is still enforced on every connection.

Versions below 0.32.0 support only the Device Code flow.

**Internal CLI**: connect to Pomerium without a route name. Commands (see `--help`):
- `whoami`: current session info.
- `logout`: forces IdP re-authentication on next connection.
- `portal`: interactive route picker, using the username from the original ssh command. Disabled by default; enabled by the `ssh_routes_portal` runtime flag.

Any authenticated user can use the CLI; route policy is evaluated after a route is selected. See ssh-client-bindings for managing keys.

## Checked

2026-11-04. Read the Native SSH Access page: connection syntax, first and later connection behaviour, 14 hour and 48 hour limits, version note, and internal CLI commands all confirmed. Nothing removed.

Method: documentation only; no commands were run.
