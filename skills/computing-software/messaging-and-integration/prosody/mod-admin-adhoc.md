---
id: computing-software.messaging-and-integration.prosody.mod-admin-adhoc
name: mod-admin-adhoc
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, ad-hoc-commands, administration, modules]
level: intro
status: docs-checked
description: "mod_admin_adhoc in Prosody: let admins run server commands from an XMPP client's Execute command menu; no options beyond enabling it."
sources:
  - https://prosody.im/doc/modules/mod_admin_adhoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_admin_adhoc

Ad-hoc commands let you control XMPP servers and clients remotely over XMPP. There is no special configuration: after enabling the module Prosody automatically offers commands to server admins via the "Execute command" option in their client.

```lua
modules_enabled = {
    "admin_adhoc";
}
```

Clients known to support ad-hoc commands include Psi, Gajim, Pidgin, tkabber and poezio, and probably others.

## Checked

2026-11-04: confirmed against prosody.im/doc/modules/mod_admin_adhoc. Removed the claims that only accounts in `admins` can use it, that configuration reload is offered, a cross-reference to a skill that does not exist, and a generic verify line.
Method: documentation only; no commands were run.
