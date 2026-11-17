---
id: computing-software.cybersecurity-defensive.dex.dex-ldap-nested-groups-recursion
name: dex-ldap-nested-groups-recursion
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [ldap, nested-groups, recursion, groupsearch]
level: advanced
status: docs-checked
description: "Resolve nested LDAP group membership in Dex with groupSearch.recursionGroupAttr, which also has cycle detection."
sources:
  - https://dexidp.io/docs/connectors/ldap/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Some LDAP schemas allow groups to contain other groups. Dex resolves these indirect memberships with `recursionGroupAttr`.

```yaml
groupSearch:
  baseDN: cn=groups,dc=freeipa,dc=example,dc=com
  filter: "(objectClass=group)"
  userMatchers:
  - userAttr: uid
    groupAttr: member
    recursionGroupAttr: member
  nameAttr: name
```

Example: John is a member of `seniorAdmins`, and `seniorAdmins` is a member of `admins`. With recursion enabled John is treated as a member of both.

How it works:

- Dex first finds groups where `member` matches the user's `uid`.
- Groups can list other groups in the same `member` attribute.
- With `recursionGroupAttr` set (in the `userMatchers` entry), Dex recursively searches for parent groups that contain the matched groups, following that attribute.
- If `recursionGroupAttr` is not set, only a single level of lookup is done.
- Built-in cycle detection prevents infinite loops when group references form a cycle.

Gotcha: `recursionGroupAttr` goes inside a `userMatchers` entry, not directly under `groupSearch`.

Check: log in with the `groups` scope and confirm parent groups appear in the claim.

## Checked

2026-11-03: read against Dex docs, LDAP connector (https://dexidp.io/docs/connectors/ldap/).

Removed or corrected: The unsupported claim that recursion adds extra queries per login; corrected the YAML so recursionGroupAttr sits inside the userMatchers entry.

Method: documentation only; no commands were run.
