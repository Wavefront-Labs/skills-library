---
id: computing-software.database-administration.cockroachdb.ldap-authentication
name: ldap-authentication
category: computing-software
field: database-administration
product: cockroachdb
tags: [ldap-authentication, active-directory, host-based-authentication, hba, user-provisioning]
level: advanced
status: docs-checked
description: "Configure CockroachDB LDAP or Active Directory login via the HBA cluster setting, bind credentials redaction, optional TLS settings and user provisioning."
sources:
  - https://www.cockroachlabs.com/docs/stable/ldap-authentication
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let users sign in with directory credentials.

Step 1, protect secrets: the HBA setting will contain the LDAP bind password, so enable redaction of sensitive cluster settings first so only authorized users (such as `admin` members) can view it.

Step 2, host-based authentication: set `server.host_based_authentication.configuration`. Parameters: `ldapserver`, `ldapport` (typically 636 for LDAPS), `ldapbasedn`, `ldapbinddn` (service account DN), `ldapbindpasswd`, `ldapsearchattribute` (matched to the SQL username), `ldapsearchfilter` (restricts valid users, e.g. group membership). Example from the page:
```sql
SET CLUSTER SETTING server.host_based_authentication.configuration = '
host all all all ldap ldapserver=ldap.example.com
    ldapport=636
    "ldapbasedn=ou=users,dc=example,dc=com"
    "ldapbinddn=cn=readonly,dc=example,dc=com"
    ldapbindpasswd=<bind-password>
    ldapsearchattribute=uid
    "ldapsearchfilter=(memberof=cn=cockroachdb_users,ou=groups,dc=example,dc=com)"';
```

Step 3, optional TLS to the directory: `server.ldap_authentication.domain.custom_ca`, `server.ldap_authentication.client.tls_certificate`, `server.ldap_authentication.client.tls_key` (PEM values).

Step 4, user creation, choose one:
- Automatic provisioning (recommended): `SET CLUSTER SETTING security.provisioning.ldap.enabled = true;` Users get a `PROVISIONSRC` role option of `ldap:{ldap_server}` and `estimated_last_login_time` is tracked.
- Manual: `CREATE ROLE username LOGIN;` for each user.

Gotcha: authentication succeeding only proves identity; privileges still come from SQL roles and grants.

Before enabling automatic provisioning, the page recommends enabling LDAP authorization so new users get the intended roles.

## Checked

2026-11-03. Confirmed against the LDAP authentication page: HBA setting and parameters, redaction, TLS settings, provisioning option and `PROVISIONSRC`, `estimated_last_login_time`, manual `CREATE ROLE`. Removed: invented verification step.
Method: documentation only; no commands were run.
