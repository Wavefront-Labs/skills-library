---
id: computing-software.systems-network-administration.openldap.per-database-limits
name: per-database-limits
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, olclimits, paged-results, size-unchecked, limits, group-limits]
level: advanced
status: docs-checked
description: "Give specific OpenLDAP users or groups different search limits with the limits / olcLimits directive: selectors, time and size forms, paged results, glued databases."
sources:
  - https://www.openldap.org/doc/admin26/limits.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# per-database limits
Directive: `limits <selector> <limit> [<limit> ...]` in slapd.conf, or `olcLimits` in cn=config. The clause can repeat; clauses are checked in order and the first match on the initiator or base DN wins. With no match, the global limits apply.

Selectors:
- `*` everyone, `anonymous`, `users`.
- `dn[.type][.style]=pattern`: type `self` or `this`; styles exact, base, onelevel, subtree, children, regex, anonymous.
- `group[/oc[/at]]=pattern`: group members. Granting to a group is preferred over naming individuals.

Limits: `time[.soft|hard]=<n>` and `size[.soft|hard]=<n>`; without a qualifier both are set. `unlimited` removes a limit. The global specials also work: `size.unchecked`, `size.pr`, `size.prtotal`.

Examples (from the guide):
```
limits group/groupOfNames/member="cn=dirsync,dc=example,dc=org" size.prtotal=unlimited
limits users size.soft=5 size.hard=100 size.prtotal=disabled
limits anonymous size.soft=2 size.hard=5 size.prtotal=disabled
limits dn.exact="cn=anyuser,dc=example,dc=org" size=100000
```
Gotcha: for a glued (subordinate) database layout, limits meant to span parent and subordinates must be defined in both; the subordinate's own settings are otherwise not honoured.

Verify by binding as each identity and running a search; `ldapsearch -E pr=<size>[/prompt|noprompt]` exercises the paged-results limits.

## Checked

2026-11-04. Confirmed against the OpenLDAP 2.6 Administrator's Guide Limits chapter (9.4 per-database limits, selector table, time and size forms, unlimited, examples 9.5.3 and 9.5.4, glued database note 9.6) and the ldapsearch(1) pr= extension syntax. Replaced example DNs with the guide's own forms (the group example previously omitted the group/groupOfNames/member form).

Method: documentation only; no commands were run.
