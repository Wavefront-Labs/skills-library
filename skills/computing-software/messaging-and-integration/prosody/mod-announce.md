---
id: computing-software.messaging-and-integration.prosody.mod-announce
name: mod-announce
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, announcements, administration, shell, modules]
level: practitioner
status: docs-checked
description: "mod_announce in Prosody: send admin announcements to online users via a message to HOST/announce/online, an ad-hoc command, or the Prosody 13 shell."
sources:
  - https://prosody.im/doc/modules/mod_announce
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_announce

Lets administrators message all online users (for example about an upcoming outage or maintenance). It has no options; enable with `"announce";` in `modules_enabled`.

Ways to send (only administrators can send announcements):

- Message to `HOST/announce/online`, for example `example.com/announce/online`.
- The ad-hoc command, in a client that supports them: look for "Send Announcement to Online Users", fill out the form and send.
- Shell, new in Prosody 13.0: `announce:all(host, text)` (all users on the host), `announce:online(host, text)` (all online users), `announce:role(host, role, text)` (users with a specific role).

```
# prosodyctl shell
prosody> announce:online("example.com", "Hello from the Shell!")
| OK: Announcement sent to 3 users
```

```
# prosodyctl shell announce online example.com "Hello from $SHELL"
```

Permission required: `announce:send-announcement`, granted to the `prosody:admin` role.

## Checked

2026-11-04: confirmed against prosody.im/doc/modules/mod_announce (message method, ad-hoc command, Prosody 13.0 shell commands, permission, no options). Replaced the invented example text with the page's example and removed a generic verify line.
Method: documentation only; no commands were run.
