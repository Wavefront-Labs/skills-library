---
id: computing-software.cybersecurity-defensive.nessus.nessus-manager-user-management
name: nessus-manager-user-management
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, nessus-user-management, nessus-manager, rbac, user-roles, nessuscli, nessus-deployment]
level: practitioner
status: draft
description: "Manage Nessus Manager / Nessus Professional users, roles (Basic, Standard, Administrator, System Administrator), groups, scan sharing and LDAP/SAML login."
sources: ["https://docs.tenable.com/nessus/Content/Users.htm", "https://docs.tenable.com/nessus/Content/UserRoles.htm", "https://docs.tenable.com/nessus/Content/Groups.htm"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Nessus user accounts and roles

Nessus Professional is single-user oriented (multiple accounts allowed, no sharing model);
Nessus Manager supports full multi-user management. Large teams should use Tenable VM or
Tenable Security Center instead.

## Roles (Nessus Manager)
- **Basic**: read scan results shared with them.
- **Standard**: create scans, policies, user audit files; use shared resources.
- **Administrator**: Standard plus manage users, groups, agents; cannot change system settings.
- **System Administrator**: everything, including scanners, updates, licensing.
- **Disabled**: account kept for audit but cannot log in.

## Create and manage
- UI: Settings > Accounts > Users > New User; Groups for sharing scans/policies.
- CLI: `nessuscli adduser <name>` (prompts for password and admin flag), `nessuscli rmuser <name>`,
  `nessuscli chpasswd <name>`, `nessuscli lsuser`.
- API: `POST /users` with `permissions` (16 Basic, 32 Standard, 64 Administrator, 128 System Administrator).

## Sharing
Scans and policies are shared to users/groups with permission levels (Can View, Can Control, Can
Configure). Credentials embedded in shared policies can be used but not viewed. Prefer managed
credentials where available.

## Authentication
- LDAP (Settings > LDAP Server) to authenticate users against AD; accounts must still exist locally
  with matching username (or auto-created on first login when configured).
- SAML for Nessus Manager on recent versions; keep a local System Administrator for break-glass.
- Password policy: `nessuscli fix --set password_complexity=yes`, `login_banner`, account lockout
  via `max_login_attempts`.

## Gotchas
- Deleting a user deletes their scans unless reassigned first; disable instead.
- API keys are per user; rotate them when staff leave (Settings > My Account > API Keys).

## Verify
`nessuscli lsuser` matches the access list; a Standard test user cannot open Settings > Advanced.
