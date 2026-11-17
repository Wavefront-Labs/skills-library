---
id: computing-software.messaging-and-integration.prosody.mod-register
name: mod-register
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, registration, accounts, spam, security]
level: practitioner
status: docs-checked
description: "mod_register in Prosody: in-band account registration via allow_registration (default false), sub-modules it enables, and the abuse risks of open registration."
sources:
  - https://prosody.im/doc/modules/mod_register
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_register

```lua
modules_enabled = { "register"; }
allow_registration = true
```

`allow_registration` defaults to `false`, so registration stays closed unless set.

Side effects: enabling mod_register also enables `mod_user_account_management` (password changes); with `allow_registration = true` it also enables `mod_register_ibr` and `mod_watchregistrations`.

Risks: open registration invites spam accounts and abuse, so be ready to handle them. Consider disabling `mod_s2s` on an open-registration server. Rate limiting of account creation is done by `mod_register_limits`; `mod_invites` can control who registers.

Verify: a client can create an account only while `allow_registration = true` after a reload.

## Checked

2026-11-04. Read the mod_register page: allow_registration default false, the split into mod_register_ibr, mod_register_limits and mod_user_account_management, which modules mod_register enables and when, and the spam, mod_s2s and mod_invites advice all match. Nothing removed.

Method: documentation only; no commands were run.
