---
id: computing-software.systems-network-administration.netbird.ssh-server-enable
name: ssh-server-enable
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, netbird-ssh, allow-server-ssh, ssh-sftp, ssh-port-forwarding]
level: practitioner
status: docs-checked
description: "Enable the NetBird built-in SSH server on a peer with --allow-server-ssh, optional SFTP, root and port-forwarding flags, and the dashboard policy that permits it."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/peers/ssh.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
NetBird SSH reaches peers over the overlay without exposing port 22 publicly. It is disabled by default. Needs v0.61.0+ on clients and servers.

Enable on the target peer:
```
sudo netbird down
sudo netbird up --allow-server-ssh
```

Optional features:
```
sudo netbird up --allow-server-ssh \
  --enable-ssh-local-port-forwarding \
  --enable-ssh-remote-port-forwarding \
  --enable-ssh-sftp \
  --enable-ssh-root
```
Other flags: `--disable-ssh-auth` (turns off JWT auth), `--ssh-jwt-cache-ttl <seconds>` (default 0, disabled). Disable the server with `netbird down && netbird up --allow-server-ssh=false`.

Enabling the server, root login, or disabling SSH auth needs root (Linux/macOS) or administrator (Windows). Turning them off does not.

Access policy: in Access Control create a policy with Source, Destination, and Protocol set to NetBird SSH (fine-grained) or TCP port 22 (basic). Under SSH Access choose Full Access (any local user) or Limited Access (per-group local user mappings).

Upgrade order when moving to v0.61.0: SSH servers, then SSH clients, then management server and dashboard; upgrading the server first breaks SSH for older peers.

## Checked

2026-11-04: read the SSH Access page in full. Confirmed the default-off state, v0.61.0 requirement, enable and disable commands, the optional flags and the 0 default for the JWT cache TTL, the privilege rule, policy protocol options, Full versus Limited Access and the upgrade order. Nothing removed.

Method: documentation only; no commands were run.
