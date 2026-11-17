---
id: computing-software.database-administration.mongodb.ldap-and-kerberos-authentication
name: ldap-and-kerberos-authentication
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-ldap, kerberos, mongodb-security, ldap-authorization, enterprise-authentication]
level: practitioner
status: docs-checked
description: "Configure MongoDB Enterprise LDAP (proxy auth and LDAP authorization) and Kerberos/GSSAPI authentication, with mongoldap testing and common failure causes."
sources:
  - https://www.mongodb.com/docs/manual/core/security-ldap/
  - https://www.mongodb.com/docs/manual/core/security-ldap-external/
  - https://www.mongodb.com/docs/manual/core/kerberos/
  - https://www.mongodb.com/docs/manual/reference/program/mongoldap/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LDAP and Kerberos authentication (Enterprise)

**Goal:** authenticate MongoDB users against the corporate directory and map AD groups to MongoDB roles, so no per-user passwords live in the database. Requires MongoDB Enterprise. LDAP authentication and authorization has been deprecated since MongoDB 8.0 (and remains deprecated in 9.0) and will be removed in a future release; the manual recommends migrating to Workforce Identity Federation (OIDC) for people and Workload Identity Federation or X.509 for applications.

## LDAP proxy authentication + LDAP authorization
```yaml
# mongod.conf
security:
  authorization: enabled
  ldap:
    servers: "ldap1.corp.example:636,ldap2.corp.example:636"
    transportSecurity: tls
    bind:
      method: simple
      queryUser: "CN=svc-mongo,OU=Service,DC=corp,DC=example"
      queryPassword: "<from secret store>"
    userToDNMapping: '[{ match: "(.+)", ldapQuery: "DC=corp,DC=example??sub?(sAMAccountName={0})" }]'
    authz:
      queryTemplate: "{USER}?memberOf?base"   # RFC 4516 query URL; assumes the memberOf attribute and a DN as {USER}
setParameter:
  authenticationMechanisms: "PLAIN,SCRAM-SHA-256"
```
Roles are created in `admin` with the **group DN** as the role name:
```javascript
db.getSiblingDB("admin").createRole({ role: "CN=dba,OU=Groups,DC=corp,DC=example", privileges: [], roles: ["root"] })
```
`{USER}` is replaced with the authenticated (or `userToDNMapping`-transformed) username; `{PROVIDED_USER}` is the name as supplied. Design the query to return the user's group DNs; the template above is the manual's `memberOf` example and depends on your directory.

## Test before restarting mongod
```bash
mongoldap --config /etc/mongod.conf --user alice --password '...'
```
`mongoldap` tests the LDAP configuration (options include `--config`, `--user`, `--password`) so you can check it before relying on it.

## Client login
```bash
mongosh "mongodb://alice@db1.example:27017/?authSource=\$external&authMechanism=PLAIN&tls=true"
```
PLAIN sends the password, so use TLS on the client connection.

## Kerberos (GSSAPI)
1. Create SPN `mongodb/db1.example.com@CORP.EXAMPLE` and a keytab; set `KRB5_KTNAME=/etc/mongodb.keytab` in the service environment.
2. `setParameter: authenticationMechanisms: GSSAPI,SCRAM-SHA-256`.
3. Users: `db.getSiblingDB("$external").createUser({ user: "alice@CORP.EXAMPLE", roles: [...] })` (or LDAP authz for roles).
4. Client: `kinit alice` then `mongosh --host db1.example.com --authenticationMechanism GSSAPI --authenticationDatabase '$external' -u alice@CORP.EXAMPLE`.

## Common failures
- Hostname mismatch: Kerberos needs the FQDN that matches the SPN, reverse DNS matters.
- Kerberos servers and MongoDB hosts must be within the maximum clock skew (5 minutes by default).
- `ldapUserCacheInvalidationInterval` (default 30 seconds) controls how long the LDAP user cache is kept.
- Keep a local SCRAM admin user for break-glass when LDAP is down.

## Verify
`db.runCommand({connectionStatus: 1})` shows `authenticatedUsers` with db `$external` and the expected roles.

## Checked

2026-10-25, against the MongoDB manual source (mongodb/docs repository, content/manual/manual, latest commit 2026-10-23). Confirmed: LDAP authentication and authorization deprecated starting in 8.0 (still in 9.0) with OIDC/Workload Identity/X.509 recommended instead, Enterprise requirement, security.ldap options (transportSecurity, userToDNMapping with {0}, authz.queryTemplate with {USER} and {PROVIDED_USER}), role named by the LDAP group DN in admin, authenticationMechanisms PLAIN with $external and --authenticationMechanism PLAIN, mongoldap with --config/--user/--password, ldapUserCacheInvalidationInterval default 30 s, Kerberos users in $external with an upper-case realm, GSSAPI mechanism, mongodb/<host>@REALM service principal and keytab with KRB5_KTNAME, canonical hostname must match the SPN, 5 minute maximum clock skew. Removed the unconfirmed nested-group matching rule claim and mongoldap step description.

Method: documentation only; no commands were run.
