---
id: computing-software.cybersecurity-defensive.dex.dex-ldap-active-directory-example
name: dex-ldap-active-directory-example
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [ldap, active-directory, userprincipalname, groups]
level: practitioner
status: docs-checked
description: "Configure the Dex LDAP connector for Active Directory: userPrincipalName login, DN based ids and member group matching."
sources:
  - https://dexidp.io/docs/connectors/ldap/
  - https://dexidp.io/docs/guides/kubelogin-activedirectory/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The docs' Active Directory example logs users in by their UPN and resolves groups through `member`:

```yaml
connectors:
- type: ldap
  name: ActiveDirectory
  id: ad
  config:
    host: ad.example.com:636
    insecureNoSSL: false
    insecureSkipVerify: true
    bindDN: cn=Administrator,cn=users,dc=example,dc=com
    bindPW: admin0!
    usernamePrompt: Email Address
    userSearch:
      baseDN: cn=Users,dc=example,dc=com
      filter: "(objectClass=person)"
      username: userPrincipalName
      idAttr: DN
      emailAttr: userPrincipalName
      nameAttr: cn
    groupSearch:
      baseDN: cn=Users,dc=example,dc=com
      filter: "(objectClass=group)"
      userMatchers:
      - userAttr: DN
        groupAttr: member
      nameAttr: cn
```

Key choices: `username` and `emailAttr` are both `userPrincipalName`, `idAttr` is `DN`, and groups match the user DN against `member`.

Gotchas:

- The example sets `insecureSkipVerify: true` for brevity. In production remove it and supply `rootCA` so certificate checks stay on.
- The sample bind account and password are placeholders. Use a read-only service account and keep its secret in an environment variable.
- The kubelogin guide uses AD with TLS required: "Please ensure TLS is enabled".

Searches that return multiple entries are ambiguous and produce an error, so choose a `username` attribute that is unique per user.

## Checked

2026-11-03: read against Dex docs, LDAP connector (https://dexidp.io/docs/connectors/ldap/); Dex docs, Kubelogin with Active Directory guide (https://dexidp.io/docs/guides/kubelogin-activedirectory/).

Removed or corrected: Nothing removed; the TLS and read-only-user remarks were confirmed on the kubelogin guide.

Method: documentation only; no commands were run.
