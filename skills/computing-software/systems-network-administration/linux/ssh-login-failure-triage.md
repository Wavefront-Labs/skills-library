---
id: computing-software.systems-network-administration.linux.ssh-login-failure-triage
name: ssh-login-failure-triage
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, ssh-login-failure, permission-denied-publickey, sshd-debug, authorized-keys-permissions, ssh-vvv, pam-sshd]
level: practitioner
status: docs-checked
description: "Triage SSH login failures methodically: client ssh -vvv, server logs, sshd -T and debug mode, key and directory permissions, PAM, SELinux contexts, AllowUsers, and lockouts."
sources:
  - https://github.com/openssh/openssh-portable/blob/master/ssh.1
  - https://github.com/openssh/openssh-portable/blob/master/sshd_config.5
  - https://github.com/openssh/openssh-portable/blob/master/sshd.8
  - https://github.com/fail2ban/fail2ban/blob/master/man/fail2ban-client.1
  - https://github.com/SELinuxProject/selinux/blob/main/policycoreutils/setfiles/restorecon.8
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SSH login failure triage

Work from both ends: what the client tried, and why the server said no. The client message alone (`Permission denied (publickey)`) hides the reason by design.

## 1. Client side
```bash
ssh -vvv alice@web1 2>&1 | grep -E 'Connecting|Offering|Authentications that can continue|Server accepts|denied|kex|no matching'
```
| Output | Meaning |
|---|---|
| `Connection refused` | nothing listening on that port / sshd down |
| `Connection timed out` | firewall, routing, security group |
| `no matching ...` errors for host key type or key exchange | algorithm mismatch (old device or crypto policy) |
| `Offering public key: ... ` then `Authentications that can continue: publickey` | server rejected that key |
| `REMOTE HOST IDENTIFICATION HAS CHANGED` | host key changed: verify out of band, then `ssh-keygen -R web1` |
| `Too many authentication failures` | agent offered too many keys; use `-o IdentitiesOnly=yes -i key` |

## 2. Server logs
```bash
journalctl -u sshd -u ssh --since -15min      # the unit is named sshd or ssh depending on the distribution
```
Or read the authentication log your syslog writes. Typical causes to look for:
- a permission refusal for the home directory or `~/.ssh` -> permissions (below).
- the user rejected by `AllowUsers`/`AllowGroups`/`DenyUsers` -> check those directives.
- a locked or expired account -> `chage -l`, `passwd -S`.
- pam_faillock lockout -> `faillock --user alice --reset`.
- a client offering only the SHA-1 `ssh-rsa` signature -> not in the default `PubkeyAcceptedAlgorithms`; use ed25519 or an RSA key with `rsa-sha2-*`.

## 3. Permissions (StrictModes)
```bash
chmod go-w ~alice; chmod 700 ~alice/.ssh; chmod 600 ~alice/.ssh/authorized_keys
chown -R alice: ~alice/.ssh
restorecon -Rv ~alice/.ssh             # SELinux: restore the policy default labels after copying files
```

## 4. Effective config and debug server
```bash
sshd -T | grep -iE 'passwordauth|pubkeyauth|permitroot|allowusers|authorizedkeysfile|match'
sshd -T -C user=alice,host=1.2.3.4,addr=1.2.3.4    # evaluates Match blocks for that connection
/usr/sbin/sshd -d -p 2222                           # one-shot debug server on another port; connect with ssh -p 2222
```
First value wins in sshd_config: an earlier `PasswordAuthentication no` in an included file beats a later `yes`.

## 5. Other causes
- Expired password or account (`chage -l alice`) - key auth still triggers `account` PAM checks.
- `AuthorizedKeysCommand` (sssd/LDAP) failing; test with `sss_ssh_authorizedkeys alice`.
- fail2ban banned the client IP: check `fail2ban-client status sshd`.

## Verify
- [ ] Root cause recorded (log line), fix applied, `ssh -o BatchMode=yes alice@web1 true` succeeds.
- [ ] Keep a second session open whenever changing sshd config; `sshd -t` before reload.

## Checked
Checked 2026-10-25 against OpenSSH portable master manual sources (ssh.1, ssh_config.5, sshd.8, sshd_config.5, ssh-keygen.1, ssh-add.1, scp.1, sftp.1), fail2ban-client(1) and restorecon(8).
Confirmed: `-v`, `sshd -T` and `sshd -T -C user=...,host=...,addr=...`, `sshd -d -p`, `sshd -t`, StrictModes, first-value-wins ordering, `BatchMode`, the default PubkeyAcceptedAlgorithms (no `ssh-rsa`), AllowUsers/AllowGroups/DenyUsers, `faillock --reset`, `chage -l`, `sss_ssh_authorizedkeys`, `fail2ban-client status <jail>`, `restorecon -R -v`.
Removed as unconfirmed: exact sshd log message texts, distribution log file paths, the `ssh_home_t` label name, NFS home SELinux boolean and fcontext advice, and the disk-full cause.

Method: documentation only; no commands were run.
