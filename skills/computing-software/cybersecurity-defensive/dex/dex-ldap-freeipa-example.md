---
id: computing-software.cybersecurity-defensive.dex.dex-ldap-freeipa-example
name: dex-ldap-freeipa-example
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [ldap, freeipa, groups, example]
level: practitioner
status: docs-checked
description: "Use the documented Dex LDAP configuration for a FreeIPA server: posixAccount user search, group search by member and a custom rootCA."
sources:
  - https://dexidp.io/docs/connectors/ldap/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The docs give a FreeIPA configuration where users are `posixAccount` entries and groups use the `member` attribute.

```yaml
connectors:
- type: ldap
  id: ldap
  name: LDAP
  config:
    host: freeipa.example.com:636
    rootCA: ca.crt
    userSearch:
      baseDN: cn=users,dc=freeipa,dc=example,dc=com
      filter: "(objectClass=posixAccount)"
      username: uid
      idAttr: uid
      emailAttr: mail
    groupSearch:
      baseDN: cn=groups,dc=freeipa,dc=example,dc=com
      filter: "(objectClass=group)"
      userMatchers:
      - userAttr: uid
        groupAttr: member
      nameAttr: name
```

How it translates:

- The user search becomes `(&(objectClass=posixAccount)(uid=<username>))`.
- The group search becomes `(&(objectClass=group)(member=<user uid>))`.
- If the user search finds an entry, Dex tries the provided password to bind as that entry.

The `rootCA` is the FreeIPA server's CA. Port 636 is the LDAPS default, so `host` needs no extra TLS flags.

Gotcha: the user and group `baseDN` values here are examples. Replace `freeipa.example.com` and the `dc=` components with your own realm, then verify with `ldapsearch` before putting them in Dex.

Add the `groups` scope to the initial redirect of the client so that group information from the directory appears in the ID token.

## Checked

2026-11-03: read against Dex docs, LDAP connector (https://dexidp.io/docs/connectors/ldap/).

Removed or corrected: Nothing removed.

Method: documentation only; no commands were run.
