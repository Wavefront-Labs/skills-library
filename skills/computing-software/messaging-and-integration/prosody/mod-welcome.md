---
id: computing-software.messaging-and-integration.prosody.mod-welcome
name: mod-welcome
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, welcome-message, registration, modules]
level: intro
status: docs-checked
description: "mod_welcome in Prosody: greet newly registered users with welcome_message, using $username and $host variables; requires mod_register with registration allowed."
sources:
  - https://prosody.im/doc/modules/mod_welcome
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_welcome

Sends a custom message to new users. It works only when `mod_register` is enabled and allows registration.

```lua
modules_enabled = { "welcome"; }
welcome_message = "$host accepts you $username"
```

`welcome_message` defaults to `"Hello $username, welcome to the $host IM server!"`. `$username` is the new user's name and `$host` the host of the new user (example: for new.user@example.net, `new.user` and `example.net`).

## Checked

2026-11-04: confirmed against prosody.im/doc/modules/mod_welcome. Removed the "on first login" claim and a generic verify line.
Method: documentation only; no commands were run.
