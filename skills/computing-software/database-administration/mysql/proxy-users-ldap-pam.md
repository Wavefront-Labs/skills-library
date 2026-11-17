---
id: computing-software.database-administration.mysql.proxy-users-ldap-pam
name: proxy-users-ldap-pam
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, proxy-users, ldap-authentication, pam-authentication, authentication-ldap-sasl, external-authentication, mysql-security]
level: practitioner
status: draft
description: "Map external identities to MySQL privileges with proxy users and pluggable LDAP or PAM authentication, including group mapping and the default proxy account."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/proxy-users.html
  - https://dev.mysql.com/doc/refman/8.4/en/ldap-pluggable-authentication.html
  - https://dev.mysql.com/doc/refman/8.4/en/pam-pluggable-authentication.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Proxy users and pluggable LDAP / PAM authentication

External auth plugins (LDAP, PAM, Kerberos) are MySQL Enterprise features; Percona Server ships a free PAM plugin (`auth_pam`) and MariaDB has `pam`. Proxying works the same way with each.

## Proxy concept
A login authenticates as account A (proxy user) but runs with the privileges of account B (proxied user).
```sql
CREATE USER 'dev_role'@'%' IDENTIFIED WITH caching_sha2_password BY '<RANDOM>' ACCOUNT LOCK;   -- privilege holder, nobody logs in
GRANT SELECT, INSERT, UPDATE, DELETE ON app.* TO 'dev_role'@'%';
CREATE USER 'alice'@'%' IDENTIFIED WITH authentication_ldap_simple AS 'uid=alice,ou=People,dc=example,dc=com';
GRANT PROXY ON 'dev_role'@'%' TO 'alice'@'%';
```
```sql
-- as alice
SELECT USER(), CURRENT_USER(), @@proxy_user;   -- alice@host, dev_role@%, 'alice'@'%'
```
Plugins must permit proxying: `check_proxy_users = ON` plus `<plugin>_proxy_users = ON` (e.g. `sha256_password_proxy_users`) for built-in plugins; LDAP/PAM plugins handle it themselves.

## Group mapping with a default proxy account (LDAP)
```ini
[mysqld]
plugin-load-add = authentication_ldap_sasl.so
authentication_ldap_sasl_server_host = ldap.example.com
authentication_ldap_sasl_bind_base_dn = 'ou=People,dc=example,dc=com'
authentication_ldap_sasl_group_search_attr = cn
```
```sql
CREATE USER ''@'%' IDENTIFIED WITH authentication_ldap_sasl AS '+ou=People,dc=example,dc=com#dba=dba_role,devs=dev_role';
GRANT PROXY ON 'dba_role'@'%' TO ''@'%';
GRANT PROXY ON 'dev_role'@'%' TO ''@'%';
```
Any LDAP user who authenticates and is in group `dba` runs as `dba_role`; no per-person MySQL account needed. Membership changes in LDAP take effect at next login.

## PAM (Percona auth_pam)
```sql
INSTALL PLUGIN auth_pam SONAME 'auth_pam.so';
CREATE USER ''@'' IDENTIFIED WITH auth_pam AS 'mysqld, dba=dba_role, devs=dev_role';   -- PAM service, unix group mapping
```
`/etc/pam.d/mysqld` defines the stack (sssd/ldap). Clients need the cleartext plugin: `mysql --enable-cleartext-plugin` (use TLS).

## Gotchas
- The anonymous `''@'%'` default proxy matches any user name; ensure no other anonymous accounts exist, and that more specific accounts take precedence the way you expect (MySQL matches the most specific host/user first).
- Cleartext-password plugins (LDAP simple, PAM) must only run over TLS (`require_secure_transport = ON`).
- Auditing shows both `USER()` (external) and `CURRENT_USER()` (proxied); log both.
