---
id: computing-software.systems-network-administration.openldap.ldapmodify-and-ldapadd
name: ldapmodify-and-ldapadd
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, ldapmodify, ldapadd, change-records, ldif, modify]
level: practitioner
status: docs-checked
description: "Change directory entries with ldapmodify and ldapadd: LDIF change records, -a, -c, -f, -j, -S, -n, controls, and error handling for large loads."
sources:
  - https://www.openldap.org/software/man.cgi?query=ldapmodify&sektion=1&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/software/man.cgi?query=ldif&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ldapmodify and ldapadd
`ldapadd` is a hard link to `ldapmodify` that always sets `-a`.

Modify record:
```
dn: cn=Modify Me,dc=example,dc=com
changetype: modify
replace: mail
mail: modme@example.com
-
add: title
title: Grand Poobah
-
delete: description
```
Run: `ldapmodify -x -D "cn=Manager,dc=example,dc=com" -W -f /path/to/entrymods`.

Other records: `changetype: delete`; `changetype: modrdn` per ldif(5). ldapadd reads plain entry records with no `changetype`, as in the man page example. A `delete:`/`replace:` block with no values removes the attribute.

Options:
- `-a` add (default is modify); `-f file` (else stdin); `-n` with `-v` previews without changing.
- `-c` continue after errors; `-S file` writes skipped records with the server error as a comment; `-j lineno` resumes at a line after fixing errors.
- `-M[M]` manageDSAit; `-e` controls (`assert`, `preread`, `postread`, `relax`, `ppolicy`, `noop`, `sessiontracking`); `-E txn[=abort|commit]`.
- Connection/auth flags as for ldapsearch: `-x -D -W -H -Z -Y`.

Gotchas: binary values use `attr:< file:///path`; exit status is zero only on success.

## Checked

2026-11-09. Confirmed against ldapmodify(1) (hard link and -a, -n with -v, -c, -f, -j, -S, -M, -e and -E extension lists, txn, example records, exit status) and ldif(5) (modify blocks, empty replace or delete removes the attribute, modrdn, file URL values). Reworded the claim that records without changetype are adds, which the pages show only via the ldapadd example.

Method: documentation only; no commands were run.

