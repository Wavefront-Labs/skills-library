---
id: computing-software.systems-network-administration.openldap.ldapdelete-and-ldapmodrdn
name: ldapdelete-and-ldapmodrdn
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, ldapdelete, ldapmodrdn, rename-entry, recursive-delete, delete-entry]
level: practitioner
status: docs-checked
description: "Delete and rename OpenLDAP entries from the command line: ldapdelete -r, -f, -c, -n and ldapmodrdn -r, -s new superior, -f input format."
sources:
  - https://www.openldap.org/software/man.cgi?query=ldapdelete&sektion=1&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/software/man.cgi?query=ldapmodrdn&sektion=1&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ldapdelete and ldapmodrdn
**ldapdelete**
```
ldapdelete -x -D "cn=admin,dc=example,dc=com" -W "cn=Delete Me,dc=example,dc=com"
ldapdelete -n -v -x -D "cn=admin,dc=example,dc=com" -W "cn=Delete Me,dc=example,dc=com"
ldapdelete -c -f dns.txt -H ldap://ldap.example.com -ZZ
```
- `-f file`: DNs one per line. `-c` continue on error. `-n` with `-v` dry run.
- `-r` recursive delete of the children and descendants of the DN, with no verification. `-z sizelimit` raises the limit for finding children when the server caps searches.
- `-M[M]` manageDSAit; `-e` controls (`assert`, `preread`, `postread`, `relax`, `noop`).

**ldapmodrdn**
- Command line: `ldapmodrdn [opts] dn rdn` replaces the RDN of `dn`.
- File or stdin: pairs of lines (a DN, then its new RDN), pairs separated by blank lines.
```
cn=Modify Me,dc=example,dc=com
cn=The New Me
```
`ldapmodrdn -r -f /path/to/entrymods` renames and removes the old `cn` value.
- `-r` remove old RDN values (default: keep them). `-s newsup` moves the entry under a new superior (not LDAPv2).

Both accept the usual auth flags: `-x -D -W -w -y -H -Z -Y -X`.

Gotchas: `-r` does no verification and can delete large portions of the tree; take a `slapcat` backup first. Both tools exit non-zero on error.

## Checked
2026-11-08: confirmed against the ldapdelete(1) and ldapmodrdn(1) man pages: every flag and extension named, input formats, the entrymods example, -r and -s semantics and exit status. Removed the unconfirmed write-access claim for the entry and children pseudo-attributes.
Method: documentation only; no commands were run.
