---
id: computing-software.systems-network-administration.openldap.proxy-authorization
name: proxy-authorization
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, authzto, authzfrom, authz-policy, proxy-authorization, olcauthzpolicy]
level: advanced
status: docs-checked
description: "Let one OpenLDAP identity act as another: authz-policy values, authzTo source rules, authzFrom destination rules, DN, regex and URL forms, and -X on clients."
sources:
  - https://www.openldap.org/doc/admin26/sasl.html
  - https://www.openldap.org/software/man.cgi?query=slapd-config&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/software/man.cgi?query=slapd-ldap&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/software/man.cgi?query=ldapwhoami&sektion=1&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# proxy authorization
Disabled by default. Server option `authz-policy` (`olcAuthzPolicy`): `none` (default), `to`, `from`, `any`, `all` (cn=config reference lists `none, from, to, any, all`).

Rules:
- `authzTo`: source rule, stored in the authenticating entry.
- `authzFrom`: destination rule, stored in the target entry.
- Values: a DN, `dn.regex:<regex>`, or an LDAP URL. Checks run source first, then destination; default is deny.
- The attribute needs `auth` privilege; restrict who can write `authzTo`, since writers can grant themselves any identity.

Examples:
```
dn: cn=WebUpdate,dc=example,dc=com
authzTo: ldap:///dc=example,dc=com??sub?(objectclass=person)

authzTo: dn.regex:^uid=[^,]*,dc=example,dc=com$
```
Client side: `-X u:<username>` or `-X dn:<dn>`. Check the effective identity with:
`ldapwhoami -Y DIGEST-MD5 -U web -X u:babs`

Gotchas:
- The `ldap` backend's `idassert-bind` also needs the remote server to set `authz-policy` to `to` or `both`.
- Proxying relies on proper ACLs on `authzTo`; see the access-control recipes.

## Checked

2026-11-09. Confirmed against the OpenLDAP 2.6 Admin Guide SASL chapter (authorization identities, proxy authorization rules, authzTo and authzFrom forms and evaluation), the slapd-config(5) olcAuthzPolicy entry, slapd-ldap(5) idassert-bind and ldapwhoami(1) (-U, -X with dn: or u: forms, -Y).

Method: documentation only; no commands were run.

