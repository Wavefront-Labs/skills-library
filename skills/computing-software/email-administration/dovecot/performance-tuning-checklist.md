---
id: computing-software.email-administration.dovecot.performance-tuning-checklist
name: performance-tuning-checklist
category: computing-software
field: email-administration
product: dovecot
tags: [optimization, mailbox-list-index, auth-cache-size, service-restart-request-count, process-min-avail, tz-environment]
level: practitioner
status: docs-checked
description: "Reduce disk I/O and CPU in Dovecot with the TZ variable, list index, auth cache, process reuse and hibernate settings."
sources:
  - https://doc.dovecot.org/main/core/config/optimization.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Busy IMAP and POP3 servers are usually bound by disk I/O, not CPU, so cutting I/O is the best first step. The page offers these measures:

- TZ: glibc stats /etc/localtime on every localtime() call unless `TZ` is set. Set `TZ=:/etc/localtime` (note the colon) for the process, in the shell or Dovecot config. A restart is required, not a reload.
- `mailbox_list_index = yes` answers STATUS-style lookups from one index; it is already the default. `mailbox_list_index_very_dirty_syncs = yes` assumes the index is current.
- `mail_prefetch_count` can help with some formats.
- `mail_volatile_path` moves lock files to a local directory, especially useful if mail lives on NFS.
- With the ACL plugin and only global ACLs, set `acl_globals_only = yes`.
- `auth_cache_size` caches passdb and userdb lookups. `auth_cache_verify_password_with_worker = yes` spreads hash calculation across CPU cores through auth workers.
- Where a service has `client_limit` and `process_limit` above 1, set `process_min_avail` to the CPU core count.
- Raise `service_restart_request_count` from 1 to something like 100 for imap and pop3 to reuse processes; avoid very high or unlimited values because users differ in memory use.
- `imap_hibernate_timeout` moves idle IMAP connections to a shared imap-hibernate process, freeing memory.
- Use `pop3_no_flag_updates = yes` for POP3.

`vsz_limit`, `process_limit` and `client_limit` do not directly change memory use; they guard against leaks and DoS. For glibc, `import_environment` defaults to an mmap threshold of 128 kB since 2.4.1 so memory returns to the OS.

## Checked

2026-11-03. Confirmed on the Dovecot Optimizations page: TZ=:/etc/localtime (restart, not reload), disk I/O first, mailbox_list_index (default) and very_dirty_syncs, mail_prefetch_count, mail_volatile_path, acl_globals_only, auth_cache_size and auth_cache_verify_password_with_worker, process_min_avail equal to CPU cores, service_restart_request_count 1 to about 100 with the memory caveat, imap_hibernate_timeout, pop3_no_flag_updates, the vsz_limit/process_limit/client_limit notes and the 128 kB mmap threshold default (changed 2.4.1). Nothing removed.

Method: documentation only; no commands were run.
