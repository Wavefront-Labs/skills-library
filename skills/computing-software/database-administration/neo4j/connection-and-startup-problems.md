---
id: computing-software.database-administration.neo4j.connection-and-startup-problems
name: connection-and-startup-problems
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, port-7687, auth-failed, lock-file, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Boot and connectivity"
sources:
  - https://neo4j.com/docs/operations-manual/current/configuration/set-initial-password/
  - https://neo4j.com/docs/operations-manual/current/authentication-authorization/password-and-user-recovery/
  - https://neo4j.com/docs/operations-manual/current/installation/linux/tarball/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connection and startup problems

Goal: diagnose connection and startup failures.
- Check the listen and advertised address settings.
- `neo4j-admin dbms set-initial-password` is for use once, before the first startup. To recover a forgotten password later, follow the password and user recovery page (it temporarily disables authentication and restricts `server.default_listen_address`).
Verify: Bolt connection succeeds from a client host.

## Checked

2026-11-02. Confirmed in the set-initial-password and password-and-user-recovery pages. Removed: the claim that set-initial-password resets a forgotten password (wrong; it is first-start only), and the lock-file and store-version causes (not read).
Method: documentation only; no commands were run.
