---
id: computing-software.systems-network-administration.audiobookshelf.user-access-control-libraries-tags
name: user-access-control-libraries-tags
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [users, access-control, tags, libraries, invert, performance]
level: advanced
status: docs-checked
description: "Limit an Audiobookshelf user by library and by tags, including the Invert toggle and its performance cost on large libraries."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/user-management.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
User access can be limited two ways: by **library** and by **tags**.

Tag rules:

- Give a user access to only certain tags, or to everything except certain tags.
- The `Invert` toggle switches between `Tags Accessible to User` and `Tags not Accessible to User`.
- Tag access control applies to all libraries the user can access.

Example: tag restricted material `adult` and set the child's account to Invert with `adult` listed, which grants everything except that tag.

Performance caveat from the docs: because of the existing data model, users with tag-based access control may experience performance issues with larger libraries. Prefer library-level limits when they are enough.

By default, users and guests can access all non-explicit content in all libraries, so access limits are an opt-in restriction you add per user.

## Checked

Method: docs-checked 2026-11-09 against the User Management page of the Audiobookshelf docs repo, read in full from raw markdown. The `adult` tag example is an illustration, not page text.
