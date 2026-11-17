---
id: computing-software.systems-network-administration.openldap.test-acls-with-slapacl
name: test-acls-with-slapacl
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, slapacl, acl-testing, dry-run, access-control, authz]
level: practitioner
status: docs-checked
description: "Check what an identity may do under the current OpenLDAP ACLs using slapacl: -b, -D, -U, -X, attr/access:value arguments, -u dry run, and -o connection options."
sources:
  - https://www.openldap.org/software/man.cgi?query=slapacl&sektion=8&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# test ACLs with slapacl
Syntax:
```
slapacl -b DN [-d level] [-D authcDN | -U authcID] [-f slapd.conf] [-F confdir]
        [-o option[=value]] [-u] [-v] [-X authzID | -o authzDN=DN]
        [attr[/access][:value] ...]
```
Example:
```
slapacl -F /usr/local/etc/openldap/slapd.d -v -D "uid=bjorn,ou=People,dc=example,dc=com" \
    -b "uid=babs,ou=People,dc=example,dc=com" "mail/read" "userPassword/write"
```
- `-b` entry must exist (it is fetched) and lie in a configured naming context.
- `-D` uses a DN; `-U` uses an ID mapped by `authz-regexp`; `-X` supplies an authorization ID. `-D`/`-U` and `-X`/`-o authzDN` are mutually exclusive pairs.
- No attribute arguments means the `entry` pseudo-attribute is tested.
- `-o` options: `peername`, `sockname`, `sockurl`, `domain`, `ssf`, `tls_ssf`, `sasl_ssf`, `transport_ssf`, `authzDN`, plus syslog options. Use them to simulate connection-based ACLs.
- `-u` dry-run uses a fake empty entry, so rules depending on entry contents or other objects will not behave as in reality.

Gotchas: with both `-f` and `-F`, the file is converted into the directory; with neither, the default config directory wins if valid. Run it against the same config slapd uses.

## Checked
2026-11-08: confirmed against the slapacl(8) man page: synopsis, every option, the -o option names, entry pseudo-attribute default, dry-run behaviour and the -f/-F rules.
Method: documentation only; no commands were run.
