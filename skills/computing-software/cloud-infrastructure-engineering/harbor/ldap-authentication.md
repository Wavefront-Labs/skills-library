---
id: computing-software.cloud-infrastructure-engineering.harbor.ldap-authentication
name: ldap-authentication
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [ldap, active-directory, ldap-groups, memberof, ldap-search-dn]
level: practitioner
status: docs-checked
description: "Configure Harbor LDAP/AD login: search DN, base DN, filter, UID, scope, group settings, memberof requirement and the test button."
sources:
  - https://goharbor.io/docs/main/administration/configure-authentication/ldap-auth/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
With LDAP/AD authentication, users in an external directory log in directly and you do not create accounts in Harbor. You can switch from database mode to LDAP only if no user other than `admin` exists in Harbor. Self-registration, creating or deleting users and changing or resetting passwords are not supported in this mode.

Under Administration, Configuration, **Authentication**, set **Auth Mode** to LDAP, enter the server address (for example `ldaps://10.162.16.194`) and fill in:
- **LDAP Search DN** and **LDAP Search Password**: the bind identity, for example `cn=admin,dc=example.com`.
- **LDAP Base DN**: lookup root, subtree included.
- **LDAP Filter**: for example `objectclass=user`.
- **LDAP UID**: attribute matched to the login name, such as `uid` or `cn`. The password is then checked by a bind request.
- **LDAP Scope**: Subtree, Base or OneLevel.

For group-based authentication the server must support `memberof` (enabled by default in Active Directory), so a user `memberof` attribute follows group `member` changes. Group fields: **LDAP Group Base DN**, **LDAP Group Filter** (`objectclass=groupOfNames` for OpenLDAP, `objectclass=group` for AD), **LDAP Group GID** (for example `cn`), **LDAP Group Admin DN** (members become system administrators) and **LDAP Group Membership** (default `memberof`). Enable **LDAP Group Attached in Parallel** to avoid login timeouts for users with many groups.

Untick **LDAP Verify Cert** for self-signed certificates, click **Test LDAP Server**, then **Save**.

## Checked

2026-11-03. Mode-switch rule, unsupported operations, every LDAP field and example, group settings and the memberof requirement were read against the Harbor docs page for LDAP/AD authentication. Nothing removed.

Method: documentation only; no commands were run.
