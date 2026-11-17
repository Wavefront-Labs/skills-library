---
id: computing-software.systems-network-administration.linux.bulk-account-creation-newusers-chpasswd
name: bulk-account-creation-newusers-chpasswd
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, newusers, chpasswd, bulk-users, useradd, password-hashing, user-provisioning]
level: practitioner
status: verified
description: "Create or update many local accounts at once with newusers and chpasswd: input formats, hashing (-c, -e), forcing password change at first login, and safer alternatives."
sources:
  - https://github.com/shadow-maint/shadow/blob/master/man/newusers.8.xml
  - https://github.com/shadow-maint/shadow/blob/master/man/chpasswd.8.xml
  - https://github.com/shadow-maint/shadow/blob/master/man/chage.1.xml
  - https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/user.py
  - https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/filter/password_hash.yml
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Bulk accounts with newusers and chpasswd

## newusers — create/update from passwd-format lines
`users.txt` (`name:password:UID:GID:GECOS:home:shell`; empty UID/GID = allocate):
```
alice:Temp-Pa55-1::::/export/users/alice:/bin/bash
bob:Temp-Pa55-2::::/export/users/bob:/bin/bash
labuser01:Temp-Pa55-3:2001:2000:Lab user 1:/export/users/labuser01:/bin/bash
```
```bash
newusers users.txt                 # creates users, a group for each GID that does not exist yet, and home directories (parent directories must already exist)
for u in alice bob labuser01; do chage -d 0 "$u"; done   # force change at first login
# delete users.txt afterwards: it contains clear-text passwords
```
Existing users get updated (password, GECOS...) — careful running it twice with different data. newusers first creates users with a locked password, then sets the passwords through PAM in a second pass. Newer shadow releases document `newusers -c` (NONE, SHA256 or SHA512); shadow 4.17.4 on Debian 13 has no `-c` (only `-b`, `-r`, `-R`), so the hash follows `ENCRYPT_METHOD` in /etc/login.defs (YESCRYPT there). The home directory is created empty (skel files are not copied) and a missing parent directory makes the line fail without creating the account.

## chpasswd — set passwords only
```bash
printf '%s\n' 'alice:N3w-Pass!' 'bob:0ther-Pass!' | chpasswd          # hashed by PAM by default; -c METHOD or -e change that
chpasswd -e < hashed.txt          # input already hashed (name:hash), generated elsewhere
chpasswd -c SHA512 < plain.txt     # choose the method: SHA256, SHA512, YESCRYPT (MD5, DES, NONE too); Debian 13 rejects BCRYPT, and NONE stores the password in clear text
```
Avoid passwords on command lines (visible in `ps` and shell history); feed via stdin from a protected file or a vault lookup.

## Safer/better options
- Central identity (FreeIPA/AD/LDAP) instead of local accounts on many hosts.
- Ansible `user` module with `password: "{{ pw | password_hash('sha512') }}"` and `update_password: on_create`.
- SSH keys + locked passwords (`passwd -l`) for admin accounts.

## Verify
- [ ] `getent passwd alice`, `chage -l alice` shows "password must be changed"; first login prompts for a new password.

## Checked

2026-10-26. shadow-maint/shadow master (last commit 2026-10-20, release 4.20.3): newusers line format, empty UID/GID handling, group creation, home creation without parent directories, two-pass password handling and -c methods; chpasswd -e, -c methods and PAM-based default hashing. Ansible devel: user module update_password values (always, on_create) and password_hash filter default sha512. Removed the shred, openssl passwd and mkpasswd lines, and the unconfirmed claim that newusers copies /etc/skel. Forcing a change with chage -d 0 relies on shadow(5): a last-change date of 0 means change at next login.

Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container (shadow 4.17.4): newusers with empty and explicit UID/GID, group created for GID 2000, home created empty (no /etc/skel files copied) with the HOME_MODE/UMASK mode, missing parent directory failing with `mkdir ... failed` and no account created, second run leaving one entry, hashes from ENCRYPT_METHOD ($y$); chage -d 0 giving last change 1970-01-01; chpasswd default hash, -c SHA256/SHA512/YESCRYPT/NONE, -e with a pre-made $6$ hash, BCRYPT rejected. Not run: newusers -c (this shadow version has no such option), mkpasswd, Ansible lines.
