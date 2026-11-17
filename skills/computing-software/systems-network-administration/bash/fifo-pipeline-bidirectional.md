---
id: computing-software.systems-network-administration.bash.fifo-pipeline-bidirectional
name: fifo-pipeline-bidirectional
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, fifo-pipeline-bidirectional, fifo-two-way, shell-scripting]
level: advanced
status: docs-checked
description: "Build two-way communication in bash using a pair of named pipes (mkfifo) for client-server scripts, with open order and cleanup."
sources:
  - https://man7.org/linux/man-pages/man7/fifo.7.html
  - https://man7.org/linux/man-pages/man7/pipe.7.html
  - https://www.gnu.org/software/coreutils/manual/html_node/mktemp-invocation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Two-way communication with fifos
**Goal:** request/response between two shell processes.
```bash
d=$(mktemp -d); mkfifo "$d/req" "$d/resp"; trap 'rm -rf "$d"' EXIT
( while read -r line < "$d/req"; do echo "echo: $line" > "$d/resp"; done ) &
echo hello > "$d/req"
read -r reply < "$d/resp"; echo "$reply"      # echo: hello
exec 3<>"$d/req"                               # open read/write
```
- Normally, opening a FIFO blocks until the other end is opened too; the FIFO must be open at both ends before data passes.
- Under Linux, opening a FIFO for read and write succeeds in both blocking and nonblocking mode (POSIX leaves this undefined). A process using both ends to talk to itself must take care to avoid deadlocks.
- In nonblocking mode, opening read-only succeeds with no writer, and opening write-only fails with ENXIO unless the other end is already open.
- Writing to a FIFO that is not open for reading on the other side sends the writer SIGPIPE.
- Per pipe(7), writes of PIPE_BUF bytes or fewer to a pipe are atomic; larger writes may be interleaved with other writers. On Linux PIPE_BUF is 4096 bytes.
- Create the directory with `mktemp -d` (the directory is accessible only to the current user, subject to umask) and remove the FIFOs when done.
- Self-check: the client prints the echoed line and no process remains afterwards.

## Checked
2026-11-09. Confirmed in fifo(7) (blocking open, nonblocking open, Linux read/write open, SIGPIPE) and pipe(7) (PIPE_BUF atomicity, 4096 on Linux), and in the mktemp page (directory permissions). Removed: the claim that readers get EOF when all writers close (not confirmed on the cited pages) and the long-lived-server fd advice that rested on it.
Method: documentation only; no commands were run.
