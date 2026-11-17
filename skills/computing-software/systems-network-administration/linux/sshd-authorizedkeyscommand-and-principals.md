---
id: computing-software.systems-network-administration.linux.sshd-authorizedkeyscommand-and-principals
name: sshd-authorizedkeyscommand-and-principals
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, sshd, authorizedkeyscommand, authorizedprincipalsfile, ssh-ca, central-keys, sshd-config]
level: advanced
status: docs-checked
description: "Fetch SSH keys or certificate principals dynamically: AuthorizedKeysCommand contract, AuthorizedPrincipalsFile for SSH CA roles, permissions and testing."
sources:
  - https://github.com/openssh/openssh-portable/blob/master/sshd_config.5
  - https://github.com/openssh/openssh-portable/blob/master/ssh-keygen.1
  - https://github.com/openssh/openssh-portable/blob/master/ssh_config.5
  - https://github.com/SSSD/sssd/blob/master/src/man/sss_ssh_authorizedkeys.1.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AuthorizedKeysCommand and AuthorizedPrincipals

## AuthorizedKeysCommand
sshd runs a program to obtain authorized keys for the user logging in.
```
AuthorizedKeysCommand /usr/local/sbin/ssh-keys-from-api %u %f
AuthorizedKeysCommandUser sshkeys        # dedicated unprivileged user
```
Contract: print authorized_keys-format lines to stdout, exit 0. Tokens: `%u` user, `%f` fingerprint of the offered key,
`%k` key, `%t` key type, `%h` home. (the manual requires the program to be owned by root, not writable by group or others, and given by absolute path).
Make it fast and fail-closed (timeout, cache) — it runs on every key offered.
A common implementation is `sss_ssh_authorizedkeys` (SSSD).

## SSH certificates and principals
With `TrustedUserCAKeys /etc/ssh/user_ca.pub`, a certificate is accepted if one of its principals matches.
Without a principals file, the username must appear in the certificate's principals. Map roles instead:
```
AuthorizedPrincipalsFile /etc/ssh/principals/%u
```
`/etc/ssh/principals/deploy`:
```
ops-team
release-bot
```
Now any cert with principal `ops-team` can log in as `deploy`. Dynamic variant: `AuthorizedPrincipalsCommand /usr/local/sbin/principals %u` + `AuthorizedPrincipalsCommandUser`.

## Test
```bash
sshd -t ; sshd -T | grep -i authorized
sudo -u sshkeys /usr/local/sbin/ssh-keys-from-api alice      # run the command exactly as sshd would
ssh -v -i ~/.ssh/id_ed25519 -o CertificateFile=~/.ssh/id_ed25519-cert.pub deploy@host   # then read sshd's log
```

## Gotchas
- A crashing/slow command blocks logins — keep a local break-glass key (`AuthorizedKeysFile`) for emergencies.
- Output larger than needed or including `command=` restrictions is honoured — the command controls access fully.

## Verify
- [ ] Login works via the command or cert principal; removing the user from the source denies access within the cache window.

## Checked
Checked 2026-10-25 against OpenSSH portable master manual sources (ssh.1, ssh_config.5, sshd.8, sshd_config.5, ssh-keygen.1, ssh-add.1, scp.1, sftp.1) and SSSD sss_ssh_authorizedkeys(1).
Confirmed: AuthorizedKeysCommand and AuthorizedKeysCommandUser semantics and ownership rule, token list (%u user, %f fingerprint, %k key, %t key type, %h home), AuthorizedPrincipalsFile and AuthorizedPrincipalsCommand (and its user setting), TrustedUserCAKeys, `sshd -T`, and that the command output is authorized_keys format.
Removed as unconfirmed: the parent-directory ownership rule, the exact refusal message and the third-party implementations list.

Method: documentation only; no commands were run.
