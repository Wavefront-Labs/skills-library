---
id: computing-software.systems-network-administration.openldap.ldappasswd-password-change
name: ldappasswd-password-change
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, ldappasswd, password-modify, set-password, extended-operation]
level: practitioner
status: docs-checked
description: "Change or reset an OpenLDAP password with ldappasswd using the Password Modify extended operation: old and new password flags, server-generated passwords, TLS."
sources:
  - https://www.openldap.org/software/man.cgi?query=ldappasswd&sektion=1&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ldappasswd password change
Target: the optional `user` argument (DN); if omitted, the bound user.

Flags:
- Bind: `-x -D binddn -W | -w pw | -y file`, `-H uri`.
- Old password: `-A` prompt, `-a oldPasswd`, `-t oldPasswdFile`.
- New password: `-S` prompt, `-s newPasswd`, `-T newPasswdFile`. If no new password is given and prompting is off, the server generates one.
- SASL: `-Y mech -U authcid -R realm -X authzid -O props -I -Q -N`.
- TLS: `-Z`, `-ZZ` to require StartTLS.
- Other: `-n` do nothing (test), `-v`, `-d`, `-e` controls (`ppolicy`, `assert`, ...), `-o`.

Examples:
```
ldappasswd -x -H ldap://ldap.example.com -D "cn=admin,dc=example,dc=com" -W -S "uid=jdoe,ou=people,dc=example,dc=com"
ldappasswd -ZZ -x -D "cn=admin,dc=example,dc=com" -y bindpw.txt -T newpw.txt "uid=jdoe,ou=people,dc=example,dc=com"
ldappasswd -Y DIGEST-MD5 -U jdoe -H ldap://ldap.example.com "uid=jdoe,ou=people,dc=example,dc=com"
```
Gotchas:
- Passwords on the command line (`-w`, `-s`, `-a`) are visible to other users; prefer prompts or files.
- `-e ppolicy` is one of the supported general extensions.
- Use TLS (`-Z`/`-ZZ`) for any simple bind.
- ldappasswd is not designed or intended to replace passwd(1).

Verify: `ldapwhoami -x -D "uid=jdoe,ou=people,dc=example,dc=com" -W`.

## Checked
2026-11-08: confirmed against the ldappasswd(1) man page: every flag and extension named, RFC 3062 Password Modify operation, server-generated password behaviour and the passwd(1) note. Removed the unconfirmed pwdSafeModify claim and the claim that ppolicy errors are shown.
Method: documentation only; no commands were run.
