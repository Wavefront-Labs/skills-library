---
id: computing-software.systems-network-administration.apache-guacamole.user-and-group-management
name: user-and-group-management
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, user-management, user-groups, permissions, login-disabled, password-expiry, group-membership, administration]
level: practitioner
status: docs-checked
description: "Manage Guacamole users and groups in the admin UI: passwords, expiry, admin rights, Login disabled, group nesting and inheritance."
sources:
  - https://guacamole.apache.org/doc/gug/administration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Users and user groups

Settings, Users / Groups (database extensions only).

Users:
- **New User**: username and password. A new user has no access to existing connections and no admin rights until you grant them, and cannot log in until a password is set.
- Edit a user to change the password, expire it (forcing a change at next login), add or remove administrative permissions, and add or remove read access to connections, sharing profiles and groups.
- **Login disabled** rejects sign-in as if the account did not exist, without deleting it; **Delete** (if you hold delete permission) removes the account permanently.
- Edit group membership from the user screen (Groups section; the X removes, saved with the user).

User groups:
- **New Group**: set members and permissions; **Disabled** suspends the group's effects without deleting it.
- Groups may contain users and groups: the editor has parent groups, member groups and member users. How permissions inherit is up to the extension providing the group; the database extension inherits recursively, to all nested descendants.

New connections are usable only by administrators (and the creating user) until access is granted by editing a user or a group the user belongs to.

Prefer granting through groups: one place to audit.

Verify: log in as a non-admin member of a group and confirm only the intended connections appear.

## Checked

2026-11-08. Read the whole of the administrative interface chapter (administration.html) and confirmed new-user defaults, password expiry, Login disabled versus Delete, group Disabled, group nesting and recursive inheritance in the database extension, and new-object visibility. Removed claims not on the cited page: LDAP/SSO name matching and case-sensitivity, TOTP per-user disabling from 1.6.0, and the user-password-* property rules, plus the cross-references built on them.
Method: documentation only; no commands were run.
