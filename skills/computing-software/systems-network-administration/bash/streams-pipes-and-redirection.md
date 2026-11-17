---
id: computing-software.systems-network-administration.bash.streams-pipes-and-redirection
name: streams-pipes-and-redirection
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, shell, redirection, pipes, stdout, stderr, stdin, streams, file-descriptors, tee, xargs, here-doc, here-string, process-substitution, pipefail, noclobber, exec-redirect, dev-null, buffering, stdbuf, pipestatus, lpic-1, linux]
level: intro
status: gated
description: "Use Unix streams correctly in bash: fd numbers, redirection order (2>&1 placement), tee, here-docs, process substitution, exec-level redirects, PIPESTATUS, noclobber and the buffering trap."
sources:
  - https://www.gnu.org/software/bash/manual/html_node/Redirections.html
  - https://mywiki.wooledge.org/BashGuide/InputAndOutput
  - https://man7.org/linux/man-pages/man1/stdbuf.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Streams, pipes and redirection — plumbing commands together without losing output

**Goal:** send each command's output exactly where you intend (file, next command,
log, nowhere), capture errors separately, and read why `2>&1 >file` did not do what you
thought.

## 1. The three streams and the fd numbers
Every process starts with fd 0 (stdin), 1 (stdout), 2 (stderr). Redirection operators
act on fds; the shell applies them **left to right, before the command runs**:
```bash
cmd > out.txt            # fd1 → file (truncate);  >> appends
cmd 2> err.txt           # fd2 → file
cmd > out.txt 2>&1       # fd1 → file, THEN fd2 → wherever fd1 points now (the file)  ✔
cmd 2>&1 > out.txt       # fd2 → terminal (fd1's current target), THEN fd1 → file    ✘ errors still on screen
cmd &> all.txt           # bash shorthand for > all.txt 2>&1   (&>> appends)
cmd < in.txt             # fd0 ← file
cmd 2>/dev/null          # discard errors; > /dev/null 2>&1 discards everything
cmd > /dev/null          # keep errors visible, drop normal output
```
`2>&1` means "make fd2 a copy of fd1 *as it is right now*", which is why order matters.
`>&2` inside a script writes to stderr: `echo "usage: ..." >&2`. Messages for humans go
to stderr; data for the next program goes to stdout — a tool that mixes them cannot be
piped.

## 2. Pipes
`a | b` connects a's stdout to b's stdin; stderr of `a` still goes to the terminal.
`a 2>&1 | b` or `a |& b` pipes both. Each side runs in its own subshell: variables set
inside `while read` in a pipeline vanish afterwards —
```bash
count=0; cat f | while read -r l; do count=$((count+1)); done; echo "$count"   # 0 !
count=0; while read -r l; do count=$((count+1)); done < f; echo "$count"       # works
# or: shopt -s lastpipe (non-interactive) ; or mapfile -t lines < f
```
Exit status of a pipeline is the **last** command's; `set -o pipefail` makes it the
rightmost non-zero one, and `${PIPESTATUS[@]}` holds every status right after the
pipeline (`PIPESTATUS` is overwritten by the next command, copy it immediately).

`tee` writes to a file *and* stdout: `make 2>&1 | tee build.log`, `tee -a` appends,
`cmd | tee >(gzip > out.gz) | wc -l` fans out. Writing to a root-owned file:
`echo x | sudo tee /etc/f >/dev/null` (`sudo echo x > /etc/f` fails because the
redirection is done by your non-root shell).

`xargs` turns stdin into arguments: `find . -name '*.log' -print0 | xargs -0 rm --`;
`-n1`/`-P4` for one-per-call/parallel; `-I{}` placeholder; `-r` (GNU) skip if empty.

