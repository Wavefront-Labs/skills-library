---
id: computing-software.systems-network-administration.bash.named-pipes-mkfifo
name: named-pipes-mkfifo
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, named-pipes, mkfifo, fifo, ipc, pipes, streams, blocking-open, coprocess, tee-fifo, redirection, lpic-1, sysadmin]
level: practitioner
status: gated
description: "Use named pipes (mkfifo) for inter-process streaming: blocking open semantics, holding a FIFO open with a dummy fd, fan-out with tee, and alternatives."
sources:
  - https://man7.org/linux/man-pages/man7/fifo.7.html
  - https://man7.org/linux/man-pages/man1/mkfifo.1.html
  - https://www.gnu.org/software/bash/manual/bash.html#Process-Substitution
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Named pipes — a pipe with a filename

**Goal:** connect two processes that were not started in the same pipeline (different
shells, a daemon and a script, a tool that only accepts a file path) and avoid the
blocking-open deadlocks that make FIFOs feel haunted.

## 1. Create and use
```bash
mkfifo /tmp/myfifo                    # -m 600 to restrict; it is a filesystem object (type p)
ls -l /tmp/myfifo                     # prw-r--r--
# terminal 1
tail -f /var/log/app.log > /tmp/myfifo
# terminal 2
grep ERROR < /tmp/myfifo
```
Data never touches disk; the FIFO is a kernel buffer (default capacity 65,536 bytes with 4 KiB pages, but do not depend on it: pipe(7)) addressed by path.
Readers get EOF when the **last writer** closes.

## 2. Open semantics (the part that bites)
- `open()` for reading **blocks** until a writer opens; for writing blocks until a reader
  opens. A script that does `echo hi > fifo` with no reader hangs forever.
- Writer closes → reader sees EOF → `tail -f ... > fifo` loop ends after the first reader quits.
  Keep it alive by holding a dummy fd: `exec 3<>/tmp/myfifo` (read-write open never blocks
  on Linux) — then readers can come and go.
- A write-only `O_NONBLOCK` open fails with ENXIO when there is no reader (fifo(7); tested with `dd of=fifo oflag=nonblock`: "No such device or address").
- Opening a FIFO read-write is allowed on Linux but undefined by POSIX (fifo(7)); the `exec 3<>fifo` trick is Linux-flavoured (it also worked on the MSYS bash tested here).
- Multiple writers: writes ≤ PIPE_BUF (4096) are atomic; larger ones may interleave.

## 3. Patterns
```bash
# feed a tool that insists on a filename, without a temp file
mkfifo /tmp/dump.fifo
mysqldump db > /tmp/dump.fifo &  gzip < /tmp/dump.fifo > db.sql.gz; rm /tmp/dump.fifo

# fan-out one stream to two consumers
mkfifo /tmp/a /tmp/b
cat big.log | tee /tmp/a > /tmp/b &
grep ERROR /tmp/a > errors.txt &  wc -l /tmp/b > count.txt; wait

# a long-lived command queue
mkfifo /run/app/cmd; exec 3<>/run/app/cmd
while read -r line <&3; do handle "$line"; done &   # writers: echo start > /run/app/cmd
```

## 4. Process substitution is usually enough
`diff <(sort a) <(sort b)` and `cmd > >(logger -t app)` create anonymous FIFOs
(`/dev/fd/63`) that bash manages for you — same mechanism without the file, the cleanup or
the blocking surprises. Reach for `mkfifo` only when processes are started independently
or the path must be stable.

## 5. Cleanup and permissions
- FIFOs persist until `rm`; stale ones in `/tmp` from crashed scripts are common — create
  under `mktemp -d` and `trap 'rm -rf "$tmp"' EXIT`.
- Place shared FIFOs in a directory such as `/run/<app>/` with owner/group restricting
  who can write commands into your daemon (gated: unconfirmed, source is paywalled or blocked).
- SELinux: confined daemons may need policy permissions on FIFOs; check the audit log for AVC denials (gated: unconfirmed, source is paywalled or blocked).

## Failure modes
- Script hangs at `> fifo`: no reader yet; start the reader first or hold `exec 3<>`.
- Reader exits immediately with no data: writer had not opened yet and a previous writer's
  EOF was delivered; use the dummy fd trick.
- "Interrupted system call"/partial lines with several writers: messages over PIPE_BUF.
- `cp`/`cat` of a FIFO blocks backups: exclude `-type p` in backup finds; `tar` stores FIFOs
  as special files without reading them (tested: `tar -tv` shows a `p` entry of size 0).

## Verify
- [ ] `stat -c %F /tmp/myfifo` prints `fifo`.
- [ ] With `exec 3<>fifo` held, `echo x > fifo` returns immediately and `read -t1 l < fifo` gets `x`.
