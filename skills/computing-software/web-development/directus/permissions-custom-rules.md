---
id: computing-software.web-development.directus.permissions-custom-rules
name: permissions-custom-rules
category: computing-software
field: web-development
product: directus
tags: [permissions, custom-permissions, field-presets, item-permissions]
level: practitioner
status: docs-checked
description: "Set Directus permissions per collection and action with item filters, field lists, validation and presets, and handle the null-on-restricted-field behaviour."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/03.auth/2.access-control.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A permission is set on a collection and one action: create, read, update, delete or share. Each is all, none, or custom.

Custom permissions have four parts:
- **Item permissions**: filter rules choose which items, e.g. update only where `user_created` equals the current user.
- **Field permissions**: which fields; different per action.
- **Field validation**: filter rules checked on create/update.
- **Field presets**: default values on create/update, shown on the item page and editable later.

Structure: users get policies (directly or through roles); policies hold permissions. A user starts with no permissions.

Gotcha: via the API only permitted fields are returned. If several permissions allow different access to the same field, a disallowed context returns it as `null`. Treat `null` as both a value and a sign of restriction.

Access Control is in the Settings module.

## Checked

2026-11-04: confirmed against the Directus docs Access Control page: actions, all/none/custom, four custom permission parts, policies, no permissions by default, conflicting-permissions null callout. Removed the invented click path (the page only says Access Control is in Settings) and the verify line.

Method: documentation only; no commands were run.
