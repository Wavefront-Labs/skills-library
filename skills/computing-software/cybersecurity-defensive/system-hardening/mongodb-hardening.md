---
id: computing-software.cybersecurity-defensive.system-hardening.mongodb-hardening
name: mongodb-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [mongodb-hardening, database-hardening, scram, mongodb-rbac, tls, exposed-database]
level: practitioner
status: docs-checked
description: "Harden self-managed MongoDB: enable authorization, limit network exposure, TLS, least-privilege roles, disable server-side JavaScript, auditing, encryption, patching."
sources: ["https://www.mongodb.com/docs/manual/administration/security-checklist/", "https://www.mongodb.com/docs/manual/core/authorization/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MongoDB hardening

The MongoDB Security Checklist for Self-Managed Deployments is the baseline; it says itself that it is not
exhaustive. Internet-exposed MongoDB without authentication is a common cause of data loss.

## Access control
MongoDB does not enable access control by default. Enable it with `--auth` or the `security.authorization`
setting; enabling internal authentication also enables client authorization. Community supports SCRAM (default) and
X.509 certificate authentication; Atlas and Enterprise add LDAP proxy and Kerberos. LDAP authentication and
authorization is deprecated from MongoDB 8.0 and will be removed in a future release.

## Users and roles
1. The first user created must be a user administrator who can manage other users; create it first, then add others.
2. Create a unique user for each person or application, assign only the roles needed (least privilege), and use
   user-defined roles when built-in ones are too broad.
3. Roles never limit privileges: if a user holds two roles, the greater access applies. Revoke with
   `revokeRolesFromUser`.
4. Use `authenticationRestrictions` on `db.createUser()` or role definitions to require connections from given
   IP ranges. View a role's privileges with `rolesInfo` (`showPrivileges` and `showBuiltinRoles` true).
5. Review users periodically and rotate their credentials.

## Network exposure
Run MongoDB in a trusted network with firewall or security-group rules limiting inbound and outbound traffic to
trusted clients. Related settings: `net.bindIp` and `security.clusterIpSourceAllowlist`. Disable direct SSH root
access.

## TLS
Use TLS for all incoming and outgoing connections, including between `mongod` and `mongos` and from every
application. MongoDB uses the native OS libraries (Schannel on Windows, OpenSSL on Linux/BSD, Secure Transport on
macOS).

## Server-side JavaScript
`mapReduce`, `$where`, `$accumulator` and `$function` run JavaScript on the server. If you do not use them,
disable server-side scripting with `--noscripting`.

## Run safely
Run MongoDB under a dedicated operating-system account with access to the data but no unnecessary permissions.
Protect data files, configuration files, audit logs and key files with file-system permissions. Configure any
antivirus or EDR scanner to exclude the database storage and log paths, which scanners can otherwise quarantine.

## Auditing and logging
MongoDB Enterprise includes an auditing facility with filters (for example authentication events). Collect logs to
a central log store; they contain authentication attempts with source IP addresses.

## Encryption
Use WiredTiger Encryption at Rest, or file-system or device encryption (for example dm-crypt) on each host.
Queryable Encryption or Client-Side Field Level Encryption encrypt fields application-side.

## Ongoing
Check MongoDB CVEs and end-of-life dates and upgrade; review network rule changes that could expose MongoDB to the
Internet; apply OS patches.

## Verify
An unauthenticated connection cannot run commands; non-TLS connections are refused; the app user cannot read other
databases; an external scan shows the MongoDB port closed.

## Checked
2026-10-31. Confirmed on the Security Checklist and Role-Based Access Control pages: access control off by default,
`--auth`/`security.authorization`, SCRAM and X.509, Enterprise/Atlas mechanisms, LDAP deprecation, first-user rule,
least privilege, role precedence, `revokeRolesFromUser`, `rolesInfo`, `authenticationRestrictions`, `net.bindIp`,
`security.clusterIpSourceAllowlist`, TLS libraries, `--noscripting`, dedicated user, AV/EDR exclusion, encryption
options, Enterprise auditing, CVE/EOL review. Removed as not confirmed on those pages: the YAML TLS block and
`javascriptEnabled`, keyFile and `clusterAuthMode` lines, example commands and role names, data-directory mode,
OIDC claim, the 2025 vulnerability remark, and the CIS benchmark source (registration wall).
Method: documentation only; no commands were run.
