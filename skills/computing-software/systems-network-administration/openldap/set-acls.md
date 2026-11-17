---
id: computing-software.systems-network-administration.openldap.set-acls
name: set-acls
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, set-acl, nested-groups, this-manager, experimental, access-control]
level: sme
status: docs-checked
description: "Use experimental OpenLDAP set ACLs to grant access through nested groups, posix memberUid groups and manager/secretary relationships."
sources:
  - https://www.openldap.org/doc/admin26/access-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# set ACLs
Set expressions are experimental and use `by set="<expr>" <access>`.

Syntax pieces:
- `attr*` recurses through nested groups (`member*`).
- `&` intersects with the requester: `user` (their DN) or `user/uid` (their uid attribute).
- `this` is the entry being accessed, so `this/manager` follows its manager reference and `this/manager/secretary` chains.

Typical uses:
- Nested groups: members of subgroups are included via `member*`.
- POSIX groups: match `memberUid` against the user's `uid` with `user/uid`.
- Manager and secretary: grant a manager's secretary access to the subordinate's entry, optionally with an extra nested-group check restricting it to executives.

Sketch (pattern, not copied verbatim):
```
access to dn.children="ou=People,dc=example,dc=com"
    by set="this/manager & user" write
    by * read
```

Gotchas:
- The feature is experimental; test behaviour with `slapacl` before relying on it.
- ACLs are never evaluated for the rootdn.

## Checked

2026-11-09. Confirmed against the OpenLDAP 2.6 Admin Guide chapter 8.5 (sets are experimental; `member*` recursion with `& user`; `memberUid & user/uid`; `this/manager & user`; `this/manager/secretary`; executive-group restriction) and the slapacl and rootdn notes in chapter 8. Removed the unsupported remark that set walks cost extra lookups.

Method: documentation only; no commands were run.

