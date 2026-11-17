---
id: computing-software.systems-network-administration.openldap.backends-overview
name: backends-overview
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, backends, ldif-backend, null-backend, relay, passwd, sql]
level: intro
status: docs-checked
description: "Pick an OpenLDAP slapd backend: mdb, ldap, ldif, meta, null, passwd, relay and sql, with their purpose, minimal config and caveats."
sources:
  - https://www.openldap.org/doc/admin26/backends.html
  - https://www.openldap.org/software/man.cgi?query=slapd-ldif&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# backends overview
- **mdb**: the recommended primary store (LMDB). Hierarchical, indexed, no tuning cache; `maxsize` is mandatory.
- **ldap**: proxies to another LDAP server and chases referrals; used internally by other backends and overlays.
- **ldif**: entries as LDIF files in a filesystem tree. "Cheap, low performance, easy to use"; also stores persistent `cn=config`. Config:
```
database  ldif
directory ./ldif
suffix    "dc=example,dc=com"
```
The directory must exist with rwx for slapd's identity. ACL semantics are not honoured; only read access is enforced by the frontend.
- **meta**: proxies several remote servers into one DIT; the guide gives no config and warns about overhead.
- **null**: discards everything; searches succeed empty, compares return compareFalse. Add `bind on` to allow binds as any DN in the suffix with any password.
```
database null
suffix "cn=Nothing"
bind on
```
- **passwd**: serves `/etc/passwd` as `uid=<name>,<suffix>`; demonstration only.
- **relay**: maps a naming context of another database in the same slapd; needs the rwm overlay; experimental.
- **sql**: RDBMS via ODBC; experimental and deprecated.

Choose mdb unless you need a proxy (ldap, meta, relay) or a test double (null).

## Checked

2026-11-09. Confirmed against the OpenLDAP 2.6 Admin Guide chapter 11 (mdb recommended, indexing, no cache, mandatory maxsize; ldap proxy and referral chasing; ldif purpose and cn=config storage; meta overhead warning and no config; null behaviour and `bind on`; passwd demonstration only; relay needs rwm and is experimental; sql ODBC, experimental and deprecated) and slapd-ldif(5) (directory rwx, ACL semantics not honoured, only read enforced by the frontend).

Method: documentation only; no commands were run.

