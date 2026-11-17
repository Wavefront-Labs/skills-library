---
id: computing-software.collaboration-platform-administration.vikunja.ldap-authentication
name: ldap-authentication
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, ldap-bind, userfilter, binddn-service-account, attribute-mapping, ldap-tls]
level: practitioner
status: docs-checked
description: "Enable LDAP login in Vikunja: the bind flow, userfilter with the %[1]s placeholder, service account, TLS settings, attribute mapping and Active Directory example."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/ldap.mdx
  - https://raw.githubusercontent.com/go-vikunja/vikunja/main/config-raw.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Login flow: Vikunja binds with the service account, searches the user with `userfilter`, then binds as that user. On success it creates or updates the Vikunja account from the mapped attributes.

```
auth:
  ldap:
    enabled: true
    host: ldap.example.com
    port: 389
    basedn: dc=example,dc=com
    userfilter: "(&(objectClass=person)(uid=%[1]s))"
    binddn: "cn=admin,dc=example,dc=com"
    bindpassword: "secretpassword"
```

`%[1]s` becomes the typed username and may repeat, for example `(|(uid=%[1]s)(mail=%[1]s))` to allow username or email. Adjust at least the `objectClass`. The bind account should have minimal permissions.

TLS: `usetls` is true by default; disable only if you must. `verifytls: false` skips certificate chain checks.

Attributes: `attribute.username` (default `uid`), `email` (`mail`), `displayname` (`displayName`). Users must have an email address.

Active Directory: `userfilter: (&(objectClass=user)(sAMAccountName=%[1]s))` and `attribute.username: sAMAccountName`.

Environment form: `VIKUNJA_AUTH_LDAP_ENABLED`, `_HOST`, `_BASEDN`, `_USERFILTER`, `_BINDDN`, `_BINDPASSWORD`, `_ATTRIBUTE_USERNAME`.

## Checked

2026-11-04: flow, example config, `%[1]s` placeholder, TLS settings, attribute mapping, Active Directory example and env names checked against the LDAP page; defaults against config-raw.json (auth.ldap).

Method: documentation only; no commands were run.
