---
id: computing-software.database-administration.scylladb.security-ldap-authentication-saslauthd
name: security-ldap-authentication-saslauthd
category: computing-software
field: database-administration
product: scylladb
tags: [ldap, saslauthd, authentication, saslauthdauthenticator, mechanism]
level: advanced
status: docs-checked
description: "LDAP authentication for ScyllaDB through saslauthd: install and test saslauthd, set mechanism ldap, authenticator SaslauthdAuthenticator, saslauthd_socket_path and matching roles."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/security/ldap-authentication.rst", "https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/security/saslauthd.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LDAP authentication via saslauthd

ScyllaDB outsources authentication to `saslauthd` through its custom `SaslauthdAuthenticator`; saslauthd talks to LDAP (or PAM).

1. Install saslauthd: package `cyrus-sasl` (rpm-based) or `sasl2-bin` (deb-based). Enable it: `systemctl enable saslauthd.service`.
2. Set the mechanism:
   - rpm: `/etc/sysconfig/saslauthd` gets `MECH=ldap`
   - deb: `/etc/default/saslauthd` gets `MECHANISMS=ldap`
3. Edit `/etc/saslauthd.conf` with the LDAP server parameters from the Cyrus SASL saslauthd LDAP documentation.
4. After every change run `systemctl restart saslauthd.service`, then test with `testsaslauthd`; you must see a success message. On failure check credentials and the saslauthd logs (`dmesg -H`, look for `LOG_AUTH`).
5. Find the saslauthd Unix socket (the mux file): usually `/run/saslauthd/mux` on rpm systems and `/var/run/sasl2/mux` on deb systems.
6. In `scylla.yaml` set on every node:
```
authenticator: com.scylladb.auth.SaslauthdAuthenticator
saslauthd_socket_path: /path/to/the/mux
```
7. Restart ScyllaDB. All logins are now authenticated through saslauthd.
8. Create ScyllaDB roles that match the roles in the LDAP server (see CQL security reference and the RBAC example).

## Checked

2026-11-09. Confirmed packages, service commands, mechanism settings per distro family, testsaslauthd check, socket locations, scylla.yaml settings and role matching against the ScyllaDB LDAP and saslauthd pages (both read in full). Removed unsupported claims about roles without permissions and a break-glass superuser.

Method: docs-checked 2026-11-09 against the ScyllaDB docs pages operating-scylla/security/ldap-authentication.rst and saslauthd.rst
