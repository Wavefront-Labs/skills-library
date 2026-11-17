---
id: computing-software.systems-network-administration.bash.named-coproc-fd
name: named-coproc-fd
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, named-coproc-fd, coproc-named, shell-scripting]
level: advanced
status: docs-checked
description: "Use named bash coprocesses and their file descriptor array to talk to a background process and clean it up."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Named coprocesses and descriptors
**Goal:** interact with a long-running helper.
```bash
coproc CALC { bc -l; }
echo "2^10" >&"${CALC[1]}"          # write to coprocess stdin
read -r -u "${CALC[0]}" result      # read its stdout
echo "$result"
w=${CALC[1]}; exec {w}>&-           # close its stdin; the helper sees EOF
wait "$CALC_PID"
```
- `coproc NAME { command; }` is the recommended form. The shell creates array `NAME`: `NAME[0]` is the descriptor for the coprocess's standard output (read it), `NAME[1]` is the descriptor for its standard input (write to it). `NAME_PID` holds the process ID of the shell spawned for the coprocess.
- If NAME is omitted the default name is `COPROC`. Simple commands (`coproc cmd args`) cannot take a NAME and always use `COPROC`.
- The descriptors can be used through ordinary expansion in redirections and as arguments (`read -u fd`). They are not available in subshells, other than those created to run the command and process substitutions.
- `exec {var}>&-` closes the descriptor whose number is stored in `var`; the `{varname}` form of `>&-` takes the variable's value as the descriptor to close.
- `wait` may be used to wait for the coprocess; `coproc` itself always returns success because the coprocess runs asynchronously, and the coprocess's own status is the exit status of the command.
- `read -t timeout` returns a status greater than 128 on timeout, which keeps a script from blocking forever on a silent helper. `-t` works on pipes.
- Whether the helper flushes its output, and whether it exits on EOF, depends on the helper program, not on bash; check its own documentation.

## Checked
Date: 2026-11-07
Method: Read GNU Bash manual section 3.2.6 Coprocesses, the Redirections paragraph on {varname}, and the read builtin entry (-u, -t) against each claim. Trims: removed the unsourced claims that only one coprocess is supported or warns, that descriptors vanish on exit, the `stdbuf -oL` buffering advice, the "prints 1024" comment and self-check (bc behaviour, not in the manual), and changed the close command from `exec {CALC[1]}>&-` to a variable form because the manual documents only the {varname} form. Searched the manual text for coproc rather than reading all 523k characters.
