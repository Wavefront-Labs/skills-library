---
id: computing-software.cloud-infrastructure-engineering.zot.ldap-authentication
name: ldap-authentication
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, ldap, bind-dn, credentials-file, user-group-attribute, ldap-groups]
level: practitioner
status: docs-checked
description: "Configure Zot LDAP authentication with a bind credentials file, base DN, user attribute and filter, group attribute, and using group FQDNs in policies."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/authn-authz.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```json
"http": { "auth": { "ldap": {
  "credentialsFile": "examples/config-ldap-credentials.json",
  "address": "ldap.example.org", "port": 389, "startTLS": false,
  "baseDN": "ou=Users,dc=example,dc=org",
  "userAttribute": "uid",
  "userFilter": "(!(nsaccountlock=TRUE))",
  "userGroupAttribute": "memberOf",
  "skipVerify": false, "subtreeSearch": true
} } }
```

- `credentialsFile`: path to bind credentials.
- `address`, `port`: LDAP server.
- `startTLS`: enables TLS to the LDAP server.
- `baseDN`: start of user searches; `subtreeSearch` widens to subtrees.
- `userAttribute`: attribute holding the username; `userFilter`: optional extra filter.
- `userGroupAttribute`: attribute listing user groups.
- `skipVerify`: skips TLS verification (avoid outside testing).

Credentials file:

```json
{ "bindDN": "cn=ldap-searcher,ou=Users,dc=example,dc=org", "bindPassword": "ldap-searcher-password" }
```

In access control, reference LDAP groups by their FQDN, for example `cn=ldap-group,ou=Groups,dc=example,dc=org`.

If htpasswd is also configured it is checked first. Docker clients and basic auth: see the docker mixed-access skill.

## Checked

2026-11-04. Read against the zot authn-authz article (LDAP section and access control notes); every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
