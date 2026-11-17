---
id: computing-software.database-administration.dragonfly.acl-key-and-channel-permissions
name: acl-key-and-channel-permissions
category: computing-software
field: database-administration
product: dragonfly
tags: [key-permissions, pubsub-permissions, acl-patterns, resetkeys, dragonfly]
level: practitioner
status: docs-checked
description: "Restrict Dragonfly ACL users to key patterns and pub/sub channels with ~, %R~, %W~, & and the reset rules."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/acl.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/acl/setuser.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A command runs only if the user's ACL allows both the command (or group) and a key pattern matching the command's keys.

Key rules (glob-style patterns):

- `~<pattern>`: access matching keys (`~*` all keys).
- `%R~<pattern>`: read only.
- `%W~<pattern>`: write only.
- `%RW~<pattern>`: alias for `~<pattern>`.
- `allkeys`: alias for `~*`.
- `resetkeys`: remove all key patterns; the user can access no key.

Pub/Sub rules:

- `&*` or `allchannels`: all channels.
- `&<pattern>`: matching channels.
- `resetchannels`: revoke all channels.

For commands starting with `P` such as `PSUBSCRIBE`, the pattern must match literally. If the ACL contains `&foo` then `PSUBSCRIBE foo` passes; a pattern like `&fo&` would not. This restriction does not apply to other pub/sub commands.

Verify rules without running a command by using `ACL DRYRUN`, and inspect a user with `ACL GETUSER`.

## Checked

2026-11-04. Confirmed in the Dragonfly ACL guide (Key Permissions and Pub/Sub Permissions) and the ACL SETUSER page (same rules, literal match note for `P` commands). Nothing removed.

Method: documentation only; no commands were run.
