---
id: computing-software.collaboration-platform-administration.nextcloud.enable-sse-and-team-folder-encryption
name: enable-sse-and-team-folder-encryption
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [encryption-enable, default-encryption-module, groupfolders, external-mount, occ-encryption]
level: advanced
status: docs-checked
description: "Enable Nextcloud server-side encryption step by step, extend it to external mounts and team folders, and use the occ encryption commands."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/encryption_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: turn on server-side encryption after reading the limits and choosing a key mode.

Steps in the web interface:
1. Open the *Server-side encryption* section of the admin page.
2. Check *Enable server-side encryption*.
3. A message says "No encryption module loaded." Go to the Apps page and enable the Nextcloud Default Encryption Module.
4. Return to the admin page; the module appears and is auto-selected.
5. Log out and in again to initialise your encryption keys.
6. Optional: uncheck the box for encrypting home storage to leave local files unencrypted.

External mountpoints: you and your users can encrypt them. Set the encryption option in the mount configuration of each external storage.

Team Folders:

```
occ config:app:set groupfolders enable_encryption --value=true
```

Only new or updated files in team folders are encrypted afterwards.

Useful commands:
- `occ encryption:status` shows the status and module
- `occ encryption:enable` enables server-side encryption
- `occ encryption:list-modules` lists available modules
- `occ encryption:set-default-module [Module ID]` selects the default module

Back up the key directories (`data/<user>/files_encryption` and `data/files_encryption`) before and after enabling.

Related reading: sse-limitations-and-key-loss-risks and sse-key-management-modes. Enabling is hard to undo from the web interface.

Check: `occ encryption:status` reports encryption enabled with the default module loaded.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/encryption_configuration.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
