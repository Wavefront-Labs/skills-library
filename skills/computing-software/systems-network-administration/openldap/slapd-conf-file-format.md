---
id: computing-software.systems-network-administration.openldap.slapd-conf-file-format
name: slapd-conf-file-format
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, slapd-conf, include, deprecated-config, backend, database]
level: intro
status: docs-checked
description: "Write a valid OpenLDAP slapd.conf: section order, comments and continuation, quoting, include, schema files, and a two-database example."
sources:
  - https://www.openldap.org/doc/admin26/slapdconfig.html
  - https://www.openldap.org/software/man.cgi?query=slaptest&sektion=8&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# slapd.conf file format
Deprecated in favour of cn=config; use it only for backends slapd-config does not support.

- Default location: `/usr/local/etc/openldap`, overridden by `slapd -f`.
- Order: global directives, then `backend` declarations, then `database` declarations. Database settings override backend settings, which override global ones.
- `#` starts a comment; a line beginning with whitespace continues the previous line.
- Quote arguments containing whitespace with double quotes; escape `"` and backslash with a backslash.
- `include <file>` reads another file in place (commonly schema). There is no small limit on nested includes and no loop detection.

Example:
```
include /usr/local/etc/schema/core.schema
referral ldap://root.openldap.org
access to * by * read

database mdb
suffix "dc=example,dc=com"
directory /usr/local/var/openldap-data
rootdn "cn=Manager,dc=example,dc=com"
rootpw secret
index uid pres,eq
index objectClass eq
```
Backend types: asyncmeta, config, dnssrv, ldap, ldif, mdb, meta, monitor, null, passwd, perl, relay, sock, sql, wt.

Gotcha: a global `access` rule is applied after database-specific ones. Check the file with `slaptest -f slapd.conf -v`.

## Checked

2026-11-09. Confirmed against the OpenLDAP 2.6 Admin Guide chapter 6 (deprecation note, default location, global then backend then database order and override rules, comments and continuation, quoting, include and its nesting warning, backend table of 15 types, example file, global access applied after database rules) and slaptest(8) (-f and -v example). Fixed the example index lines to the guide's form and removed the unsourced schema directory line.

Method: documentation only; no commands were run.

