---
id: computing-software.messaging-and-integration.prosody.mod-admin-telnet
name: mod-admin-telnet
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, console, telnet, administration, security]
level: practitioner
status: docs-checked
description: "mod_admin_telnet in Prosody: the local administration console on port 5582 via console_ports, its lack of authentication, and what it can do."
sources:
  - https://prosody.im/doc/modules/mod_admin_telnet
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_admin_telnet

```lua
modules_enabled = { "admin_telnet"; }
console_ports = { 5582, 5583 }  -- optional; default { 5582 }
```

`console_ports` sets which ports to listen on for telnet connections. The console can reload configuration, enable or disable a module and show Prosody's internals.

By default the telnet console can only be accessed from the same machine as Prosody. Because there is no authentication, do not enable it on servers that may be accessed by untrusted users.

## Checked

2026-11-04: confirmed against prosody.im/doc/modules/mod_admin_telnet (console_ports default and example, local-only access, no authentication). Removed the `prosodyctl shell` claim, the console page link and a generic verify line, which the page does not state.
Method: documentation only; no commands were run.
