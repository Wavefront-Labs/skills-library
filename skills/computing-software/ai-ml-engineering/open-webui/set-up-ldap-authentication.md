---
id: computing-software.ai-ml-engineering.open-webui.set-up-ldap-authentication
name: set-up-ldap-authentication
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [ldap-scim, ldap, openldap, authentication, troubleshooting, open-webui]
level: practitioner
status: docs-checked
description: "Connect Open WebUI to OpenLDAP with ENABLE_LDAP and LDAP_* variables, test with ldapsearch and ldapwhoami, and fix the common bind and TLS errors."
sources:
  - https://docs.openwebui.com/features/authentication-access/auth/ldap
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: users log in with their LDAP uid and password.

## 1. Test the directory first
```bash
ldapsearch -x -H ldap://localhost:389 -D "cn=admin,dc=example,dc=org" -w admin -b "dc=example,dc=org" "(uid=jdoe)"
```
(Docs use an `osixia/openldap:1.5.0` test container with `LDAP_DOMAIN=example.org`, seeded with `docker exec openldap ldapadd -x -D "cn=admin,dc=example,dc=org" -w admin -f /seed.ldif`; the example `inetOrgPerson` entry carries `cn`, `sn`, `uid`, `mail` and `userPassword`. Outside tests use a hashed password, for example from `slappasswd`.)

## 2. Open WebUI variables
```env
ENABLE_LDAP="true"
LDAP_SERVER_LABEL="OpenLDAP"
LDAP_SERVER_HOST="localhost"   # hostname/IP only, no ldap:// prefix
LDAP_SERVER_PORT=389           # 636 for LDAPS; no quotes
LDAP_USE_TLS="false"           # default is "true"
LDAP_VALIDATE_CERT="false"     # default "true"; keep true in production
LDAP_APP_DN="cn=admin,dc=example,dc=org"
LDAP_APP_PASSWORD="admin"
LDAP_SEARCH_BASE="dc=example,dc=org"
LDAP_ATTRIBUTE_FOR_USERNAME="uid"
LDAP_ATTRIBUTE_FOR_MAIL="mail"
# LDAP_DEFAULT_EMAIL_DOMAIN="example.org"
# LDAP_SEARCH_FILTER="(memberOf=cn=allowed-users,ou=groups,dc=example,dc=org)"
```
`LDAP_SEARCH_FILTER` is only for extra conditions; the username filter is added automatically, so never include `%(user)s` or `%s`.

Env vars are read only at first startup (PersistentConfig) unless `ENABLE_PERSISTENT_CONFIG=false`. Alternatively use Admin Panel > Settings > Authentication > LDAP; saved settings apply on the next login attempt without restart.

## 3. Log in
Use the uid and password in a fresh browser window. A new account gets the instance default role (`pending` unless changed); the first account on an instance is admin.

## Fixing errors
- `port must be an integer`: remove quotes from `LDAP_SERVER_PORT` and remove protocol from `LDAP_SERVER_HOST`.
- `SSL: UNEXPECTED_EOF_WHILE_READING`: TLS mismatch. Plaintext = port 389 with `LDAP_USE_TLS=false`; LDAPS = 636 with `true`. StartTLS is NOT supported (implicit TLS only).
- `err=49` (invalid credentials) on the user's bind: check password and user DN; isolate with `ldapwhoami -x -H ldap://localhost:389 -D "uid=jdoe,ou=users,dc=example,dc=org" -w "password123"`.
- `User does not have a valid email address.`: user has no mail attribute; set `LDAP_DEFAULT_EMAIL_DOMAIN` (user becomes `username@domain`; if an account with that address exists the LDAP user signs into it, so use a domain you control).

## Checked
2026-11-07. Confirmed against the Open WebUI docs: features/authentication-access/auth/ldap (read in full). Replaced the unconfirmed ldapadd description with the page's own seed command.
Method: documentation only; no commands were run.
