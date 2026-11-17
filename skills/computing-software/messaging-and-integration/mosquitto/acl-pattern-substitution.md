---
id: computing-software.messaging-and-integration.mosquitto.acl-pattern-substitution
name: acl-pattern-substitution
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [acl-pattern, pattern-substitution, client-id, username, pattern]
level: practitioner
status: docs-checked
description: "Use pattern lines in an ACL file with %c and %u so every client is limited to topics containing its own id or username."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: write one ACL rule that scales to every client.

In an ACL file, `pattern` has the same form as `topic` but supports substitution:

```
pattern [read|write|readwrite|deny] <topic>
```

Available substitutions:
- `%c` matches the client id of the client
- `%u` matches the username of the client

The substitution pattern must be the only text for that level of hierarchy, so `sensor/%u/data` works while text mixed into a level does not substitute.

Examples from the page:
```
pattern write sensor/%u/data
pattern write $SYS/broker/connection/%c/state
```

The second line allows bridge connection messages, which is the one `$SYS` topic where write access can be granted.

Pattern ACLs apply to all users, even if the `user` keyword has previously been given in the file, whereas plain `topic` lines after a `user` line are specific to that user.

## Checked

Method: 2026-11-08 docs-only. Read the cited man page in full and compared each claim. Claims checked against mosquitto.conf(5). Removed the unsupported Dynamic Security ACL type claims; other claims unchanged.
