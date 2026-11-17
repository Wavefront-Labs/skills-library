---
id: computing-software.systems-network-administration.linux.ssh-client-config-proxyjump-and-multiplexing
name: ssh-client-config-proxyjump-and-multiplexing
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, ssh, openssh, ssh-config-file, host-aliases, proxyjump, bastion, controlmaster, ssh-multiplexing, serveraliveinterval, ssh-keepalive, escape-sequences, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Make ssh fast and reliable with ~/.ssh/config: Host aliases, ProxyJump through bastions, ControlMaster multiplexing, keepalives, and ~ escape sequences."
sources:
  - https://github.com/openssh/openssh-portable/blob/master/ssh_config.5
  - https://github.com/openssh/openssh-portable/blob/master/ssh.1
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ssh client config: aliases, ProxyJump, multiplexing, keepalive

**Goal:** `ssh db1` just works through the bastion with the right user and key, repeat
connections open instantly, and idle sessions don't die behind NAT/firewalls.

## 1. ~/.ssh/config basics
First match wins per option, so put specific `Host` blocks before general ones.
```sshconfig
Host bastion
    HostName bastion.example.com
    User alice
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes                 # don't offer every agent key (avoids "Too many authentication failures")

Host db1 db2 app-*
    HostName %h.internal.example.com
    User ops
    ProxyJump bastion

Host *
    AddKeysToAgent yes
    ServerAliveInterval 30
    ServerAliveCountMax 4
    ControlMaster auto
    ControlPath ~/.ssh/cm-%C
    ControlPersist 10m
```
System-wide defaults: `/etc/ssh/ssh_config`. Check the
result: `ssh -G db1 | grep -E '^(hostname|user|proxyjump|identityfile)'`.

## 2. ProxyJump (bastions)
```bash
ssh -J alice@bastion ops@db1.internal              # ad hoc
ssh -J bastion1,bastion2 target                    # chain
scp -J bastion file db1:/tmp/; rsync -e 'ssh -J bastion' …
```
End-to-end encrypted: the bastion only forwards TCP; your key/agent never sits on it (unlike
agent forwarding). Older clients: `ProxyCommand ssh -W %h:%p bastion`.

## 3. Multiplexing (ControlMaster)
First connection becomes master; later ssh/scp/git/ansible to the same host reuse its TCP+auth
session — no handshake, no 2FA prompt again.
```bash
ssh -O check db1      # master running?
ssh -O exit db1       # ask the master to exit (after changing config or when a stuck master blocks new sessions)
```
`%C` is a hash of the local host, remote host, port and user; the docs recommend including at least `%h`, `%p` and `%r` (or `%C`) in `ControlPath` and keeping the socket in a directory other users cannot write.

## 4. Keepalives and escapes
- `ServerAliveInterval 30` + `ServerAliveCountMax 4`: client probes every 30 s inside the
  encrypted channel; disconnects after 2 min of no answer (instead of hanging forever). Server
  side equivalent: `ClientAliveInterval`.
- `TCPKeepAlive` messages are spoofable; server-alive messages travel inside the encrypted channel.
- Escape sequences (after Enter): `~.` kill a frozen session, `~^Z` suspend, `~#` list
  forwardings, `~C` command line (add forwardings: `-L 8080:localhost:80`), `~?` help.

## Gotchas
- `Host *` at the top overrides everything below it for options it sets.
- A stale ControlMaster with a dead network keeps new sessions hanging — `ssh -O exit` or delete the socket.
- `StrictHostKeyChecking no` in config to "make warnings go away" disables MITM protection; manage known_hosts instead.

## Verify
- [ ] `ssh -G <alias>` shows the intended hostname/user/proxyjump.
- [ ] Second `ssh db1 true` returns in well under a second (multiplexed).
- [ ] An idle session survives > 15 minutes through the firewall.

## Checked
Checked 2026-10-25 against OpenSSH portable master manual sources (ssh.1, ssh_config.5, sshd.8, sshd_config.5, ssh-keygen.1, ssh-add.1, scp.1, sftp.1).
Confirmed: first-obtained-value rule for ssh_config, `ProxyJump` syntax and comma chains, `ssh -J`, `ssh -G`, `ssh -O check|exit`, `ControlMaster`/`ControlPath`/`ControlPersist` and the `%C` token recommendation, `ServerAliveInterval` (default 0) and `ServerAliveCountMax`, `TCPKeepAlive` being spoofable, `ClientAliveInterval` as the server-side counterpart, `AddKeysToAgent`, `IdentitiesOnly`, and the escape sequences `~.`, `~^Z`, `~#`, `~C`, `~?`.
Removed as unconfirmed: the ssh_config.d directory, the Unix socket path length figure and the bulk-transfer advice.

Method: documentation only; no commands were run.
