---
id: computing-software.systems-network-administration.linux.debug-ssh-client-authentication
name: debug-ssh-client-authentication
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, ssh, ssh-verbose, ssh-debugging, permission-denied-publickey, ssh-v, sshd-debug, known-hosts]
level: practitioner
status: docs-checked
description: "Diagnose 'Permission denied (publickey)' and other SSH client failures with ssh -vvv: offered keys, server replies, agent issues, file modes and server logs."
sources:
  - https://github.com/openssh/openssh-portable/blob/master/ssh.1
  - https://github.com/openssh/openssh-portable/blob/master/sshd.8
  - https://github.com/openssh/openssh-portable/blob/master/ssh_config.5
  - https://github.com/openssh/openssh-portable/blob/master/sshd_config.5
  - https://github.com/openssh/openssh-portable/blob/master/ssh-add.1
  - https://github.com/SELinuxProject/selinux/blob/main/policycoreutils/setfiles/restorecon.8
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging SSH client authentication

## Read the verbose output
```bash
ssh -v alice@host          # -vv / -vvv for more
```
`-v` prints debugging messages about connection, authentication and configuration. Read them for:
- which configuration files and `Host` blocks were applied;
- whether the TCP connection was established;
- the server host key and the known_hosts check;
- the authentication methods the server will continue with;
- each identity offered, and whether the server accepted it (a key offered with no acceptance was rejected);
- the final failure when no method is left.

## Client-side causes
- Too many keys in the agent → server's `MaxAuthTries` (default 6) exceeded before the right one: `ssh -o IdentitiesOnly=yes -i ~/.ssh/key host`.
- Key not loaded/agent not reachable: `ssh-add -l` lists the identities the agent holds.
- Wrong user (config `User`) or host alias pointing elsewhere: `ssh -G host | grep -E '^(user|hostname|identityfile)'`.
- Deprecated key types: `ssh-rsa` (SHA-1) disabled on new servers — use ed25519 or `-o PubkeyAcceptedAlgorithms=+rsa-sha2-256`.

## Server-side causes (need access or an admin)
```bash
journalctl -u sshd -n 50     # unit name varies by distribution; look for a permission (StrictModes) refusal
```
- `~`, `~/.ssh` and `authorized_keys` must not be writable by others (StrictModes); the recommended modes are user-only access, e.g. `~/.ssh` 700 and `authorized_keys` 600.
- On SELinux systems a wrong file label can block sshd; `restorecon -Rv ~/.ssh` restores the policy default.
- `AllowUsers/AllowGroups`, `DenyUsers`, `PubkeyAuthentication no`, Match blocks.
- Debug server instance: `sudo /usr/sbin/sshd -d -p 2222` then `ssh -p 2222 -v host`.

## Verify
- [ ] `ssh -v` shows the key being accepted and public key authentication completing.

## Checked
Checked 2026-10-25 against OpenSSH portable master manual sources (ssh.1, ssh_config.5, sshd.8, sshd_config.5, ssh-keygen.1, ssh-add.1, scp.1, sftp.1) and restorecon(8).
Confirmed: `-v` behaviour, `IdentitiesOnly`, `ssh -G`, `PubkeyAcceptedAlgorithms` with the `+` append syntax and the default list without `ssh-rsa`, MaxAuthTries default 6, StrictModes and recommended permissions, AllowUsers/AllowGroups/DenyUsers, `sshd -d -p`, `ssh-add -l`, `restorecon -R -v`.
Removed as unconfirmed: the quoted debug and log message texts.

Method: documentation only; no commands were run.
