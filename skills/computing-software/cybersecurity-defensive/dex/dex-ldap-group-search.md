---
id: computing-software.cybersecurity-defensive.dex.dex-ldap-group-search
name: dex-ldap-group-search
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [ldap, groupsearch, usermatchers, groups]
level: practitioner
status: docs-checked
description: "Configure Dex LDAP groupSearch with userMatchers pairing a user attribute to a group attribute, including DN and mixed group object classes."
sources:
  - https://dexidp.io/docs/connectors/ldap/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`groupSearch` finds groups for a user entry. Each group query adds a requirement that a group attribute matches a user attribute.

```yaml
groupSearch:
  baseDN: cn=groups,dc=example,dc=com
  filter: "(objectClass=group)"
  userMatchers:
  - userAttr: uid
    groupAttr: member
  nameAttr: name
```

- `baseDN`, `filter`: where and what to search.
- `userMatchers`: list of `userAttr` / `groupAttr` pairs.
- `nameAttr`: attribute holding the group name.

Match on distinguished names by using the keyword `DN` (capitalised) in `userAttr`:

```yaml
userMatchers:
- userAttr: DN
  groupAttr: member
```

POSIX groups list members by uid in `memberUid`:

```yaml
filter: "(objectClass=posixGroup)"
userMatchers:
- userAttr: uid
  groupAttr: memberUid
nameAttr: cn
```

When group types use different attributes, widen the filter and give several matchers so Dex knows which to use:

```yaml
filter: "(|(objectClass=posixGroup)(objectClass=group))"
userMatchers:
- userAttr: uid
  groupAttr: memberUid
- userAttr: DN
  groupAttr: member
```

Gotcha: group claims only appear when the client requests the `groups` scope.

Group searches must match a user attribute to a group attribute. For the `member` example the final query is `(&(objectClass=group)(member=<user uid>))`.

## Checked

2026-11-03: read against Dex docs, LDAP connector (https://dexidp.io/docs/connectors/ldap/).

Removed or corrected: Nothing removed.

Method: documentation only; no commands were run.
