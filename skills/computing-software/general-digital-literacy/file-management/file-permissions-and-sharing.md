---
id: computing-software.general-digital-literacy.file-management.file-permissions-and-sharing
name: file-permissions-and-sharing
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-permissions, sharing, shared-folders, read-only, access-control, onedrive-sharing, google-drive-sharing, network-drive, who-can-see-what, link-permissions, inherited-permissions]
level: intro
status: docs-checked
description: "Share a file or folder with exactly the right people and the right access level, and understand read/write permissions well enough to fix 'access denied'."
sources:
  - https://support.google.com/drive/answer/2494822
  - https://support.apple.com/guide/mac-help/change-permissions-for-files-folders-or-disks-mchlp1203/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File permissions and sharing — give access to exactly who should have it

**Goal:** share a file or folder with the right people at the right access level (view
vs edit), understand the basic permission model well enough to diagnose "access denied,"
and avoid the two classic mistakes — sharing too widely, and locking yourself out.

## 1. Two different sharing models
- **Cloud sharing** (Google Drive and similar services): permission belongs to the
  *share*. In Google Drive the roles are Viewer, Commenter and Editor, and general
  access is Restricted (only invited people), Anyone with the link, or Your Organization
  (Workspace accounts).
- **Local file-system permissions** (your computer or a network drive): permission
  belongs to the file or folder itself, per user or group.
Confusing the two is a common cause of "I shared it but they still can't open it": a
cloud share does nothing for a local network-drive folder, and vice versa.

## 2. Cloud sharing in practice (Google Drive)
- Prefer **Restricted** (invited people) over "Anyone with the link" for anything not
  meant to be public: anyone on the internet with the link can open the file.
- Default to **Viewer**; grant **Editor** only when someone must change the file. By
  default Editors can also change permissions and share; you can stop that.
- Access expiration can be set on work or school accounts, within one year; on folders
  it applies only to Viewers. Check your service's help for whether you can use it.
- Check **who has access**: File Information › Details › Manage access, and remove
  people who no longer need it.
- Files inherit their parent folder's sharing, and you cannot give someone less access
  to a file than they have to its folder. To restrict one file, move it to a different
  or limited-access folder.
- Ownership can be transferred to another person; do it before an owner leaves.

## 3. macOS permissions
Select the item in Finder › File › Get Info › expand **Sharing & Permissions**, click
the lock to unlock, pick a user or group and set a privilege: Read & Write, Read only,
Write only (Drop Box) or No Access. For a folder, the Action menu's "Apply to enclosed
items" pushes the change to its contents. On a shared Mac, the administrator can
control permissions for individual users. For Windows and network drives, use your
system's or administrator's documentation.

## Verify
- [ ] You can say which model (cloud share vs file-system permission) governs a given
      shared item before troubleshooting access to it.
- [ ] Sensitive shares are Restricted to named people, not "Anyone with the link."
- [ ] Access lists on your important shared files match who should still have access.

## Checked
2026-11-01. Confirmed from Google Drive Help on sharing (roles, general access options,
inheritance, expiration, Manage access, ownership transfer) and Apple's Mac help on
changing permissions (Get Info, lock, privileges, apply to enclosed items). Removed:
OneDrive and Dropbox claims, Windows Security-tab and change-owner steps, the macOS
"everyone" row and admin-password unlock, and the shared-folder advice.
Method: documentation only; no commands were run.
