---
id: computing-software.cloud-infrastructure-engineering.harbor.database-authentication-mode
name: database-authentication-mode
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [database-auth, self-registration, auth-mode, local-users, harbor]
level: intro
status: docs-checked
description: "Use Harbor database authentication, optionally allow self-registration, and avoid locking yourself out of switching auth modes."
sources:
  - https://goharbor.io/docs/main/administration/configure-authentication/db-auth/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In database authentication mode user accounts live in the Harbor local database. By default only the Harbor system administrator creates accounts.

To configure it:
1. Log in as a system administrator.
2. Under Administration, Configuration, open the **Authentication** tab.
3. Leave **Auth Mode** on the default **Database** option.
4. Optionally tick **Allow Self-Registration**.

Self-registration is deactivated by default. When enabled, unregistered users can click **Sign up for an account** on the login page and create their own account.

The key gotcha: once you create users in the database, Harbor is locked into database mode. You cannot change to a different authentication mode after local users exist. Decide on LDAP or OIDC before adding any user other than `admin`. The LDAP page states the same rule from the other side: switching from database to LDAP is only possible if no user other than `admin` is in the database.

Creating users in this mode is a separate administrator task, covered in the page on creating user accounts in database mode. In LDAP mode, self-registration, user creation and password changes are not available in Harbor, because identities are managed by the external directory.

## Checked

2026-11-03. The menu path, default Database mode, self-registration default and the lock-in rule were read against the Harbor docs page for database authentication; the LDAP-mode statements against the LDAP/AD authentication page. Nothing removed.

Method: documentation only; no commands were run.
