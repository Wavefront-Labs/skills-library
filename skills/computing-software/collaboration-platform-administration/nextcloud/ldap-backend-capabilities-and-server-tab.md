---
id: computing-software.collaboration-platform-administration.nextcloud.ldap-backend-capabilities-and-server-tab
name: ldap-backend-capabilities-and-server-tab
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [ldap, active-directory, base-dn, ldaps, server-tab]
level: practitioner
status: docs-checked
description: "Enable the LDAP user and group backend, know what it supports, and fill in the Server tab fields (host, port, system user DN, base DN) correctly."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_user/user_auth_ldap.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: connect Nextcloud to LDAP or Active Directory so those users appear and log in with their directory credentials.

Enable the `LDAP user and group backend` app on the Apps page, then configure it in the admin settings. There are four tabs; a correct Server tab is mandatory before the others open, and a green indicator lights when it is correct.

What it supports: LDAP groups, sharing with users and groups, WebDAV and desktop client access, versioning and external storage, Active Directory with no extra setup including primary groups, auto-detection of attributes such as base DN, email and port, and optionally letting users change their LDAP password. Access is read only: editing or deleting users in LDAP is not supported. You manage group memberships, quotas and sharing permissions like for any other user.

Server tab fields:
- Host: hostname or IP, or an `ldaps://` URI. Adding the port speeds detection (for example `directory.my-company.com:9876`).
- Port: detected automatically for standard ports; enter it manually if detection fails (for example `389`).
- User DN: a user allowed to search the directory. Empty means anonymous access. The docs recommend a dedicated LDAP system user, for example `uid=nextcloudsystemuser,cn=sysusers,dc=my-company,dc=com`.
- Password: for that user; empty for anonymous.
- Base DN: where all users and groups can be reached, for example `dc=my-company,dc=com`. Mandatory, one per line if several.



Check: the Server tab turns green and later tabs become usable.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/configuration_user/user_auth_ldap.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
