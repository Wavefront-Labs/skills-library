---
id: computing-software.cybersecurity-defensive.dex.dex-ldap-user-search
name: dex-ldap-user-search
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [ldap, usersearch, attributes, basedn]
level: practitioner
status: docs-checked
description: "Map an LDAP schema to Dex userSearch: baseDN, filter, username, idAttr, emailAttr, nameAttr, preferredUsernameAttr, and the DN keyword."
sources:
  - https://dexidp.io/docs/connectors/ldap/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`userSearch` maps the username entered by the user to a directory entry.

```yaml
userSearch:
  baseDN: cn=users,dc=example,dc=com
  filter: "(objectClass=person)"
  username: uid
  idAttr: uid
  emailAttr: mail
  nameAttr: name
  preferredUsernameAttr: uid
```

- `baseDN`: where the search starts.
- `filter`: optional, combined with the username match. The final query looks like `(&(objectClass=person)(uid=<username>))`.
- `username`: attribute compared with the typed username.
- `idAttr`: string identity of the user.
- `emailAttr`: required. Attribute mapped to email.
- `nameAttr`: display name (no default). `preferredUsernameAttr`: preferred username (no default).

Setting an `*Attr` to `DN` uses the entry's distinguished name. `DN` is case-sensitive and must be capitalised.

To discover your schema, install `ldap-utils` (apt) or `openldap-clients` (dnf) and dump entries:

```bash
ldapsearch -x -H ldap://ldap.example.org -b 'dc=example,dc=org' | less
```

A POSIX/FreeIPA compat example uses `filter: "(objectClass=posixAccount)"`, `idAttr: DN` and `nameAttr: gecos`.

Gotcha: if no email attribute exists, use another unique value such as `uid` for `emailAttr`, since the field is required.

## Checked

2026-11-03: read against Dex docs, LDAP connector (https://dexidp.io/docs/connectors/ldap/).

Removed or corrected: Nothing removed.

Method: documentation only; no commands were run.
