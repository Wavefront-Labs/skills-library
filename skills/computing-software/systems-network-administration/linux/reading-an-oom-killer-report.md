---
id: computing-software.systems-network-administration.linux.reading-an-oom-killer-report
name: reading-an-oom-killer-report
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, oom-report, oom-kill-log, oom-killer, dmesg, memory-cgroup, oom-score, out-of-memory]
level: advanced
status: docs-checked
description: "Read an OOM killer report from dmesg/journal: global vs cgroup OOM, the trigger line, Mem-Info, the task table with rss and oom_score_adj, and what to fix next."
sources:
  - https://docs.kernel.org/admin-guide/mm/concepts.html
  - https://www.kernel.org/doc/gorman/html/understand/understand016.html
  - https://docs.kernel.org/admin-guide/cgroup-v2.html
  - https://github.com/torvalds/linux/blob/master/mm/oom_kill.c
  - https://github.com/torvalds/linux/blob/master/mm/memcontrol.c
  - https://github.com/systemd/systemd/blob/main/man/systemd.exec.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading an OOM killer report

## Find it
```bash
journalctl -k -b | grep -iE 'out of memory|oom-kill|invoked oom-killer'
dmesg -T | grep -A60 'invoked oom-killer'      # full report follows the trigger line
```

## Anatomy
1. **Trigger:** `java invoked oom-killer: gfp_mask=0xcc0(GFP_KERNEL), order=0, oom_score_adj=0` — who was
   allocating (not necessarily the culprit).
2. **Context:** `oom-kill:constraint=CONSTRAINT_MEMCG,...,oom_memcg=/system.slice/myapp.service` → a
   **cgroup limit** was hit (MemoryMax / container limit), not host exhaustion; a global OOM prints `,global_oom` instead of `oom_memcg=`. Other constraint values are `CONSTRAINT_NONE`, `CONSTRAINT_CPUSET` and `CONSTRAINT_MEMORY_POLICY`.
3. **Mem-Info:** free/active/inactive/slab/shmem pages, per-zone free and swap figures.
   Large `shmem` → tmpfs/IPC; large unreclaimable slab → see the slab skill.
4. **Task table** ("memory values in pages"): `[ pid ] uid tgid total_vm rss rss_anon rss_file rss_shmem pgtables_bytes swapents oom_score_adj name` — values are in **pages**, not kB.
5. **Verdict:** `Out of memory: Killed process 4211 (java) total-vm:...kB, anon-rss:...kB, file-rss:...kB, shmem-rss:...kB, UID:1001 pgtables:...kB oom_score_adj:0` — for a cgroup OOM the prefix is `Memory cgroup out of memory`.

## Next steps by finding
| Finding | Action |
|---|---|
| CONSTRAINT_MEMCG | raise the unit/container limit or fix the application's memory use |
| One process with huge anon-rss | leak or misconfigured cache; check growth over time |
| Many medium processes | too many workers for the RAM available |
| shmem/tmpfs large | check `/dev/shm`, `/run`, tmpfs mounts |
| Victim was critical (sshd, db) | lower its score with `OOMScoreAdjust=` (range -1000 to 1000), but fix the real consumer |

## Gotchas
- The victim is chosen by a badness heuristic (`oom_badness`), not by who allocated last.
- With systemd-oomd, kills can happen earlier in userspace — look in `journalctl -u systemd-oomd`.

## Verify
- [ ] You can state global vs memcg, the victim's RSS, and the top three RSS consumers at the time.

## Checked

Checked against the Linux kernel source `mm/oom_kill.c` and `mm/memcontrol.c` (torvalds/linux master, latest commit 2026-10-25), `Documentation/filesystems/proc.rst` and the systemd `systemd.exec(5)` source on 2026-10-26. Confirmed from the print statements: trigger line `invoked oom-killer: gfp_mask=..., order=..., oom_score_adj=...`, `oom-kill:constraint=...` with `oom_memcg=` or `global_oom`, constraint names, task-table header and unit (pages), victim line fields including `shmem-rss`, the `Memory cgroup out of memory` prefix for cgroup OOMs, `oom_badness`, `OOMScoreAdjust=` range. Fixed: the task-table header gained `rss_anon rss_file rss_shmem`, and the verdict line gained `shmem-rss`. Removed: the systemd per-unit message text, the order-means-fragmentation claim, earlyoom, application-specific tuning examples.

Method: documentation only; no commands were run.
