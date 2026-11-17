---
id: computing-software.database-administration.memcached.admin-runtime-commands
name: admin-runtime-commands
category: computing-software
field: database-administration
product: memcached
tags: [cache-memlimit, shutdown, verbosity, version, runtime-config]
level: practitioner
status: docs-checked
description: "Adjust memcached without restart: cache_memlimit, verbosity, version and the optional shutdown command (-A)."
sources:
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

- `cache_memlimit <MB>`: change the memory limit at runtime. The argument is in megabytes, not bytes. Replies `OK` or an error (nothing with `noreply` as the last parameter). If the new limit is higher, the server may start requesting more memory from the OS. If it is lower and slabs_reassign plus automove are enabled, free memory may be released back to the OS asynchronously.
- `verbosity <n>`: set the verbosity of the logging output; always succeeds and replies `OK`.
- `version`: replies `VERSION <version>`.
- `shutdown [graceful]`: disabled by default; enable with the `-A`/`--enable-shutdown` flag. Plain `shutdown` raises SIGINT; `shutdown graceful` raises SIGUSR1 for a graceful shutdown.
- `quit`: the server closes the connection (the client may also just close it).
- `flush_all [delay]`: invalidate all items immediately or after the delay; replies `OK`.

`stats settings` reports `shutdown_command` (yes/no) and `maxbytes`.

## Checked

2026-11-04. Confirmed against protocol.txt "Other commands" (cache_memlimit, shutdown, version, verbosity, quit, flush_all) and the settings statistics table. Removed: the unstated "used with warm restart" remark, the Verify line and the Security paragraph.

Method: documentation only; no commands were run.
