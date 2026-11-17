---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-admin-roles-and-accounts
name: pan-os-admin-roles-and-accounts
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [admin-role-profile, pan-os, rbac, admin-accounts, superuser, deviceadmin, role-based, mgt-config]
level: practitioner
status: draft
description: "Create PAN-OS admin accounts and custom admin role profiles with least privilege, including a read-only auditor role."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/firewall-administration/manage-firewall-administrators"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: nobody uses the shared `admin` account day to day; each human or integration gets a named account with just enough privilege.

Built-in roles: superuser, superreader, deviceadmin, devicereader, vsysadmin, vsysreader. Custom Admin Role Profiles restrict WebUI, XML API, REST API and CLI features independently.

```
configure
set mgt-config users alice permissions role-based superreader yes
set mgt-config users alice phash <HASH>
set mgt-config users api-svc permissions role-based custom profile api-readonly-role
commit
```
Generate a hash with `request password-hash password` (it prompts, so the clear text never lands in shell history). Build the custom role in Device > Admin Roles: enable only the WebUI nodes needed and mark the XML API categories Operational Requests and Configuration as read-only for `api-readonly-role`.

Hardening
- Authentication profiles (see the authentication-profile skill) let accounts defer to LDAP/SAML; keep one local break-glass account whose password sits in a vault.
- Password profile: minimum length and expiry (Device > Password Profiles); lockout via Authentication Settings (failed attempts and lockout time).

Gotchas
- A custom role that references a feature your release lacks is silently ignored after upgrade; re-audit roles after major upgrades (confirm).
- API keys inherit the account role: a key for a superuser is a super key. Rotate by regenerating the key and consider the key lifetime setting in Device > Setup > Management.

## Verify
```
show admins all
show admins
```
Log in as the new account and confirm blocked areas are greyed out; check `show log system` for "authenticated for user" entries.
