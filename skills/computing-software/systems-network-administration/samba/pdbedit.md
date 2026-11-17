---
id: computing-software.systems-network-administration.samba.pdbedit
name: pdbedit
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, pdbedit, passdb, account-policy, sam-database, backend-migration]
level: advanced
status: docs-checked
description: "Manage the Samba user database with pdbedit: list, add, modify, delete users, account flags, account policies, and import or export between passdb backends."
sources:
  - https://www.samba.org/samba/docs/current/man-html/pdbedit.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pdbedit
Run as root. The page says it is independent of the passdb backend in use.

Core:
- `pdbedit -L` list `user:uid:fullname`; `-L -v` verbose; `-L -w` smbpasswd format (with `-v` shows hashes)
- `pdbedit -a -u name` add (prompts for password); `-a -m -u machine` machine trust account
- `pdbedit -r -u name [fields]` modify; `-x -u name` delete

Fields: `-f fullname`, `-h homedir`, `-D drive`, `-S logon script`, `-p profile`, `-N description`, `-I domain`, `-U sid|rid`, `-K never` kickoff time, `-Z` reset logon hours, `-z` clear bad-password count, `--set-nt-hash HEX`, `-t` password from stdin, `--force-initialized-passwords`.

Account flags (`-c "[X ]"`): N no password required, D disabled, H home directory required, T temporary duplicate of other account, U regular user, M MNS logon user, W workstation trust, S server trust, L automatic locking, X password does not expire, I domain trust.

Account policy: `pdbedit -P "bad lockout attempt"` shows; `-P "bad lockout attempt" -C 3` sets. Names: minimum password age, reset count minutes, disconnect time, user must logon to change password, password history, lockout duration, min password length, maximum password age, bad lockout attempt. `--policies-reset` restores defaults.

Backend moves:
```
pdbedit -e smbpasswd:/path/to/samba-users.backup
pdbedit -i smbpasswd:/path/to/smbpasswd.old
pdbedit -y -i tdbsam: -e ldapsam:ldap://my.ldap.host
```
`-g` applies import/export to group mappings, `-y` to policies, `-b` picks another backend.

pdbedit does not call the Unix password synchronisation script if `unix password sync` is set; to add a user and sync the password immediately, use `smbpasswd -a`.

## Checked
2026-11-04: options, flags, policy names, import and export examples and the sync note compared with the pdbedit man page. Nothing removed.
Method: documentation only; no commands were run.
