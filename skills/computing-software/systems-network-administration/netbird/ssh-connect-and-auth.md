---
id: computing-software.systems-network-administration.netbird.ssh-connect-and-auth
name: ssh-connect-and-auth
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, netbird-ssh, jwt-authentication, machine-identity, openssh-client]
level: practitioner
status: docs-checked
description: "Connect to NetBird SSH servers with netbird ssh or native OpenSSH, choose JWT versus machine identity authentication, cache JWTs, and know the limitations."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/peers/ssh.mdx
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/get-started/cli.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Connect:
```
netbird ssh user@<peer-ip>
netbird ssh user@<peer-ip> "uptime"
netbird ssh -L 8080:localhost:80 user@<peer-ip>
netbird ssh -R 8080:localhost:3000 user@<peer-ip>
```
Native OpenSSH (`ssh`, `sftp`, `scp`) also works through a drop-in file NetBird creates (`/etc/ssh/ssh_config.d/99-netbird.conf` on Linux). Only OpenSSH clients are supported; PuTTY is not.

Authentication:
- JWT (default): each new session needs an OIDC login unless cached. Enable caching on the client: `netbird up --ssh-jwt-cache-ttl <seconds>` (default 0, disabled; cached tokens expire at the TTL or when the daemon restarts). The CLI reference says the receiving SSH server rejects tokens older than 10 minutes, so values above 600 cause authentication failures for cached tokens. The server clock must be synchronized with the IdP or validation fails.
- Machine identity: any peer allowed by ACLs can connect; no per-user audit trail and no fine-grained access. Enable with `netbird up --allow-server-ssh --disable-ssh-auth`.

`netbird ssh` also takes `-p/--port`, `-u/--user`, `--no-cache`, `--no-browser`, `--strict-host-key-checking`.

Limitations:
- Port forwarding works only with `netbird ssh`, not native `ssh -L/-R`.
- No port forwarding on Windows servers; only when connecting as the user running NetBird.
- User switching requires root/administrator.
- Linux, macOS, Windows and FreeBSD fully supported; Android is server-only.

## Checked

2026-11-04: read the SSH Access page in full and the CLI page ssh section. Confirmed commands, the OpenSSH drop-in file and OpenSSH-only support, JWT versus machine identity, the cache flag and default, client flags, limitations and platform support. Replaced the 3600 second cache example, which conflicts with the CLI page note that the server rejects tokens older than 10 minutes.

Method: documentation only; no commands were run.
