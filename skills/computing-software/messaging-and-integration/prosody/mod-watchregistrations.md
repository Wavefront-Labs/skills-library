---
id: computing-software.messaging-and-integration.prosody.mod-watchregistrations
name: mod-watchregistrations
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, registration, alerts, monitoring, admins]
level: intro
status: docs-checked
description: "mod_watchregistrations in Prosody: alert watchers when someone registers, registration_watchers (default admins) and the registration_notification template."
sources:
  - https://prosody.im/doc/modules/mod_watchregistrations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_watchregistrations

Alerts you when someone registers on a server with open registration.

```lua
modules_enabled = { "watchregistrations"; }
registration_watchers = { "some.user@example.net" }
registration_notification = "User $username just registered on $host from $ip"
```

- `registration_watchers` default `{ }`; if empty the `admins` list is used.
- `registration_notification` default is the string above; variables `$username`, `$host`, `$ip`.

By enabling the module, all configured admins receive a message when someone registers; the options customise this. Variables are replaced before sending: `$username` is the new user's username, `$host` their host, `$ip` the IP address the registration was made from.

## Checked

2026-11-04: confirmed against prosody.im/doc/modules/mod_watchregistrations (both options and defaults, three variables). Removed the claim that it is enabled automatically with `allow_registration`, and a generic verify line.
Method: documentation only; no commands were run.
