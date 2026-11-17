---
id: computing-software.database-administration.postgresql.ssh-tunnel-connections
name: ssh-tunnel-connections
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, ssh-tunnel-postgres, port-forwarding, bastion, remote-access, security]
level: practitioner
status: docs-checked
description: "Reach a PostgreSQL server that only listens on localhost through an SSH local port forward or a bastion jump host, and keep the tunnel alive."
sources:
  - https://www.postgresql.org/docs/current/ssh-tunnels.html
  - https://man.openbsd.org/ssh
  - https://man.openbsd.org/ssh_config
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secure TCP/IP connections with SSH tunnels

Use when the database must not be exposed on the network (`listen_addresses = 'localhost'`) or there is no TLS set up yet.

## Basic forward
```bash
ssh -N -L 63333:localhost:5432 <user>@db1.example.com
psql -h localhost -p 63333 -U app appdb
```
- `-L local_port:target_host:target_port`: `target_host` is resolved **on the SSH server**. `localhost` there means the DB host itself, so the server sees the connection arriving on its localhost address (the default `listen_addresses = 'localhost'` is enough).
- `-N` no remote command. Pick a local port not already used by a local postgres (5432 usually is).
- The local bind address follows the ssh `GatewayPorts` setting unless you give an explicit bind_address (`localhost` binds to loopback only); see ssh and ssh_config man pages.

## Through a bastion
```bash
ssh -N -J <user>@bastion.example.com -L 63333:db1.internal:5432 <user>@bastion.example.com
# or simpler: forward from the bastion directly to the DB's private address
ssh -N -L 63333:db1.internal:5432 <user>@bastion.example.com
```
Second form: traffic bastion -> db1 is plain TCP on the private network; use `sslmode=require` or better if that hop is untrusted.

## Keep it alive / automate
```ini
# ~/.ssh/config
Host pgtunnel
  HostName bastion.example.com
  User <user>
  LocalForward 63333 db1.internal:5432
  ServerAliveInterval 30
  ServerAliveCountMax 3
  ExitOnForwardFailure yes
```
`ssh -fN pgtunnel` backgrounds it; for long-lived use a supervisor such as autossh or a systemd user unit.

## Verify
```bash
ss -ltnp | grep 63333                    # tunnel listening locally
psql -h localhost -p 63333 -c "SELECT 1"
```

## Gotchas
- Tunnel death looks like a dropped DB connection; pools must reconnect. Prefer TLS with verify-full for application traffic and keep tunnels for admin access.
- The server sees every tunnel user as the same source address, so pg_hba.conf cannot distinguish them; rely on role passwords/SCRAM.

## Checked

2026-10-28. Confirmed against PostgreSQL docs section 18.11 (ssh -L 63333:localhost:5432 form, local port any unused port, psql -h localhost -p 63333, hop through a login host is unencrypted on the last leg, listen_addresses = 'localhost') and the ssh_config man page (LocalForward, ExitOnForwardFailure, GatewayPorts and bind_address, ServerAliveInterval). Removed unconfirmed: the pg_hba.conf 127.0.0.1/32 line detail, inet_client_addr() output, the AllowTcpForwarding error text, autossh flags.

Method: documentation only; no commands were run.
