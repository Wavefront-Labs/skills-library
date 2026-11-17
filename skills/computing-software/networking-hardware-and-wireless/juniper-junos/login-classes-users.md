---
id: computing-software.networking-hardware-and-wireless.juniper-junos.login-classes-users
name: login-classes-users
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, login-class, user-accounts, permissions, radius-tacacs]
level: practitioner
status: draft
description: "Create Junos users with login classes and permissions, and add RADIUS/TACACS+ authentication order with local fallback."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# User accounts, login classes and AAA
Goal: least-privilege admin access with a local break-glass account.

```
set system login class NOC permissions [ view view-configuration network ]
set system login class NOC deny-commands "^(request system|start shell)"
set system login user alice class NOC
set system login user alice authentication ssh-ed25519 "ssh-ed25519 AAAA...placeholder alice@example"
set system root-authentication encrypted-password "$6$placeholder"
set system authentication-order [ tacplus password ]
set system tacplus-server 192.0.2.50 secret "<redacted>"
```

- Built-in classes: `super-user`, `operator`, `read-only`, `unauthorized`.
- Permissions are flags (`configure`, `view`, `trace`, `interface`, `routing`, ...); `allow-configuration`/`deny-configuration` regexes narrow stanzas.
- Remote users that do not exist locally map via `system login user remote` or the TACACS+ local-user-name attribute.

Gotcha: `authentication-order [ radius ]` without `password` locks you out when the server is unreachable. Always keep `password` in the order and test from a second session before logging out.

## Verify
- `show system login` / `show system users`; log in as the test user and confirm denied commands fail.
