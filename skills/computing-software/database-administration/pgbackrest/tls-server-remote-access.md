---
id: computing-software.database-administration.pgbackrest.tls-server-remote-access
name: tls-server-remote-access
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, tls-server, repo-host-type, certificates, remote]
level: advanced
status: docs-checked
description: "Use the pgBackRest TLS server instead of SSH for remote repository or database hosts."
sources:
  - https://pgbackrest.org/command.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: replace SSH with certificate-authenticated TLS.

Set `repo-host-type=tls` (repository access) or `pg-host-type=tls` (database access); the default for both is `ssh`. With TLS the host port defaults to 8432 for `repo-host-port`.

The `server` command runs the TLS server:

- `tls-server-address`: where it listens (default `localhost`; `*` for all).
- `tls-server-port`: default 8432.
- `tls-server-cert-file` and `tls-server-key-file`: identify the server.
- `tls-server-ca-file`: checks that client certificates are signed by a trusted CA.
- `tls-server-auth`: authorizes clients by certificate CN, for example `client-cn=stanza1,stanza2`; use `client-cn=*` for all stanzas. Wildcards may not be used in the CN itself.

```
[global]
tls-server-address=*
tls-server-ca-file=/path/to/server.ca
tls-server-cert-file=/path/to/server.crt
tls-server-key-file=/path/to/server.key
tls-server-auth=client-cn=*
```

Clients use `repo1-host-cert-file`, `repo1-host-key-file` and CA file options to prove identity; `pg1-host-cert-file` and `pg1-host-ca-file` exist for the database side.

`server-ping` checks a TLS server is accepting connections; it is an aliveness check only, with no authentication attempted.

The `server` command is what listens on the repository or database host; clients connect to the address and port configured through the host options, and authorization is checked against the certificate CN.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest Command Reference (pgbackrest.org/command.html) (server, server-ping). Nothing needed removing. 

Method: documentation only; no commands were run.
