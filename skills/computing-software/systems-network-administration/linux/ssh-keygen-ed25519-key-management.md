---
id: computing-software.systems-network-administration.linux.ssh-keygen-ed25519-key-management
name: ssh-keygen-ed25519-key-management
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, ssh, openssh, ssh-keygen, ed25519, ssh-keys, authorized-keys, ssh-copy-id, fido2-keys, ssh-agent, key-rotation, lpic-1, rhcsa, sysadmin]
level: practitioner
status: docs-checked
description: "Create and manage SSH keys properly: ed25519 or FIDO2 (-sk) keys with passphrases, ssh-copy-id and authorized_keys options, ssh-agent, fingerprints, rotation and key revocation."
sources:
  - https://github.com/openssh/openssh-portable/blob/master/ssh-keygen.1
  - https://github.com/openssh/openssh-portable/blob/master/sshd.8
  - https://github.com/openssh/openssh-portable/blob/master/ssh-add.1
  - https://github.com/openssh/openssh-portable/blob/master/ssh.1
  - https://github.com/openssh/openssh-portable/blob/master/sshd_config.5
  - https://github.com/openssh/openssh-portable/blob/master/contrib/ssh-copy-id.1
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ssh-keygen and SSH key management

**Goal:** strong keys, protected at rest, installed with least privilege, and replaceable when
a laptop is lost.

## 1. Generate
```bash
ssh-keygen -t ed25519 -a 100 -C "alice@laptop-2026" -f ~/.ssh/id_ed25519   # -a: KDF rounds for the passphrase (default 32)
ssh-keygen -t ed25519-sk -O resident -O verify-required -C "alice yubikey"  # FIDO authenticator-backed key
ssh-keygen -t rsa -b 4096                                                   # only for legacy servers without ed25519
ssh-keygen -p -f ~/.ssh/id_ed25519            # change/add passphrase
ssh-keygen -y -f ~/.ssh/id_ed25519 > id_ed25519.pub   # regenerate public key from private
ssh-keygen -lf ~/.ssh/id_ed25519.pub          # fingerprint (SHA256:…)
```
Always use a passphrase on human keys; `ssh-agent` makes it painless. Permissions: `~/.ssh` readable, writable
and searchable only by the user; private key readable and writable only by the user — ssh ignores a private key
file that others can access.

## 2. Install
```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub alice@server     # appends to the remote ~/.ssh/authorized_keys (creating file and directory if needed)
```
authorized_keys options restrict what a key can do:
```
from="10.0.0.0/8",no-agent-forwarding,no-port-forwarding,no-pty,command="/usr/local/bin/backup-receive" ssh-ed25519 AAAA… backup@nas
restrict,command="/usr/local/bin/read-data" ssh-ed25519 AAAA… reader@ci
```
`restrict` disables port, agent and X11 forwarding, PTY allocation and `~/.ssh/rc`; re-enable individual items with `pty`, `port-forwarding`, `agent-forwarding`, `X11-forwarding`, `user-rc`.

## 3. Agent
```bash
eval "$(ssh-agent -s)"; ssh-add ~/.ssh/id_ed25519      # -s prints Bourne-shell commands
ssh-add -t 8h ~/.ssh/id_ed25519                        # maximum lifetime
ssh-add -c …                                           # confirm each use
ssh-add -l; ssh-add -D
```
`AddKeysToAgent yes` in `~/.ssh/config` loads keys on first use.

## 4. Rotation and revocation
- Inventory: record each key's fingerprint (`ssh-keygen -lf key.pub`) and a meaningful comment so keys can be
  traced to people and devices.
- Lost laptop: remove its key line everywhere (config management, not by hand), or with an
  SSH CA publish a KRL: `ssh-keygen -k -f /etc/ssh/revoked_keys -s ca.pub lost_key.pub` and
  `RevokedKeys /etc/ssh/revoked_keys` in sshd_config.
- At scale use SSH certificates (`ssh-keygen -s ca -I alice -n alice -V +8h key.pub`) — short-lived, no authorized_keys sprawl.

## Gotchas
- The `ssh-rsa` (SHA-1) signature algorithm is not in the default `PubkeyAcceptedAlgorithms`; `rsa-sha2-256` and `rsa-sha2-512` are — old servers may lack them.
- Writable home, `~/.ssh` or authorized_keys files are rejected while `StrictModes` is on; check the sshd log.
- Private keys copied into CI variables are long-lived secrets; prefer per-job certificates or deploy keys with `restrict`.

## Verify
- [ ] `ssh -v server` shows the ed25519 identity being offered and public key authentication succeeding.
- [ ] Private key file is 600 and passphrase-protected (`ssh-keygen -y -f` prompts).
- [ ] `authorized_keys` entries all have identifiable comments and restrictive options where appropriate.

## Checked
Checked 2026-10-25 against OpenSSH portable master manual sources (ssh.1, ssh_config.5, sshd.8, sshd_config.5, ssh-keygen.1, ssh-add.1, scp.1, sftp.1).
Confirmed: ssh-keygen -a default of 32 rounds, `-t ed25519-sk` with `-O resident` and `-O verify-required`, `-y`, `-p`, `-l`, `-k -f krl -s ca_public`, `-s ... -I -n -V` certificate signing, authorized_keys option names (restrict, command, from, pty, port-forwarding, no-agent-forwarding and the re-enable options), ssh-add `-t`, `-c`, `-l`, `-D`, ssh-agent `-s`, `AddKeysToAgent`, `RevokedKeys`, StrictModes behaviour, and the default PubkeyAcceptedAlgorithms list.
Removed as unconfirmed: OpenSSH version gates, the rrsync example, the authorized_keys fingerprint-listing claim, log message text and desktop keyring advice.

Method: documentation only; no commands were run.
