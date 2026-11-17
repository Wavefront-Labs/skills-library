---
id: computing-software.cloud-infrastructure-engineering.openbao.ldap-auth
name: ldap-auth
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, ldap, groupfilter, binddn, starttls]
level: practitioner
status: docs-checked
description: "Configure OpenBao LDAP auth: connection and search parameters, group-to-policy mapping, DN escaping and stale token behaviour."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/auth/ldap.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LDAP auth

```
bao auth enable ldap
bao write auth/ldap/config \
    url="ldap://ldap.example.com" \
    userattr=sAMAccountName \
    userdn="ou=Users,dc=example,dc=com" \
    groupdn="ou=Users,dc=example,dc=com" \
    groupfilter="(&(objectClass=person)(uid={{.Username}}))" \
    groupattr="memberOf" \
    binddn="cn=openbao,ou=users,dc=example,dc=com" \
    bindpass='<bind-password>' \
    certificate=@ldap_ca_cert.pem \
    insecure_tls=false \
    starttls=true
```

## Parameters

`url` (required; comma-separated URLs tried in order), `groupdn` (required), `starttls`, `insecure_tls` (skips verification; use with caution), `binddn`/`bindpass`, `userdn`, `userattr`, `groupfilter` (Go template with `UserDN` and `Username`), `groupattr` (default `cn`).

## Policies and login

```
bao write auth/ldap/groups/scientists policies=foo,bar
bao write auth/ldap/users/tesla groups=engineers policies=zoobar
bao login -method=ldap username=tesla
```

## Gotchas

- You must supply properly escaped DNs. Active Directory also needs `#` escaped anywhere and `=` in usernames.
- The user filter must contain `{{.UserAttr}}` or the literal `userattr` value for unique results.
- LDAP group changes do not affect tokens already issued; revoke them and have users re-authenticate.
- Lockout: 5 attempts, 15 minutes by default.

## Checked

2026-11-04. Read the OpenBao LDAP auth method page in full. Confirmed: connection, binding and group parameters and the `groupattr` default of `cn`, the example configuration (scenario 2), group and user policy mapping commands, DN escaping notes, the stale-token note and the lockout defaults. Removed: nothing.
Method: documentation only; no commands were run.
