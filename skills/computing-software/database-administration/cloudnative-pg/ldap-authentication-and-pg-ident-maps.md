---
id: computing-software.database-administration.cloudnative-pg.ldap-authentication-and-pg-ident-maps
name: ldap-authentication-and-pg-ident-maps
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [ldap, pg-ident, user-name-maps, search-bind, simple-bind, authentication]
level: advanced
status: docs-checked
description: "Configure LDAP simple bind or search+bind in the Cluster spec, and add pg_ident user name maps, including the fixed local mapping and the insecure-fallback warning."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/postgresql_conf.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**LDAP.** An optional `ldap` stanza under `postgresql` is converted into a `pg_hba.conf` rule placed after your own rules. Two modes:

- *simple bind*: specify `server`, `prefix` and `suffix`.
- *search+bind*: specify `server`, `baseDN`, `bindDN` and `bindPassword` (a reference to a Secret), plus optionally `searchFilter` or `searchAttribute` (default `uid`).

Both modes accept an optional `scheme` (`ldapscheme`) and `port`.

```yaml
postgresql:
  ldap:
    server: 'openldap.default.svc.cluster.local'
    bindSearchAuth:
      baseDN: 'ou=org,dc=example,dc=com'
      bindDN: 'cn=admin,dc=example,dc=com'
      bindPassword:
        name: 'ldapBindPassword'
        key: 'data'
      searchAttribute: 'uid'
```

**pg_ident.** `.spec.postgresql.pg_ident` takes user-name map lines, written after one fixed rule, `local <postgres system user> postgres`, which the instance manager generates by detecting the user running PostgreSQL. If that user is not configured properly in the container, the instance manager allows any local user to connect and logs `Unable to identify the current user. Falling back to insecure mapping.`

```yaml
  postgresql:
    pg_ident:
      - "mymap /^(.*)@mydomain\\.com$ \\1"
```

## Checked

2026-11-04. Trimmed claims the page does not state. LDAP modes, search+bind example, pg_ident fixed rule and fallback warning confirmed on the PostgreSQL Configuration page.

Method: documentation only; no commands were run.
