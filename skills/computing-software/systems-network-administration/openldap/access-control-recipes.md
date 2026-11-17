---
id: computing-software.systems-network-administration.openldap.access-control-recipes
name: access-control-recipes
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, acl-recipes, selfwrite, ssf-acl, group-membership, access-control]
level: advanced
status: docs-checked
description: "Reusable OpenLDAP ACL patterns: self-service writes, anonymous auth, SSF-gated reads and writes, group membership self-edit, rootdn IP limits, attrs by objectClass."
sources:
  - https://www.openldap.org/doc/admin26/access-control.html
  - https://www.openldap.org/software/man.cgi?query=slapd.access&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/software/man.cgi?query=slapacl&sektion=8&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# access control recipes
Patterns described in the Admin Guide:
- Basic: users write their own entries, anonymous may authenticate, everyone else reads. Only the first matching `by` applies.
- Strength gating: writes need SSF 128 or higher, reads SSF 64 or higher (`by ssf=128 ...`); otherwise the implicit `by * none` applies.
- Attribute exception first: put `homePhone` rule before the subtree rule that covers other attributes.
- Group self-edit: `access to attrs=member,entry by dnattr=member selfwrite`; the `entry` pseudo-attribute is needed because any attribute access requires access to the entry.
- Rootdn lock-down: create a real entry for the rootdn with a password and limit its `auth` by client IP (`peername.regex`).
- Proxy authorization: restrict `authzTo` with `self` plus IP and SSF conditions; others cannot see it.
- Groups: `by group.exact="cn=Administrators,dc=example,dc=com" write`; `group.expand` with a regex capture for dynamic group names; `group/<objectclass>/<attr>` for non-standard group schemas.
- Attribute lists: `attrs=mail` self write and users read; `attrs=children` self only controls add/delete; `@objectclass` targets the attributes required or allowed by a class; `!objectclass` targets those neither required nor allowed.
- Regex self-service: a user writes its own entry and subtree using expanded captures.

Pitfalls: prefer scope styles (`exact`, `one`, `children`, `subtree`) over regex unless you need captures; use `([^,]+)` to match exactly one RDN; `(.+)` requires at least one character.

Verify with `slapacl -b <dn> -D <user dn> <attr>/read`.

## Checked

2026-11-09. Confirmed against the OpenLDAP 2.6 Admin Guide chapter 8.2 and 8.4 (basic ACLs, SSF 128 and 64 example, homePhone ordering example, dnattr selfwrite, rootdn lock-down by peername.regex, authzTo with self, IP and ssf=256, group.exact and group.expand and group/objectclass/attribute forms, attrs lists, @ and ! objectClass prefixes, regex tips) and the slapacl(8) attr/access syntax. Fixed the group self-edit example to include `entry`, the group DN to match the guide, and the meaning of the `!` prefix.

Method: documentation only; no commands were run.

