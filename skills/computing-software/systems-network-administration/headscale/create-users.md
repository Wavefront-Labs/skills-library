---
id: computing-software.systems-network-administration.headscale.create-users
name: create-users
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, users, create, list, tailnet]
level: intro
status: docs-checked
description: "Create and list Headscale users, which own personal nodes, and the username rules to avoid trouble with policies and OIDC."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/usage/getting-started.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/registration.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/oidc.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Users

Personal nodes belong to a Headscale user. Create one before registering devices.

```
headscale users create <USER>
headscale users list
```

The list shows each user's ID, which can be used in place of the name when creating a pre-authenticated key (`--user <USER_ID>`).

## Rules and policy links

- In policy files, a user is written with a trailing `@`, e.g. `alice@`; the identifier needs a single `@`.
- The Headscale username must not end with `@` (registration docs footnote).
- OIDC-synced usernames must be at least two characters, start with a letter, and contain only letters, digits, hyphens, dots, underscores and at most one `@`.
- Tagged nodes are owned by the special user `tagged-devices`, not a human user.

## Next

Register a device with web authentication or a pre-authenticated key (register-web-auth, register-preauthkey). Confirm with `headscale nodes list`, which shows the owner in the User column.

## Checked

2026-11-04. Confirmed against the Headscale getting-started, registration and OIDC pages: users create/list, user ID accepted for preauthkeys, trailing `@` in policy, the footnote that a username must not end with `@`, the OIDC username pattern, and `tagged-devices`.
Method: documentation only; no commands were run.
