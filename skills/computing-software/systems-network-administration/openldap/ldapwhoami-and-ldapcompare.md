---
id: computing-software.systems-network-administration.openldap.ldapwhoami-and-ldapcompare
name: ldapwhoami-and-ldapcompare
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, ldapwhoami, ldapcompare, whoami, compare, authorization-identity]
level: intro
status: docs-checked
description: "Check the effective identity with ldapwhoami and test attribute assertions with ldapcompare, including TRUE/FALSE/UNDEFINED results, base64 values and -z quiet mode."
sources:
  - https://www.openldap.org/software/man.cgi?query=ldapwhoami&sektion=1&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/software/man.cgi?query=ldapcompare&sektion=1&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ldapwhoami and ldapcompare
**ldapwhoami** performs a bind and the Who Am I operation.
```
ldapwhoami -x -D "cn=Manager,dc=example,dc=com" -W
ldapwhoami -Y EXTERNAL -H ldapi:///
ldapwhoami -Y DIGEST-MD5 -U web -X u:babs -H ldap://host
```
It shows the authorization identity the server assigned, so use it to test `authz-regexp` mapping, SASL EXTERNAL and proxy authorization (`-X dn:<dn>` or `-X u:<user>`). Common flags: `-x -D -W -w -y -H -Z -ZZ -Y -U -R -O -I -Q -N`, `-n` and `-v`.

**ldapcompare** syntax: `ldapcompare [options] DN attr:value` or `DN attr::b64value`.
```
ldapcompare "uid=babs,dc=example,dc=com" sn:Jensen
ldapcompare "uid=babs,dc=example,dc=com" sn::SmVuc2Vu
```
(The two commands are equivalent.)
- Prints `TRUE`, `FALSE` or `UNDEFINED` unless `-z` (quiet); the exit code is the LDAP result code of the compare.
- Compare extension: `-E dontUseCopy`; `-M[M]` manageDSAit; the usual auth flags.

Gotchas: the value must be passed on the command line, which the man page lists as a limitation with security concerns.

## Checked
2026-11-08: confirmed against the ldapwhoami(1) and ldapcompare(1) man pages: every option and extension named, the TRUE/FALSE/UNDEFINED output, the exit code, -z, base64 form and the equivalent-examples note. Removed the unconfirmed claim about compare access and testing without read access.
Method: documentation only; no commands were run.
