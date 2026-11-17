---
id: computing-software.messaging-and-integration.prosody.mod-invites
name: mod-invites
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, invites, registration, roles, prosodyctl]
level: practitioner
status: docs-checked
description: "mod_invites in Prosody: enable invites, invites_adhoc and invites_register, invite_expiry 7 days, and create account, admin, role or password-reset invites."
sources:
  - https://prosody.im/doc/modules/mod_invites
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_invites

Manages invite codes for registration and approval. `invite_expiry` defaults to `86400 * 7` (7 days).

```lua
VirtualHost "example.com"
modules_enabled = { "invites"; "invites_adhoc"; "invites_register"; }
```

Restart after changing config. Create invites:

```
prosodyctl shell invite create_account example.com
sudo prosodyctl mod_invites generate example.com
sudo prosodyctl mod_invites generate example.com --admin
sudo prosodyctl mod_invites generate example.com --role prosody:member
sudo prosodyctl mod_invites generate example.com --reset jdoe
```

`--admin` gives accounts made from the invite the `prosody:admin` role; `--reset jdoe` is a password-reset invite, so send it securely. More: `prosodyctl shell help invite`.

Verify: a new client registers using the generated invite link while open registration stays off.

## Checked

2026-11-04. Read the mod_invites page: invite_expiry 86400 * 7, the invites, invites_adhoc and invites_register modules, prosodyctl shell invite create_account, mod_invites generate with --admin (prosody:admin role), --role and --reset, and prosodyctl shell help invite all match. Nothing removed.

Method: documentation only; no commands were run.
