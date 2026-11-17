---
id: computing-software.systems-network-administration.linux.ssh-port-forwarding-local-remote-dynamic
name: ssh-port-forwarding-local-remote-dynamic
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, ssh, openssh, ssh-tunnels, local-forwarding, remote-forwarding, dynamic-forwarding, socks-proxy, gatewayports, agent-forwarding, ssh-agent-forwarding, autossh, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Tunnel with SSH: -L local, -R remote and -D SOCKS forwarding, bind addresses and GatewayPorts, persistent tunnels with autossh, server controls, and agent forwarding risks."
sources:
  - https://github.com/openssh/openssh-portable/blob/master/ssh.1
  - https://github.com/openssh/openssh-portable/blob/master/ssh_config.5
  - https://github.com/openssh/openssh-portable/blob/master/sshd_config.5
  - https://github.com/openssh/openssh-portable/blob/master/sshd.8
  - https://github.com/curl/curl/blob/master/docs/cmdline-opts/socks5-hostname.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSH port forwarding (-L, -R, -D) and agent forwarding

**Goal:** reach services behind firewalls through SSH, expose a local service to a remote
network temporarily, and know which forwarding is a security risk.

## 1. Local forwarding (-L): reach a remote-side service from here
```bash
ssh -L 5432:db1.internal:5432 bastion            # localhost:5432 → (via bastion) → db1:5432
ssh -L 127.0.0.1:8443:localhost:443 web01         # remote host's own localhost service
ssh -fN -L 3306:localhost:3306 db1                # -f background, -N no remote command
```
Bind defaults to 127.0.0.1 (unless `GatewayPorts yes` in client config) — keep it that way.

## 2. Remote forwarding (-R): expose a local service on the remote side
```bash
ssh -R 9000:localhost:3000 server                 # server's localhost:9000 → my localhost:3000
ssh -R 0.0.0.0:9000:localhost:3000 server         # listen on all server interfaces — needs GatewayPorts clientspecified/yes in sshd_config
ssh -R 1080 server                                 # no destination given: the local ssh acts as a SOCKS 4/5 proxy for the remote listener
```
Use for reverse access from behind NAT (support sessions) — and treat as a firewall bypass.

## 3. Dynamic forwarding (-D): SOCKS proxy
```bash
ssh -D 1080 -fN bastion
curl --socks5-hostname localhost:1080 http://intranet.internal/
```
`--socks5-hostname`/browser "proxy DNS" so names resolve on the far side.

## 4. Persistent tunnels
```bash
ssh -N -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -L 5432:db1:5432 bastion
```
Run it from a supervisor such as a systemd unit running that command with `Restart=always` and a
dedicated key restricted on the server (`permitopen="db1:5432"`, `no-pty`, `command="/bin/false"`).

## 5. Agent forwarding (-A)
Lets the remote host use your local agent to authenticate onward. Users able to bypass file permissions on that
host (the agent's socket) can use the agent to authenticate with your loaded identities while you're connected; they cannot read the key material. Prefer
**ProxyJump**. If you must: only to trusted hosts, `ssh-add -c` (confirm each use), and
`ForwardAgent` per Host block, never `Host *`.

## 6. Server-side controls (sshd_config)
`AllowTcpForwarding no|local|remote|yes`, `PermitOpen host:port`, `GatewayPorts no`,
`AllowAgentForwarding no`, `PermitListen` (for -R), per-user via `Match User`/`Match Group`.
Disabling forwarding doesn't stop users with shell access from running their own forwarders.

## Gotchas
- "bind: Address already in use" → local port taken; "remote port forwarding failed" → server policy or port in use. `-o ExitOnForwardFailure=yes` makes scripts fail loudly.
- Privileged ports (< 1024) need root on the listening side.
- Long-lived tunnels die silently without ServerAlive settings.

## Verify
- [ ] `ss -ltnp | grep <port>` shows the listener bound to 127.0.0.1 (unless intended otherwise).
- [ ] The service answers through the tunnel; `~#` in the session lists the forwarding.

## Checked
Checked 2026-10-25 against OpenSSH portable master manual sources (ssh.1, ssh_config.5, sshd.8, sshd_config.5, ssh-keygen.1, ssh-add.1, scp.1, sftp.1) and curl's socks5-hostname option page.
Confirmed: `-L`, `-R`, `-D` (SOCKS4/5) forms, `-R port` acting as a SOCKS proxy when no destination is given, `-N`, `-f`, default loopback binding and `GatewayPorts` on both client and server, `ExitOnForwardFailure`, privileged ports needing root, `AllowTcpForwarding` values (yes/all, no, local, remote), `PermitOpen`, `PermitListen`, `AllowAgentForwarding`, authorized_keys `permitopen`, `no-pty`, `command`, ForwardAgent risk wording, and `curl --socks5-hostname`.
Removed as unconfirmed: the autossh example and the OpenSSH 7.6 version gate.

Method: documentation only; no commands were run.