## 3. Feeding stdin: here-docs, here-strings, process substitution
```bash
cat <<'EOF' > /etc/motd        # quoted 'EOF' = no expansion; unquoted EOF expands $vars
Welcome, $USER is NOT expanded here
EOF
cat <<-EOF                      # <<- strips leading TABS (not spaces) for indented scripts
	indented
	EOF
grep foo <<< "$var"             # here-string: a variable as stdin (adds trailing newline)
diff <(sort a) <(sort b)        # process substitution: a command's output as a filename (/dev/fd/N)
cmd > >(logger -t cmd) 2>&1     # send output into a process instead of a file
```
Process substitution needs bash (not `sh`) and `/dev/fd`; it is what you use when a
tool insists on a file argument.

## 4. Extra fds and `exec`
```bash
exec > >(tee -a run.log) 2>&1   # from here on, everything this script prints is logged
exec 3>&1                        # save stdout as fd3
exec 1>out.txt                   # redirect the rest of the script's stdout
echo "still to terminal" >&3
exec 1>&3 3>&-                   # restore and close fd3
exec 3< input.txt; read -r first <&3; exec 3<&-     # read a file line by line across commands
exec {fd}>lockfile; flock -n "$fd" || exit 1        # bash ≥ 4.1 picks a free fd
```
Open fds inherit to children — a daemon started from a script with a redirected fd 3
keeps your log file open forever; close what you do not need (`3>&-`).
Redirecting a whole block: `{ cmd1; cmd2; } > out.txt 2>&1` or `( ... )` in a subshell;
loops take redirections too: `while ...; do ...; done < file > out`.

## 5. Safety switches
- `set -o noclobber` (`set -C`): `>` refuses to overwrite an existing file; force with
  `>|`. Good in interactive shells, keep it out of scripts you did not write.
- `cmd > file 2>&1 &` for background jobs — otherwise a backgrounded job writing to the
  terminal garbles your prompt, and a job reading stdin stops (`SIGTTIN`).
- `nohup cmd &` appends to `nohup.out` (or `$HOME/nohup.out`) if stdout is a terminal and redirects a terminal stdin from an unreadable file (nohup(1)); be explicit instead.
- `> file` with no command truncates it (`: > file` is the idiom to empty a log without
  changing its inode — `rm` + recreate breaks a still-writing daemon's handle).
- Reading and writing the same file in one pipeline empties it:
  `sort f > f` destroys `f`. Use `sort -o f f`, `sponge` (moreutils), or a temp file.

## 6. The buffering trap
C stdio line-buffers stdout on a terminal but **block-buffers** it when it is a
pipe or file (setbuf(3); the size follows `BUFSIZ`/the file's block size). So `app | grep ERROR` shows nothing for minutes, and `tail -f` of a
redirected log lags. Fixes: `stdbuf -oL app | grep ...` (works for C stdio programs),
`python -u` / `PYTHONUNBUFFERED=1`, `grep --line-buffered`, `sed -u`, `awk` with
`fflush()`, or `unbuffer app` (expect package) for stubborn ones. stderr is unbuffered
by default, which is why error lines arrive "out of order" relative to stdout in a
combined log.

## 7. Reading the plumbing of a running process
```bash
ls -l /proc/<pid>/fd            # where fds 0/1/2 point: pipe:[123], a file, /dev/null, a tty
lsof -p <pid> | head            # same, with names
cat /proc/<pid>/fdinfo/1        # offset into the file
```
A service whose fd 1 is a deleted log file (`(deleted)` suffix (gated: unconfirmed, source is paywalled or blocked)) explains the disk that stays
full after `rm` — restart the service or truncate via `: > /proc/<pid>/fd/1` (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] `ls /nonexistent / > out 2>&1; cat out` contains both the listing and the error;
      `ls /nonexistent / 2>&1 > out` shows the error on screen only.
- [ ] `false | true; echo $?` prints 0; after `set -o pipefail` it prints 1; and
      `echo "${PIPESTATUS[*]}"` directly after the pipeline shows `1 0`.
- [ ] `diff <(echo a) <(echo a)` works in bash and fails in `sh`.
- [ ] `yes | head -3 | stdbuf -oL cat` prints immediately; `python3 -c 'import time;print(1);time.sleep(5)' | cat`
      prints `1` only after 5 s without `-u`.
