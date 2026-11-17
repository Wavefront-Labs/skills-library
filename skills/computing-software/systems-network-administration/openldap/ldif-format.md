---
id: computing-software.systems-network-administration.openldap.ldif-format
name: ldif-format
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, ldif, base64, line-folding, change-records, include]
level: intro
status: docs-checked
description: "Write correct LDIF for OpenLDAP tools: entry records, base64 and URL values, line folding, comments, change records for modify, modrdn and delete, and include."
sources:
  - https://www.openldap.org/software/man.cgi?query=ldif&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/software/man.cgi?query=slapcat&sektion=8&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LDIF format
Spec: RFC 2849. Records are separated by blank lines.

Entry record:
```
dn: uid=babs,ou=People,dc=example,dc=com
objectClass: inetOrgPerson
cn: Barbara J Jensen
cn: Babs Jensen
sn: Jensen
jpegPhoto:< file:///path/to/babs.jpg
```
- `attr: value` plain UTF-8; `attr:: base64` for values with non-printing characters or that begin with a space or `:`; `attr:< URL` loads from a URL such as `file:///path`.
- A line continues when the next begins with a single space or tab.
- `#` comments; repeat the attribute for multi-valued data.

Change records start with `dn:` then `changetype:`:
- `modify`: blocks `add:`, `replace:` or `delete:` + attr, value lines, ending with a `-` line.
- `add`: attributes follow directly.
- `delete`: nothing more.
- `modrdn` (or `moddn`):
```
dn: cn=Modify Me,dc=example,dc=com
changetype: modrdn
newrdn: cn=The New Me
deleteoldrdn: 1
newsuperior: ou=People,dc=example,dc=com
```
`deleteoldrdn: 1` removes the old RDN values; `0` keeps them.

Extension (not RFC 2849): `include: file:///path/to/file.ldif`, preceded by a blank line, supported by ldapadd, ldapmodify and slapadd.

Gotchas: slapcat writes entries in database order, not superior first, so reorder the records before loading them elsewhere.

## Checked

2026-11-09. Confirmed against ldif(5) (entry and change records, base64 and file URL values, line continuation, comments, include statement and its tool support, deleteoldrdn and newsuperior) and slapcat(8) (database order, not superior first). Removed the unsupported `<` base64 trigger, the trailing-space claim and the dbtools source, which was not read.

Method: documentation only; no commands were run.

