---
id: computing-software.systems-network-administration.bash.bash-coproc-coprocesses
name: bash-coproc-coprocesses
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, coproc, coprocess, bash-fd, two-way-pipe, bc, bash-advanced]
level: advanced
status: gated
description: "Talk two-way to a long-lived helper with bash coproc: the COPROC fd array, safe reads and writes, closing, buffering deadlocks, and when to use FIFOs instead."
sources:
  - https://www.gnu.org/software/bash/manual/html_node/Coprocesses.html
  - https://mywiki.wooledge.org/BashFAQ/024
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bash coprocesses

**Goal:** keep one process (bc, a DB client, an ssh session, a REPL) running and talk to it repeatedly
instead of forking it per query.

```bash
coproc CALC { bc -l; }                  # CALC[0] = read from it, CALC[1] = write to it, CALC_PID
for x in 2 3 10; do
  echo "sqrt($x)" >&"${CALC[1]}"
  read -r -u "${CALC[0]}" result
  printf '%s -> %s\n' "$x" "$result"
done
exec {CALC[1]}>&-                         # close its stdin -> bc exits (gated: unconfirmed, source is paywalled or blocked; bc is not installed here, the loop, close and wait were run with `cat` as the child)
wait "$CALC_PID"
```
Unnamed form: `coproc cmd args` → array `COPROC`. Only one active coprocess is fully supported; bash
warns on a second (run: "warning: execute_coproc: coproc [30031:COPROC] still exists", where the numbers are a pid and the name).

## Buffering deadlocks
The child sees a pipe, not a terminal, so many programs fully buffer stdout — your `read` waits forever.
Fixes: tools with line-buffer flags (`grep --line-buffered`, `python -u`, `sed -u`), `stdbuf -oL cmd`,
or protocols with a known terminator you read until.

## Timeouts
`read -t 5 -r -u "${CALC[0]}" line || echo "no answer"` — never block forever on an external process.

## Gotchas
- The fd variables are only valid in the shell that created the coproc: writing to `"${CALC[1]}"` inside `( ... )` or a `{ ...; }` after a pipe failed with "Bad file descriptor" (bash 5.2.37).
- After the coprocess exits and has been reaped, the array and `NAME_PID` are unset (run) and writes to the stale fd give `Bad file descriptor`.
- Buffering demo (run): `python -c` reading stdin never answered `read -t 2`; `python -u` answered at once. `grep --line-buffered`, `sed -u` and `stdbuf -oL` flags exist.
- For anything complex (multiple helpers, persistence) use named pipes (`mkfifo`) or a real language.

## Verify
- [ ] Script finishes with the coprocess reaped (`wait` returns its status), no leftover child in `ps`.
