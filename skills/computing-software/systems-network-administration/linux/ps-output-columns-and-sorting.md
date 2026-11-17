---
id: computing-software.systems-network-administration.linux.ps-output-columns-and-sorting
name: ps-output-columns-and-sorting
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, ps, ps-options, ps-aux, ps-ef, process-states, process-tree, pstree, top-processes, lpic-1, rhcsa, sysadmin]
level: practitioner
status: verified
description: "Get exactly the process view you need from ps: BSD vs UNIX syntax, custom -o columns, sorting by CPU/memory, process trees, threads, and reading STAT codes."
sources:
  - https://man7.org/linux/man-pages/man1/ps.1.html
  - https://man7.org/linux/man-pages/man1/pstree.1.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# ps: columns, sorting, trees

**Goal:** answer "what is using the CPU/memory, who started it, how long has it run, what
state is it in" from one ps command, also in scripts.

## 1. Two syntaxes
- `ps aux` (BSD, no dash): all processes, user-oriented columns incl. %CPU %MEM VSZ RSS STAT START.
- `ps -ef` (UNIX): all processes, UID PID PPID C STIME TTY TIME CMD — shows the parent.
- `ps -eLf` threads (LWP, NLWP); `ps axjf` / `ps -ejH` / `pstree -p` hierarchy.

## 2. Custom columns (best for scripts)
```bash
ps -eo pid,ppid,user,stat,ni,pcpu,pmem,rss,etime,lstart,cmd --sort=-pcpu | head
ps -eo pid,rss,comm --sort=-rss | head -15       # top memory (RSS in KiB)
ps -o pid=,etimes= -p 1234                       # no header (trailing =), elapsed seconds
ps -C nginx -o pid,cmd                           # by command name
ps -u www-data -o pid,cmd                        # by effective user
ps -p 1234 -o lstart=                            # exact start time
ps -eo pid,wchan:32,cmd | awk '$2!="-"'          # where processes sleep in the kernel
ps -eo pid,cgroup:60,cmd                         # which systemd unit/container owns it
ps -T -p 1234                                    # threads of one process
```
`--sort` accepts `+`/`-` with any column key, several comma-separated (`--sort=-pmem,pid`).

## 3. STAT codes
`R` running/runnable · `S` interruptible sleep · `D` uninterruptible sleep (usually I/O) · `Z` defunct
(zombie) · `T` stopped by a job-control signal · `t` stopped by a debugger during tracing
· `I` idle kernel thread. Modifiers: `<` high priority, `N` low priority (nice), `L` pages locked in memory, `s` session leader, `l`
multithreaded, `+` foreground group.
```bash
ps -eo stat,pid,ppid,cmd | awk '$1 ~ /^D/'      # stuck in I/O
ps -eo stat,pid,ppid,cmd | awk '$1 ~ /^Z/'      # zombies → look at/restart the PPID
```

## 4. Gotchas
- `%CPU` is lifetime average (CPU time / elapsed), not current; use `top`/`pidstat 1` for now.
- `CMD` is truncated to terminal width; add `ww` (`ps auxww`) or `-o args` with wide output.
- `ps aux | grep foo` matches itself; use `pgrep -a foo` or `ps -C foo`.
- `RSS` is the non-swapped physical memory a task has used, in KiB; prefer it to `VSZ` for comparing processes.
- Inside containers, PIDs differ from the host's view.

## Verify
- [ ] Your `--sort=-pcpu` top entry matches what `top` shows over a few seconds.
- [ ] `ps -o pid=` output parses as plain integers in your script.

## Checked

Documentation check. Checked 2026-10-27 against procps-ng ps(1) from the man-pages project (man7.org): `-C` selects by executable name, `-o pid=` header suppression, `etimes` (seconds) and `etime`, `lstart`, `cgroup`, `wchan:N` width syntax, `--sort` with `+`/`-` keys, `-T` and `-L` thread options, the STAT codes including `I` and the extra modifiers, and that `%cpu` is CPU time divided by the process lifetime. Removed the load-average and cannot-be-killed claims for `D` state because the man page does not state them.
Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container (procps 4.0.4): ps aux, -ef, -eLf, axjf headers, custom -o lists with --sort=-pcpu/-rss/-pmem,pid, -o pid=,etimes=, -C, -u, lstart, wchan:32, cgroup:60, -T, STAT Z for a zombie, the grep self-match, pstree. Not run: D and t states, comparison against top.
