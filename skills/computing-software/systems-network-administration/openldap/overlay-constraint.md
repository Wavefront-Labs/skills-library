---
id: computing-software.systems-network-administration.openldap.overlay-constraint
name: overlay-constraint
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, constraint, constraint-attribute, regex-constraint, overlay, olcconstraintattribute]
level: practitioner
status: docs-checked
description: "Restrict attribute values on add and modify in OpenLDAP with the constraint overlay: regex, negregex, size, count, uri and set constraints, restrict scope."
sources:
  - https://www.openldap.org/software/man.cgi?query=slapo-constraint&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/doc/admin26/overlays.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# constraint overlay
Syntax after `overlay constraint`:
`constraint_attribute <attr>[,...] <type> <value> [<extra>]`

Types: `regex`, `negregex`, `size` (attribute length), `count` (number of values), `uri` (LDAP URI without host, evaluated by an internal search; list attributes), `set` (ACL set syntax). Extra: `restrict=<uri>` limits the constraint to entries matching the URI's base, scope (default base) and filter.

Examples:
```
overlay constraint
constraint_attribute jpegPhoto size 131072
constraint_attribute userPassword count 3
constraint_attribute mail regex ^[[:alnum:]]+@mydomain.com$
constraint_attribute mail negregex ^[[:alnum:]]+@notallowed.com$
constraint_attribute title uri ldap:///dc=catalog,dc=example,dc=com?title?sub?(objectClass=titleCatalog)
constraint_attribute cn,sn,givenName set "(this/givenName + [ ] + this/sn) & this/cn" restrict="ldap:///ou=People,dc=example,dc=com??sub?(objectClass=inetOrgPerson)"
```
cn=config: `olcConstraintAttribute` with objectClasses `olcOverlayConfig` and `olcConstraintConfig`.

Gotchas:
- Applies only to add, modify and rename, and to added or replaced values.
- Several constraints on one attribute must all pass; failures return LDAP_CONSTRAINT_VIOLATION.
- The relax control disables constraints.
- Keep a `uri` catalog in a separate database so it can be populated while the constraint is active.
- The page does not state units for `size`; test before relying on a value.

## Checked

2026-11-04. Confirmed against slapo-constraint(5) and the Administrator's Guide overlays chapter: constraint_attribute syntax, six types, uri without hostname, set with ACL set syntax, restrict= semantics, all constraints must pass, add/modify/rename only, relax control exemption, LDAP_CONSTRAINT_VIOLATION, the six examples including the separate-database catalog note, olcConstraintAttribute with olcConstraintConfig.

Method: documentation only; no commands were run.
