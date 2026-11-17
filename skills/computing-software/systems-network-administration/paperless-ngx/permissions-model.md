---
id: computing-software.systems-network-administration.paperless-ngx.permissions-model
name: permissions-model
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, permissions, users-groups, superuser, object-permissions, two-factor]
level: practitioner
status: docs-checked
description: "How Paperless-ngx combines global permissions with per-object owner, view and edit rights, plus superusers, admin status and 2FA."
sources:
  - "https://docs.paperless-ngx.com/usage/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Permissions model

## Two layers
- Global permissions determine which parts of the application and API endpoints a user can access (Documents, Tags, Settings and so on).
- Object-level permissions determine which objects are visible or editable. All objects have an owner, and view and edit permissions can be granted to other users or groups.

By default new users are granted no permissions except those inherited from groups they belong to. For objects created via the web UI the default is to set the current user as owner with no extra permissions; you can change this under Settings > Permissions. Documents consumed via the consumption directory have no owner or additional permissions by default, which workflows can control.

## Details that bite
- By default objects are only visible and editable by their owner. Only the object owner can grant permissions to other users or groups.
- Only document owners can create share links and add or remove custom fields.
- For backwards compatibility objects can have no owner, which makes them visible to any user.
- Users without view (or higher) permission see `Private` in place of the object name, for example a tag on a document.
- Object permissions apply to the object itself: permissions on a tag do not affect the documents that have the tag.
- `UISettings`: users accessing the web UI must be granted at least View.
- `AppConfig`: Change or higher grants the Application Configuration area. The page calls it a trusted, admin-level permission; it applies instance-wide and some settings, such as OCR arguments, are passed directly to the underlying processing tools.
- Workflows are global: all users who can access workflows see the same set.
- A user may keep or submit a known related-object ID when editing a document even when that object is displayed as Private.

## Special users
- Superusers can access all parts of the front and back end and all objects. Superuser status can only be granted by another superuser.
- Admin status (Django staff status) grants access to the logs, the system status dialog and the Django backend.

## Two-factor
Users enable 2FA from the My Profile dialog by scanning a QR code with a 2FA app and entering the code. They are then shown 10 recovery codes, which cannot be retrieved again. A superuser can disable 2FA for a user who has lost the device and all recovery codes, from the Users & Groups screen.

## Checked
Date: 2026-11-07
Pages read in full: the whole Permissions section and Two-factor authentication section of usage (lines 374-476), plus the Workflow permissions section; the rest of the usage page was not read for this skill.
Corrections: removed "or a superuser" from who can grant permissions or create share links (the page says only the object owner, and only document owners for share links); scoped the Settings > Permissions defaults to objects created via the web UI; dropped "Workflows" from the global-permission examples (the page lists Documents, Tags, Settings); added the related-object Private note; the AppConfig, UISettings, owner, Private and 2FA claims matched the page.
Method: documentation only; no commands were run.
