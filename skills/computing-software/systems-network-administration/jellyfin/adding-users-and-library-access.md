---
id: computing-software.systems-network-administration.jellyfin.adding-users-and-library-access
name: adding-users-and-library-access
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, users, dashboard, library-access, device-access, new-user]
level: intro
status: docs-checked
description: "Create Jellyfin users in the Dashboard and limit them to specific libraries and devices."
sources: ["https://jellyfin.org/docs/general/server/users/adding-managing-users/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Adding users and restricting libraries

User management is under `Users` in the Dashboard.

**Add a user.** Click `+` at the top. Enter the name as shown on, or typed into, the login screen.

**Library access.** By default `Enable access to all libraries` is on. Turn it off to grant access per library (a library can contain several folders). Users who did not have access to all libraries do not get rights to libraries added later; you must grant them by editing the user.

**Device access.** `Enable access from all devices` is on by default. Turn it off to grant access per device; logins from new devices are blocked until approved there.

**Managing existing users.** Click a portrait for the `Profile` tab, or use the `...` menu with `Open`, `Library access`, `Parental control` and `delete`. They are tabs on one page, plus a `Password` tab. Changes on any tab need `Save` at the bottom.

**Authentication provider.** `default` means Jellyfin handles login. The only other documented option is LDAP via the LDAP-Auth plugin; if you switch an existing user to LDAP, the username must match the LDAP UID including capitalisation.

## Checked

2026-11-03. Confirmed against the Jellyfin Managing Users page: add-user flow, Enable access to all libraries and all devices behaviour, tabs and Save, authentication provider and LDAP-Auth UID rule. Removed: unsupported display claim and the invented check step.

Method: documentation only; no commands were run.
