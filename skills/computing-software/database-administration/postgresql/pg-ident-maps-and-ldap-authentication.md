---
id: computing-software.database-administration.postgresql.pg-ident-maps-and-ldap-authentication
name: pg-ident-maps-and-ldap-authentication
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, client-authentication, pg-ident-conf, ldap-authentication, ldap, active-directory, peer-authentication, user-name-maps, gssapi]
level: advanced
status: docs-checked
description: "Use pg_ident.conf user name maps with peer/cert/GSSAPI auth, and configure LDAP (simple bind or search+bind) authentication against Active Directory."
sources:
  - https://www.postgresql.org/docs/18/auth-username-maps.html
  - https://www.postgresql.org/docs/18/auth-ldap.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# User name maps and LDAP authentication

**Goal:** OS or directory identities log in as the right database role without
duplicating passwords in PostgreSQL.

## pg_ident.conf maps
Maps translate the external name (OS user, cert CN, Kerberos principal) to a role.
```
# MAPNAME  SYSTEM-USERNAME        PG-USERNAME
admins     alice                  postgres
admins     bob                    postgres
krb        /^(.*)@EXAMPLE\.COM$   \1
```
pg_hba.conf:
```
local  all  postgres         peer map=admins
host   all  all  10.0.0.0/8  gss  include_realm=1 map=krb
```
Reload after editing. A map line allows; it does not force: the client still
asks for a specific role, and the map must contain that pair.

## LDAP
PostgreSQL only checks the password against LDAP; the role must already exist
in PostgreSQL before LDAP can be used. Two modes exist: simple bind (the DN is `ldapprefix` + user name + `ldapsuffix`) and search+bind (bind with a fixed account, search under `ldapbasedn`, then re-bind as the found user; it costs two extra LDAP requests).

Search+bind (works with AD where DNs are not predictable):
```
hostssl all all 10.0.0.0/8 ldap ldapurl="ldaps://dc1.example.com/dc=example,dc=com?sAMAccountName?sub" ldapbinddn="CN=pgsvc,OU=Svc,DC=example,DC=com" ldapbindpasswd="<secret>"
```
Simple bind (DN built from prefix/suffix):
```
hostssl all all 10.0.0.0/8 ldap ldapserver=dc1.example.com ldapscheme=ldaps ldapprefix="EXAMPLE\" ldapsuffix=""
```
Restrict to a group with `ldapsearchfilter="(&(sAMAccountName=$username)(memberOf=CN=DBUsers,OU=Groups,DC=example,DC=com))"`.

## Gotchas
- `ldapscheme=ldaps` or `ldaptls=1` encrypts only the PostgreSQL-to-LDAP leg; the client
  connection stays unencrypted unless SSL is used there too, so use `hostssl` for
  the client side as well.
- `ldapurl` is supported only with OpenLDAP, not on Windows.
- `ldapbindpasswd` sits in pg_hba.conf in plaintext: lock file permissions and
  use a least-privileged service account.
- LDAP down = nobody logs in. Keep a local superuser path (peer) for break-glass.
- Kerberos/GSSAPI is better than LDAP when available: no password reaches the DB.

## Verify
- `SELECT * FROM pg_ident_file_mappings;` and
  `SELECT * FROM pg_hba_file_rules WHERE error IS NOT NULL;` show no errors.
- A directory user logs in; a disabled directory account is rejected; the server
  log records the failure.

## Checked
2026-10-25. Against PostgreSQL 18 documentation (REL_18_STABLE doc/src/sgml, branch head 2026-10-24; PostgreSQL 19 is still at release-candidate stage): User Name Maps section (`map` supported for all methods that receive external names, `pg_ident.conf` line forms and regular-expression system names, file re-read on reload, `pg_ident_file_mappings` view for pre-testing) and LDAP Authentication section (simple bind versus search+bind, `ldapprefix`/`ldapsuffix`, `ldapbinddn`/`ldapbindpasswd`, `ldapsearchfilter` with `$username`, `ldapurl` format and its OpenLDAP-only restriction, `ldapscheme`/`ldaptls` encrypting only the server-to-LDAP leg), and `pg_hba_file_rules`. Removed the PG15 version gate, the third-party sync tool mention and the quoted log text, which the documentation does not give.
Method: documentation only; no commands were run.
