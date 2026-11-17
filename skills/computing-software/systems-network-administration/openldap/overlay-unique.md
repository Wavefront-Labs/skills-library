---
id: computing-software.systems-network-administration.openldap.overlay-unique
name: overlay-unique
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, unique, unique-uri, uniqueness, overlay, olcuniqueuri]
level: practitioner
status: docs-checked
description: "Enforce attribute uniqueness in OpenLDAP with the unique overlay: unique_uri syntax, strict, ignore and serialize keywords, scope rules and replication bypass."
sources:
  - https://www.openldap.org/software/man.cgi?query=slapo-unique&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/doc/admin26/overlays.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# unique overlay
```
overlay unique
unique_uri ldap:///?mail?sub?
```
cn=config attribute: `olcUniqueURI`. Each value is an independent uniqueness domain.

URI form: `[strict] [ignore] [serialize] ldap:///[base dn]?[attributes...]?scope[?filter]`
- Base DN defaults to the database DN and must be inside it.
- Empty attribute list means all non-operational attributes.
- Scope is effectively required: `sub` or `one` (`base` is invalid; no scope defaults to base).
- Filter limits enforcement, e.g. `ldap:///?cn?sub?(sn=e*)`.

Keywords:
- `strict`: treat null values as values (only one object may have none).
- `ignore`: enforce on every non-operational attribute except those listed, e.g. `ignore ldap:///?objectClass,dc,ou,o?sub`.
- `serialize`: make writes complete one at a time so concurrent changes cannot slip by.

Gotchas:
- The database must have a `rootdn` (the overlay searches with it to avoid ACL interference).
- Legacy `unique_base`, `unique_attributes`, `unique_ignore`, `unique_strict` cannot be mixed with `unique_uri`.

## Checked

2026-11-04. Confirmed against slapo-unique(5) and the Administrator's Guide overlays chapter: unique_uri syntax and domains, olcUniqueURI, keyword quoting, URI form and defaults, scope effectively mandatory, filter example, ignore, strict null handling, serialize, rootdn requirement, legacy parameters not mixable with unique_uri. Removed the slapadd, replication, relax and error-code remarks, which the pages do not state.

Method: documentation only; no commands were run.
