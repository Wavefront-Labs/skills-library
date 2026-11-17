---
id: computing-software.database-administration.yugabytedb.ldap-authentication-ysql
name: ldap-authentication-ysql
category: computing-software
field: database-administration
product: yugabytedb
tags: [ldap, ldap-authentication, simple-bind, search-and-bind, ldapbasedn, ysql-hba-conf-csv, ldaps]
level: advanced
status: docs-checked
description: "Configure YSQL LDAP authentication in ysql_hba_conf_csv using simple bind (ldapprefix, ldapsuffix) or search+bind (ldapbasedn, ldapsearchattribute), with TLS options."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/secure/authentication/ldap-authentication-ysql.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LDAP authentication for YSQL

LDAP works like password authentication, but the password is verified by the directory. The role must already exist in YugabyteDB with the right privileges. Configure it in `--ysql_hba_conf_csv`.

**Simple bind:** the tserver builds the DN as prefix + username + suffix.
```
--ysql_hba_conf_csv='host all yugabyte 127.0.0.1/0 password,"host all all 0.0.0.0/0 ldap ldapserver=ldap.example.com ldapprefix=""uid="" ldapsuffix="", ou=DBAs, dc=example, dc=com"" ldapport=389"'
```

**Search+bind:** the tserver binds with a fixed account (`ldapbinddn` and `ldapbindpasswd`; anonymous if omitted), searches the subtree at `ldapbasedn` for the user, then binds as the found DN.
```
--ysql_hba_conf_csv='host all yugabyte 127.0.0.1/0 password,"host all all 0.0.0.0/0 ldap ldapserver=ldap.example.com ldapbasedn=""dc=example, dc=com"" ldapsearchattribute=uid"'
```

Options:
- `ldapserver` (space-separated list), `ldapport` (389)
- `ldapscheme=ldaps` for LDAP over SSL (a non-standard approach some servers support); `ldaptls=1` (default 0) to make the connection use TLS
- `ldapsearchattribute` (default uid), `ldapsearchfilter`, `ldapurl` (an RFC 4516 URL)

Keep a password rule for the `yugabyte` admin on localhost first (as in the examples) so an administrator can log in to create the roles and permissions for LDAP users. Quote HBA values carefully: the examples double the double quotes inside the CSV value. The Kubernetes section of the page also shows passing the bind password from a secret through an environment variable.

## Checked

2026-11-04. Confirmed against the LDAP authentication in YSQL page: `--ysql_hba_conf_csv`, role must already exist, simple bind (prefix + username + suffix) and search+bind (`ldapbinddn`, `ldapbindpasswd`, anonymous bind when none, `ldapbasedn`, `ldapsearchattribute` default uid, `ldapsearchfilter`, `ldapurl` RFC 4516), `ldapserver` space-separated, `ldapport` default 389, `ldapscheme`, `ldaptls`, and the two-rule example. Reworded the reason for keeping the yugabyte password rule to the page's own explanation (the directory-down rationale is not stated).

Method: documentation only; no commands were run.
