---
id: computing-software.systems-network-administration.linux.ssh-keys-from-ldap-sss-ssh-authorizedkeys
name: ssh-keys-from-ldap-sss-ssh-authorizedkeys
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, sssd, sss-ssh-authorizedkeys, ldap-ssh-keys, authorizedkeyscommand, freeipa, openssh-lpk]
level: advanced
status: docs-checked
description: "Serve SSH public keys from LDAP or FreeIPA via SSSD: sshPublicKey attributes, AuthorizedKeysCommand sss_ssh_authorizedkeys, caching, testing and key revocation."
sources:
  - https://github.com/SSSD/sssd/blob/master/src/man/sss_ssh_authorizedkeys.1.xml
  - https://github.com/SSSD/sssd/blob/master/src/man/sssd-ldap-attributes.5.xml
  - https://github.com/SSSD/sssd/blob/master/src/man/sssd.conf.5.xml
  - https://github.com/openssh/openssh-portable/blob/master/sshd_config.5
  - https://github.com/freeipa/freeipa/blob/master/ipaserver/plugins/baseuser.py
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SSH keys from LDAP with SSSD

**Why:** no `authorized_keys` files scattered over hundreds of hosts; removing a key in the directory revokes access everywhere.

## Directory side
- FreeIPA: `ipa user-mod alice --sshpubkey="ssh-ed25519 AAAA... alice@laptop"` (built in).
- Other LDAP servers: store keys in an attribute and point SSSD at it with `ldap_user_ssh_public_key` (default attribute name `sshPublicKey`).

## SSSD
`/etc/sssd/sssd.conf`:
```ini
[sssd]
services = nss, pam, ssh, sudo
[domain/example.com]
ldap_user_ssh_public_key = sshPublicKey      # attribute holding the keys (this is the default)
```
`systemctl restart sssd`.

## sshd
```
AuthorizedKeysCommand /usr/bin/sss_ssh_authorizedkeys
AuthorizedKeysCommandUser nobody
```
(IPA clients get this via `ipa-client-install`.) `sshd -t && systemctl reload sshd`.
Local `~/.ssh/authorized_keys` still applies too unless you set `AuthorizedKeysFile none`.

## Test
```bash
sss_ssh_authorizedkeys alice           # prints keys sshd will see
ssh -v alice@host                      # 'Offering public key' then accepted
```
## Caching and revocation
SSSD caches directory entries (see `entry_cache_timeout`); after removing a key: `sss_cache -u alice` on hosts, or wait for expiry.
Know your cache timeout for emergency revocation.

## Verify
- [ ] Login works with a directory-only key; deleting it and clearing cache denies access.

## Checked
Checked 2026-10-25 against SSSD master manual sources (sssd.conf(5), sssd-ldap-attributes(5), sss_ssh_authorizedkeys(1)), the FreeIPA user plugin source and OpenSSH sshd_config(5).
Confirmed: `ssh` as an sssd service, `ldap_user_ssh_public_key` with default `sshPublicKey`, `sss_ssh_authorizedkeys` outputting authorized_keys format for use with AuthorizedKeysCommand, `entry_cache_timeout`, `sss_cache -u`, and the FreeIPA `sshpubkey` user attribute.
Removed as unconfirmed: the openssh-lpk objectClass name, the Active Directory attribute suggestion and the offline-cache statement.

Method: documentation only; no commands were run.
