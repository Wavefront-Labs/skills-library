---
id: computing-software.systems-network-administration.openldap.access-control-evaluation-order
name: access-control-evaluation-order
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, evaluation-order, break, control-keywords, stop, continue, access-control]
level: advanced
status: docs-checked
description: "Predict how OpenLDAP evaluates ACLs: first matching to-rule, first matching by-clause, implicit by * none, and the stop, continue and break controls."
sources:
  - https://www.openldap.org/doc/admin26/access-control.html
  - https://www.openldap.org/software/man.cgi?query=slapd.access&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# access control evaluation order
1. Select the `to` rule: rules are checked in order and the first matching `<what>` wins. Per-database rules come before global rules.
2. Select the `by` clause: within that rule, the first matching `<who>` wins.
3. Compare: if the granted level is at least the requested one, access is allowed.
4. A non-empty rule list ends with an implicit `by * none`. If no rule applies to a backend, default read applies.

Place specific `to` rules and specific `by` clauses first. Example: a `dn.children="dc=example,dc=com"` rule with `search` must precede a `dn.children="dc=com"` rule with `read`, or the second is never reached.

Control keywords (last token of a `by` clause):
- `stop` (default): end evaluation on a match.
- `continue`: keep checking later `by` clauses in the same rule.
- `break`: fall through to later `access` rules matching the same target.

Each who-list implicitly ends with `by * none stop`. To stop evaluation only when both what and who matched, add an explicit trailing `by * break`. Examples:
```
access to dn.subtree="dc=example,dc=com" attrs=cn by * =cs break
access to dn.subtree="ou=People,dc=example,dc=com" by * +r
```
Gotcha: the rootdn is never evaluated, so naming it in a `by` clause only costs performance.

## Checked

2026-11-09. Confirmed against the OpenLDAP 2.6 Admin Guide chapter 8 (access control evaluation, implicit `by * none`, default read, ordering example) and slapd.access(5) (stop, continue and break controls, implicit `by * none stop`, the `by * break` text and the two break examples, rootdn bypass). Reworded the `by * break` sentence to follow the man page.

Method: documentation only; no commands were run.

