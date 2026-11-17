---
id: computing-software.systems-network-administration.bash.while-read-null
name: while-read-null
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, while-read-null, read-d-null, print0-loop, shell-scripting]
level: practitioner
status: docs-checked
description: "Iterate file names safely with find -print0 process-substituted into while IFS= read -r -d '' so the loop runs in the current shell."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Null-delimited while read loops
**Goal:** loop over arbitrary filenames (spaces, newlines) without word splitting.
```bash
while IFS= read -r -d '' f; do
  printf 'file: %s\n' "$f"
done < <(find . -type f -name '*.log' -print0)
```
- `-d ''` makes read terminate a record at a NUL character (an empty delim); `-r` stops backslash acting as an escape. Emptying `IFS` (the word-splitting characters) leaves the name unsplit.
- Use process substitution (`< <(...)`) not a pipe, so variables set in the loop survive: each command in a pipeline runs in its own subshell. Process substitution needs a system with named pipes (FIFOs) or `/dev/fd`.
- The pipe form `find ... -print0 | while ...` keeps the loop in a subshell unless `shopt -s lastpipe` is set and job control is not active (the usual case in a script).
- To keep a loop body from consuming the loop's input (for example a command that reads stdin), read from another descriptor with `read -r -d '' -u 3 f ... 3< <(...)`; `-u fd` reads from file descriptor fd.
- Self-check: create `touch 'a b' $'c\nd'`; the loop prints two entries.

## Checked
2026-11-08. Confirmed in the GNU Bash manual: read -d with an empty delimiter terminates at NUL; -r; -u fd; pipeline elements run in their own subshell; lastpipe requires job control not active; process substitution requires FIFOs or /dev/fd. Removed: "non-interactive only" wording for lastpipe (manual states only the job-control condition), and the sort -z, grep -Z, xargs -0 and ssh/ffmpeg claims, which are not in the bash manual.
Method: documentation only; no commands were run.
