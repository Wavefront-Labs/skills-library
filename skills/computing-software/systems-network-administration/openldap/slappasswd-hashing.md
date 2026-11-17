---
id: computing-software.systems-network-administration.openldap.slappasswd-hashing
name: slappasswd-hashing
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, slappasswd, ssha, password-hash, olcpasswordhash, rootpw]
level: intro
status: docs-checked
description: "Generate RFC 2307 password hashes for OpenLDAP rootpw and userPassword with slappasswd: schemes, -s, -T, -g, -c salt formats, and storage caveats."
sources:
  - https://www.openldap.org/software/man.cgi?query=slappasswd&sektion=8&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/doc/admin26/security.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# slappasswd hashing
```
slappasswd -h '{SSHA}' -s 'secret'
slappasswd -T /path/to/passfile -n
slappasswd -g
```
Use the output in `rootpw {SSHA}...` or `olcRootPW: {SSHA}...`.

Options:
- `-h scheme`: `{CRYPT}`, `{MD5}`, `{SMD5}`, `{SSHA}`, `{SHA}`, `{CLEARTEXT}`. Default `{SSHA}` (SHA-1 with a seed, described as the most secure supported).
- `-s secret` | `-T file` | `-g` (generate; scheme `{CLEARTEXT}`): mutually exclusive. With none, you are prompted.
- `-c format`: salt for `{CRYPT}`, one `%s`; default 31 salt characters; `'%.2s'` two characters; `'$1$%.8s'` MD5 with 8 salt characters on some systems.
- `-n` omit trailing newline; `-u` RFC 2307 output (default); `-v` verbose.
- `-o module-path=... -o module-load="..."` load a dynamic hash module.
- Server default for stored passwords: `olcPasswordHash` `{SSHA}`, settable only in the frontend entry.

Gotchas:
- Quote braces so the shell does not expand `{SSHA}`.
- `crypt(3)` behaviour is platform specific.
- Hashes in userPassword deviate from RFC 4519 and prevent DIGEST-MD5; treat hashes like cleartext passwords.
- Hashing does not protect passwords in transit: use TLS.

## Checked

2026-11-04. Confirmed against slappasswd(8), slapd-config(5) olcPasswordHash (default {SSHA}, frontend entry only) and the Administrator's Guide Security chapter: options -v -u -s -g -T -h -c -n -o, mutual exclusion of -s/-g/-T, -g implying {CLEARTEXT}, scheme list, brace quoting, -c format with one %s and default 31 salt characters, module-path and module-load, crypt(3) platform behaviour, RFC 4519 deviation, DIGEST-MD5 incompatibility, SSHA described as most secure, TLS for transit.

Method: documentation only; no commands were run.
