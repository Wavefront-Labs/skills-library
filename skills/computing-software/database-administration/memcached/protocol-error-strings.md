---
id: computing-software.database-administration.memcached.protocol-error-strings
name: protocol-error-strings
category: computing-software
field: database-administration
product: memcached
tags: [error, client-error, server-error, protocol, troubleshooting]
level: practitioner
status: docs-checked
description: "Interpret ERROR, CLIENT_ERROR and SERVER_ERROR replies and when the server closes the connection."
sources:
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Three kinds of error line:
- `ERROR
`: nonexistent command name. Command names are lower-case and case-sensitive.
- `CLIENT_ERROR <text>
`: input does not follow the protocol (bad flags, bad length, bad key).
- `SERVER_ERROR <text>
`: the server cannot carry out the command. For severe errors that make continuing impossible, the server closes the connection after the line. This is the only case in which the server closes a connection to a client.

Clients must allow for these on any command.

Other replies: `NOT_STORED`, `EXISTS`, `NOT_FOUND` are normal outcomes, not errors. Slab/LRU commands return `ERROR [message]`, `BUSY`, `BADCLASS`.

Auth failure: `CLIENT_ERROR [message]`.

## Checked

2026-11-04. Confirmed against protocol.txt (ERROR, CLIENT_ERROR, SERVER_ERROR meanings, connection close rule, BUSY, BADCLASS). Removed: the watch connevents tip, which is not in the sources.

Method: documentation only; no commands were run.
