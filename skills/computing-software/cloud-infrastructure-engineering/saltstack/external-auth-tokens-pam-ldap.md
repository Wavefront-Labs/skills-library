---
id: computing-software.cloud-infrastructure-engineering.saltstack.external-auth-tokens-pam-ldap
name: external-auth-tokens-pam-ldap
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, external-auth, tokens, pam, ldap, active-directory]
level: advanced
status: docs-checked
description: "Use Salt eauth tokens (-T, salt_token, 12 hour default) and know the PAM requirements and LDAP/Active Directory prerequisites for external auth."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/eauth/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# eAuth tokens, PAM and LDAP

Tokens: add `-T` to a command to create a short-term token, stored in `salt_token` in the user's home directory, so credentials need not be re-entered.

For example `salt -T -a pam <target> <function>`. The default lifetime is 12 hours, configurable on the master.

PAM caveats:
- The master must run as root for PAM checks.
- PAM uses the `login` service.
- Authenticating as `root` is not allowed.

LDAP and Active Directory:
- Require the python-ldap package.
- Master config settings cover the server, TLS, bind credentials, the user search filter and group lookup.
- Active Directory uses different group-membership settings than OpenLDAP.

## Checked

2026-11-09. Read against the eauth source (doc/topics/eauth/index.rst); token, PAM and LDAP statements were confirmed there. Nothing removed.
Method: documentation only; no commands were run.
