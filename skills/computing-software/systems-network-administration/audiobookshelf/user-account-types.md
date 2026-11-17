---
id: computing-software.systems-network-administration.audiobookshelf.user-account-types
name: user-account-types
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [users, root, admin, guest, permissions, accounts]
level: intro
status: docs-checked
description: "Pick the right Audiobookshelf account type (Root, Admin, User, Guest) and know the default permissions and account-sharing caveat."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/user-management.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/faq/server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
There are four account types:

- **Root** - the original admin account created for the server. Same as Admin, but Admins cannot edit it.
- **Admin** - can access and modify server settings.
- **User** - normal user.
- **Guest** - same as User, but cannot change their own password.

Admins create users in server settings. By default, user and guest accounts get access to all non-explicit content in all libraries, and any permission granted applies to all media and libraries that user can access. Admin accounts get all permissions by default.

You can disable a user to keep the account but block authentication.

Account sharing is not an intended or supported use case: listening to different media at the same time from the same account can cause problems.

There is no default username or password. You create the root user the first time you visit the server in a browser.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: User Management page and FAQ server page (default admin).

Method: documentation only; no commands were run.
