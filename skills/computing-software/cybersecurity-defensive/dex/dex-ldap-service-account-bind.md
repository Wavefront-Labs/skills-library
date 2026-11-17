---
id: computing-software.cybersecurity-defensive.dex.dex-ldap-service-account-bind
name: dex-ldap-service-account-bind
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [ldap, binddn, bindpw, usernameprompt]
level: practitioner
status: docs-checked
description: "Configure the Dex LDAP service account with bindDN and bindPW, store passwords with $ in an environment variable, and set usernamePrompt."
sources:
  - https://dexidp.io/docs/connectors/ldap/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The connector searches users and groups with an application service account, set by `bindDN` and `bindPW`. They are not required if the LDAP server allows anonymous access.

```yaml
config:
  host: ldap.example.com:636
  bindDN: uid=serviceaccount,cn=users,dc=example,dc=com
  bindPW: $LDAP_BIND_PW
  usernamePrompt: SSO Username
```

Points from the docs:

- If the bind password contains a `$`, it must be saved in an environment variable, and that variable is given as the value of `bindPW`.
- `usernamePrompt` sets the attribute label shown in the login form. If unset it shows "Username". The Active Directory example uses `Email Address`.
- The AD kubelogin sample says the bind user "would normally be a read-only user".

Gotcha: the docs' Active Directory sample uses an Administrator DN only as an example. Use a read-only account.

Check: attempt a login with a known user and confirm the search succeeds.

The connector first initializes a connection to the directory using `bindDN` and `bindPW`, then searches for the given username and binds as that user to verify the password.

## Checked

2026-11-03: read against Dex docs, LDAP connector (https://dexidp.io/docs/connectors/ldap/).

Removed or corrected: The claim that a literal $ would be treated as variable expansion.

Method: documentation only; no commands were run.
