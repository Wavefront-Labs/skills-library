---
id: computing-software.database-administration.postgresql.preventing-server-spoofing
name: preventing-server-spoofing
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, server-spoofing, unix-socket-directories, requirepeer, verify-full, sslmode, security]
level: practitioner
status: docs-checked
description: "Stop a rogue process impersonating PostgreSQL: lock down the Unix socket directory, use requirepeer for local sockets and sslmode=verify-full over TCP."
sources:
  - https://www.postgresql.org/docs/current/preventing-server-spoofing.html
  - https://www.postgresql.org/docs/current/runtime-config-connection.html
  - https://www.postgresql.org/docs/current/libpq-ssl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Preventing server spoofing

**Threat:** while the real server is down (restart, crash, upgrade), any local user can bind port 5432 or create the socket file and harvest passwords or feed fake results to clients.

## Local (Unix-domain socket) connections
1. Put the socket in a directory that has write permission only for a trusted local user (the docs: this prevents a malicious user from creating their own socket file there):
   ```ini
   # postgresql.conf (server start)
   unix_socket_directories = '/var/run/postgresql'
   unix_socket_permissions = 0777        # default: anyone can connect; the directory permissions are what stop spoofing
   ```
   ```bash
   install -d -o postgres -g postgres -m 0755 /var/run/postgresql
   ```
   If some applications might still use `/tmp` for the socket file, create a symbolic link `/tmp/.s.PGSQL.5432` pointing at the relocated socket during operating system startup, and make sure your `/tmp` cleanup does not remove it.
2. Make clients check the peer: in the libpq connection string add `requirepeer=postgres`. libpq refuses the connection if the socket is owned by another OS user.
   ```bash
   psql "host=/var/run/postgresql dbname=app requirepeer=postgres"
   ```

## TCP connections
- Server: SSL key and certificate files, and `pg_hba.conf` that accepts only `hostssl` connections.
- Client: `sslmode=verify-ca` or `verify-full` with the appropriate root certificate (`sslrootcert=<CA_FILE>`), or `sslrootcert=system` (the system CA pool; `verify-full` is then forced). The docs also allow GSSAPI encryption instead of, or as well as, SSL.
- Put the setting in `PGSSLMODE`, a service file (`pg_service.conf`) or the connection string so nobody forgets it.
- For `scram-sha-256` over a network, connect with SSL and one of the anti-spoofing methods above; the docs add that libpq's SCRAM cannot protect the whole exchange by itself, and point to `channel_binding=require` on the client.

## Verify
```bash
ls -ld /var/run/postgresql            # owner postgres, not world-writable
psql "host=db1 sslmode=verify-full sslrootcert=ca.crt" -c "SELECT ssl, version FROM pg_stat_ssl WHERE pid = pg_backend_pid()"
```
Test the negative: connect with a wrong hostname (an IP instead of the cert CN/SAN) and confirm verify-full fails.

## Gotchas
- The spoofing the docs describe is by a local user starting their own server while the real one is down: it could read passwords and queries sent by clients but could not return data, since `PGDATA` stays protected by directory permissions. Limit shell access to database servers.
- With `verify-full`, the certificate must match the host name the client connects to; list every name clients use (including VIPs and DNS aliases).

## Checked
2026-10-25. Against PostgreSQL 18 documentation (REL_18_STABLE doc/src/sgml, branch head 2026-10-24; PostgreSQL 19 is still at release-candidate stage): Preventing Server Spoofing section (local user spoofing a down server; socket directory writable only by a trusted user; `/tmp/.s.PGSQL.5432` symlink advice; `requirepeer`; `hostssl`-only server, `sslmode=verify-ca` or `verify-full`, `sslrootcert=system` forcing `verify-full`; GSSAPI encryption alternative; SCRAM with SSL and channel binding), `unix_socket_directories` and `unix_socket_permissions` (default 0777), and libpq `channel_binding`. Removed the systemd `RuntimeDirectory` tip, the sticky-bit remark, the `require` remark beyond the docs, and the JDBC driver claim, which the documentation does not give.
Method: documentation only; no commands were run.
