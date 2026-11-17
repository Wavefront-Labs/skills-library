---
id: computing-software.systems-network-administration.openldap.authz-regexp-mapping
name: authz-regexp-mapping
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, authz-regexp, identity-mapping, olcsaslrealm, olcauthzregexp, sasl]
level: advanced
status: docs-checked
description: "Map SASL authentication identities to directory DNs in OpenLDAP with authz-regexp: direct and search-based replacement, multi-realm ordering and ACL needs."
sources:
  - https://www.openldap.org/doc/admin26/sasl.html
  - https://www.openldap.org/software/man.cgi?query=slapd-config&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/software/man.cgi?query=slapacl&sektion=8&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/software/man.cgi?query=ldapwhoami&sektion=1&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# authz-regexp identity mapping
Syntax (slapd.conf; `olcAuthzRegexp` in cn=config): `authz-regexp <search pattern> <replacement pattern>`. Only the first matching directive applies; `$1`, `$2` refer to parenthesized matches.

Direct mapping to a DN:
```
authz-regexp
  uid=([^,]*),cn=example.com,cn=gssapi,cn=auth
  uid=$1,ou=people,dc=example,dc=com
```
Search-based mapping (must return exactly one entry):
```
authz-regexp
  uid=([^,]*),cn=example.com,cn=gssapi,cn=auth
  ldap:///ou=people,dc=example,dc=com??one?(uid=$1)
```
Multi-realm: list explicit realms before a default realm so the specific rule matches first:
```
authz-regexp
   uid=([^,]*),cn=engineering.example.com,cn=digest-md5,cn=auth
   ldap:///dc=eng,dc=example,dc=com??one?(&(uid=$1)(objectClass=person))
```
Gotchas:
- The mapping search is subject to ACLs; the authentication identity needs `auth` access on what it searches.
- Order matters, because the first match wins.
- Test the mapping with `ldapwhoami -Y <mech>`, which returns the resulting `dn:`, and with `slapacl -U <authcid>`.

## Checked

2026-11-09. Confirmed against the OpenLDAP 2.6 Admin Guide SASL chapter (authz-regexp, direct and search-based replacement, first match wins, multi-realm ordering), the slapd-config(5) olcAuthzRegexp entry, slapacl(8) (-U maps an ID through authz-regexp) and ldapwhoami(1).

Method: documentation only; no commands were run.

