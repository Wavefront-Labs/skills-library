---
id: computing-software.email-administration.dovecot.nfs-single-backend-rules-and-mount-options
name: nfs-single-backend-rules-and-mount-options
category: computing-software
field: email-administration
product: dovecot
tags: [nfs, mail-nfs-index, actimeo, nolock, mail-volatile-path, mdbox-purge]
level: advanced
status: docs-checked
description: "Run Dovecot on NFS safely: one backend per user, LMTP delivery, leave mail_nfs options off, mount options and fast index storage."
sources:
  - https://doc.dovecot.org/main/core/config/nfs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dovecot works on NFS but does not support different servers accessing the same user at once; this means more or less severe corruption, and applies to delivery too.

Rules:
- Assign users to specific backends in the proxy's passdb lookups.
- Deliver mail via the LMTP server.
- Set `mmap_disable = yes` and `mail_fsync = always`.
- Keep `mail_nfs_index` and `mail_nfs_storage` at `no`.
- Do not use the quota-status service.
- The unmounted mount-point directory must not be writable by the mail processes (often the vmail user). Otherwise a missing mount lets a new empty user directory be created, which breaks things.

Mount options:
- `actimeo`: caching control; at least 60 seconds is advised (`actimeo=60`).
- `nordirplus`: Dovecot does not need readdirplus, which can slow servers.
- `noatime`: not needed.
- `root_squash`: Dovecot does not care.
- `nolock` or `local_lock=all`: slightly unsafe but fine if each user is only accessed by one server, since each user locks only their own files. If one user is accessed twice, corruption is more likely, though not for mail if indexes and mail are on separate mounts.

Other tips: mdbox is likely more efficient than sdbox but needs periodic `doveadm purge` through a doveadm proxy so it runs on the right backend. Keep lock files in tmpfs with `mail_volatile_path`. Use `mailbox_list_index_prefix` for fast index storage with `mailbox_list_iter_from_index_dir = yes`. Run ntpd everywhere; clock skew above one second causes errors.

## Checked

2026-11-03. Confirmed on the NFS page: no simultaneous access to a user from different servers (including delivery), proxy passdb assignment, LMTP delivery, mail_nfs_index/mail_nfs_storage kept off, no quota-status, unmounted mount point not writable, the actimeo (at least 60 s), nordirplus, noatime, root_squash and nolock/local_lock=all notes, the mdbox purge via doveadm proxy, mail_volatile_path, mailbox_list_index_prefix with mailbox_list_iter_from_index_dir, and ntpd with the one-second skew limit. Added the page's mmap_disable and mail_fsync rules.

Method: documentation only; no commands were run.
