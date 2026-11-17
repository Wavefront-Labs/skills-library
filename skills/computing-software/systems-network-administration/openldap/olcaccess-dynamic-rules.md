---
id: computing-software.systems-network-administration.openldap.olcaccess-dynamic-rules
name: olcaccess-dynamic-rules
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, olcaccess, rule-index, ldapmodify-acl, cn-config, access-control]
level: practitioner
status: docs-checked
description: "Manage OpenLDAP ACLs online with olcAccess in cn=config: the {N} rule index, replacing one rule safely with ldapmodify, and ordering."
sources:
  - https://www.openldap.org/doc/admin26/access-control.html
  - https://www.openldap.org/doc/admin26/slapdconf2.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# olcAccess dynamic rules
In cn=config the same grammar is stored as `olcAccess` values on a database (or on `olcDatabase=frontend` for global rules). Each value gets a `{N}` index that slapd maintains; the index fixes evaluation order.

Replace one rule by index rather than by content:
```
dn: olcDatabase={1}mdb,cn=config
changetype: modify
delete: olcAccess
olcAccess: {1}
-
add: olcAccess
olcAccess: {1}to attrs=userPassword by self write by anonymous auth by * none
-
```
Apply the LDIF with `ldapmodify`. The guide shows this delete-by-index then add-at-index pattern.

Rules:
- Use the `{N}` index in the new value (as above) rather than deleting and re-adding by content.
- Per-database rules are evaluated before the frontend (global) rules.
- With no rules the default is read for all.

Read the values back with `slapcat` or `ldapsearch` to see the `{N}` tags that slapd adds automatically.

Verify the result with `slapacl` before relying on it. The rootdn always has full rights, so keep a usable rootdn for recovery.

## Checked

2026-11-09. Confirmed against the OpenLDAP 2.6 Admin Guide 8.3 (olcAccess grammar, 8.3.6 ordering with `{X}` indexes and the delete/add by index example, frontend rules appended to per-database rules, default read) and slapd-config chapter 5.2.5 (frontend database, olcAccess default). Replaced the unsourced `replace: olcAccess` example with the guide's delete/add pattern and removed the unsourced ldapi/EXTERNAL commands.

Method: documentation only; no commands were run.

