---
id: computing-software.database-administration.pgbouncer.ldap-and-pam-auth
name: ldap-and-pam-auth
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, ldap, pam, authentication, auth-ldap-options]
level: advanced
status: docs-checked
description: "Using auth_type ldap with auth_ldap_options and auth_type pam, including build requirements and limits."
sources:
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/install.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: delegate client authentication to LDAP or PAM.

Both methods require a PgBouncer build that includes the feature, so check your package supports it. Per the install docs, the Meson options -Dpam and -Dldap default to auto (built when libraries exist); the Autoconf build needs explicit `--with-pam` or `--with-ldap`. The LDAP build option is not supported on Windows.

LDAP: set `auth_type = ldap`. Users are authenticated against an LDAP server as in PostgreSQL (see PostgreSQL's LDAP authentication docs). Connection options go in `auth_ldap_options`, or in the auth_hba_file instead (the setting is not used when authentication is configured via the HBA file):

```
auth_type = ldap
auth_ldap_options = ldapurl="ldap://127.0.0.1:12345/dc=example,dc=net?uid?sub"
```

PAM: set `auth_type = pam` in the global [pgbouncer] section. PAM validates users, auth_file is ignored, and the service name reported to PAM is `pgbouncer`. PAM is not compatible with databases that use the auth_user option, and `pam` is not supported inside the HBA configuration file (it works only as a global auth_type).

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
