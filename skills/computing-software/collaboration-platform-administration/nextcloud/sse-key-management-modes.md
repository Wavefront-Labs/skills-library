---
id: computing-software.collaboration-platform-administration.nextcloud.sse-key-management-modes
name: sse-key-management-modes
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [master-key, user-keys, recovery-key, encryption-disable-master-key, occ]
level: advanced
status: draft
description: "Pick master key or user key mode for Nextcloud server-side encryption, understand recovery keys and password loss, and switch mode before enabling."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/encryption_configuration.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: choose the key mode once, before encryption is enabled.

Master key mode (default, recommended for most deployments):
- All files are encrypted with one central server-controlled key.
- Admins can decrypt any user's files.
- Recovery keys are not available in this mode, and not needed: files stay accessible if a user forgets their password, since they are not encrypted with it.

User key mode:
- Each user's files use a key protected by their password.
- Admins cannot readily decrypt without the user's password, unless a recovery key is defined.
- If a user forgets the password and no recovery key exists, the files are lost.
- It does not work with every authentication method (for example app passwords or single sign-on) and is recommended only for compatibility with older setups.

How to choose (from the docs):
- If you trust your server administrators, use master key mode.
- If admins must not access files, use E2EE rather than SSE.
- User key mode gives some protection against malicious admins but has limitations.

To select user key mode, run this before enabling encryption:

```
occ encryption:disable-master-key
```

Back up keys: per-user keys live in `data/<user>/files_encryption` and system-wide or external storage keys in `data/files_encryption`.

Check: `occ encryption:status` shows the module and mode you intended before any user files are encrypted.
