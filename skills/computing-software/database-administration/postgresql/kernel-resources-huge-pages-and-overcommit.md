---
id: computing-software.database-administration.postgresql.kernel-resources-huge-pages-and-overcommit
name: kernel-resources-huge-pages-and-overcommit
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, kernel-resources, huge-pages, vm-overcommit-postgres, oom-killer, overcommit-memory, shared-memory, sysctl, linux, postgres-server-setup]
level: advanced
status: docs-checked
description: "Configure Linux huge pages, memory overcommit and OOM-killer protection for a PostgreSQL host so large shared_buffers work and the postmaster is never killed."
sources:
  - https://www.postgresql.org/docs/18/kernel-resources.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kernel resources: huge pages, overcommit, OOM

**Goal:** a host where `shared_buffers` sits in huge pages and a memory spike
fails one query with an error instead of the OOM killer taking out the postmaster.

## Huge pages
The docs say huge pages reduce overhead when using large contiguous chunks of memory, as PostgreSQL
does, particularly with large `shared_buffers`. The kernel must provide them (`CONFIG_HUGETLBFS=y`, `CONFIG_HUGETLB_PAGE=y`).

1. Ask the server how many it needs (the server can be stopped):
   ```bash
   postgres -D <datadir> -C shared_memory_size_in_huge_pages
   ```
2. Reserve them (a larger setting is appropriate if other programs need huge pages) and persist the setting:
   ```bash
   sysctl -w vm.nr_hugepages=<COUNT_FROM_STEP_1>
   grep ^Hugepagesize /proc/meminfo
   ```
   Add the setting to `/etc/sysctl.conf` so it is reapplied after reboots. The kernel may be unable to allocate them immediately because of fragmentation; repeat or reboot. The server's OS user may also need `vm.hugetlb_shm_group` and/or `ulimit -l`. `huge_page_size` selects 2MB or 1GB pages.
3. In postgresql.conf: `huge_pages = on` (the server fails to start if not enough huge pages are available) rather than
   the default `try` (falls back to normal pages). Restart.

## Overcommit and the OOM killer
- Set `vm.overcommit_memory = 2` with `vm.overcommit_ratio` sized so
  `CommitLimit` (in /proc/meminfo) covers RAM the DB may use; allocations then
  fail with `out of memory` in one backend rather than invoking the OOM killer.
  Only do this on a dedicated DB host; other software may not cope.
- With or without that, protect the postmaster: as root, in the startup script just before
  invoking postgres, run `echo -1000 > /proc/self/oom_score_adj` and also
  `export PG_OOM_ADJUST_FILE=/proc/self/oom_score_adj PG_OOM_ADJUST_VALUE=0` so child
  processes run with the normal score of zero (if `PG_OOM_ADJUST_FILE` is not set the children keep the postmaster's setting, which the docs call unwise).
- If a child process is killed, PostgreSQL typically terminates all remaining connections and
  recovers automatically if `restart_after_crash` is enabled, otherwise it shuts down.
- Other mitigations in the docs: lower `shared_buffers`, `work_mem` and `hash_mem_multiplier`, reduce `max_connections` and use a connection pooler, or add swap.

## Gotchas
- With `huge_pages = try` and too small a reservation, PostgreSQL falls back to normal pages;
  `huge_pages_status` shows whether huge pages were actually obtained.
- `work_mem` is per sort/hash node per backend; RAM sizing must include
  `max_connections x work_mem x nodes`, the usual OOM cause.

## Verify
- `SHOW huge_pages_status;` is `on`.
- The postmaster's `/proc/<pid>/oom_score_adj` is `-1000` and a backend's is `0` after the startup-script change.

## Checked
2026-10-25. Against PostgreSQL 18 documentation (REL_18_STABLE doc/src/sgml, branch head 2026-10-24; PostgreSQL 19 is still at release-candidate stage): Linux Huge Pages section (kernel options, `postgres -C shared_memory_size_in_huge_pages`, `vm.nr_hugepages`, `/etc/sysctl.conf`, fragmentation, `vm.hugetlb_shm_group` and `ulimit -l`, default fallback behaviour and `huge_pages = on`), `huge_pages` and `huge_pages_status` parameters, and Linux Memory Overcommit section (OOM killer behaviour, `vm.overcommit_memory=2` and `vm.overcommit_ratio`, `/proc/self/oom_score_adj`, `PG_OOM_ADJUST_FILE` and `PG_OOM_ADJUST_VALUE`, other mitigations). Removed the page-table size estimate, the `PG15+`/`PG17+` version gates, the transparent-huge-pages advice, the systemd `OOMScoreAdjust` line and the claim about reserved huge pages, which the documentation does not give; dropped the kernel.org source, which was not consulted.
Method: documentation only; no commands were run.
