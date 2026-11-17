---
id: computing-software.database-administration.memcached.unix-socket-listener
name: unix-socket-listener
category: computing-software
field: database-administration
product: memcached
tags: [unix-socket, domain-socket, s, networking, local-only]
level: practitioner
status: docs-checked
description: "Serve memcached over a unix domain socket with -s to restrict access to one local user; TCP and UDP are disabled when used."
sources:
  - https://docs.memcached.org/serverguide/configuring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

To restrict a daemon to a single local user, or to avoid network exposure, use a unix domain socket:

```
memcached -s /path/to/memcached.sock
```
Gotcha: enabling -s disables TCP and UDP, so remote and TCP clients can no longer connect.

`stats settings` reports `domain_socket` (NULL when unused) and `umask` (the docs sample shows 700).

Verify: run `stats settings` through the socket and look for `STAT domain_socket`, TCP and UDP should no longer be listening.

## Checked

Confirmed 2026-11-09: `-s <file>` restricts the daemon to a unix domain socket for a single local user, enabling it disables TCP and UDP, and `stats settings` shows `domain_socket` and `umask` (sample 700) (Configuring page). Removed the `netstat` verification command, which the page does not cover.

Method: docs-checked 2026-11-09 against docs.memcached.org Configuring page
