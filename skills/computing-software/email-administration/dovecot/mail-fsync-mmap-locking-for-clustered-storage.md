---
id: computing-software.email-administration.dovecot.mail-fsync-mmap-locking-for-clustered-storage
name: mail-fsync-mmap-locking-for-clustered-storage
category: computing-software
field: email-administration
product: dovecot
tags: [mail-fsync, mmap-disable, lock-method, clustered-filesystem, fdatasync, index-files]
level: advanced
status: docs-checked
description: "Tune fsync, mmap and locking for local or clustered filesystems, and why mail_fsync never is dangerous."
sources:
  - https://doc.dovecot.org/main/core/config/mailbox_formats/overview.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default Dovecot calls fsync and fdatasync whenever useful, so that it never reports a message as saved when a power failure a moment later could lose it. People are tempted to set `mail_fsync = never` for speed, but this is dangerous, especially with IMAP, LDA and LMTP. If you must, set it only for services where data loss is acceptable, using a per-service block rather than globally.

Clustered filesystems and NFS: Dovecot does not support any specific clustering solution. The admin must do functional and load testing to prove adequate performance. Everything on the page applies to NFS too, with extra points on the NFS page.

Index mapping: by default index files are mmap()ed. That may not work on some clustered filesystems and certainly not on NFS. `mmap_disable = yes` makes Dovecot do internal caching; even where mmap() works it may not perform better, so benchmark.

Locking: index locks use fcntl by default. Set `lock_method` to `flock` where fcntl is unsupported, or try dotlocks if fcntl causes NFS trouble. Dotlocks are always used for some locks regardless.

Operations advice:
- Run ntpd on each node. Clocks more than a second apart can cause errors when several computers access one mailbox at once.
- Redirect a user to the same server where possible, since the mailbox may be cached in memory and cluster traffic drops. At minimum send connections from one IP to one server.

## Checked
2026-11-09. Read the Dovecot Mailbox Formats overview (main documentation, marked pre-release) in full. Confirmed
each statement: fsync/fdatasync default rationale and `mail_fsync = never` warning with the per-protocol example,
clustered filesystem and NFS notes, mmap and `mmap_disable`, fcntl/flock/dotlock locking and `lock_method`, ntpd, and
same-server redirection. Nothing removed.
Method: documentation only; no commands were run.
