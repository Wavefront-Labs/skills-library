---
id: computing-software.systems-network-administration.bash.bash-debugging-set-x-and-ps4
name: bash-debugging-set-x-and-ps4
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, set-x, bash-xtrace, ps4, bash-debugging, bash-n, bash-v, bash-lineno, bash-source, funcname, bash-trap-debug, bashdb, shellcheck, shell-scripting, sysadmin]
level: practitioner
status: verified
description: "Debug bash scripts: set -x with an informative PS4 (file:line:function), trace to a separate fd, bash -n/-v syntax checks, DEBUG/ERR traps, and narrowing a trace to one function."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html#The-Set-Builtin
  - https://www.gnu.org/software/bash/manual/bash.html#Bash-Variables
  - https://www.gnu.org/software/bash/manual/bash.html#Bourne-Shell-Builtins
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging bash — make the shell tell you what it actually executed

**Goal:** see each command after expansion, with the file, line and function it came from,
without drowning the script's real output.

## 1. set -x done properly
```bash
export PS4='+ ${BASH_SOURCE##*/}:${LINENO}:${FUNCNAME[0]:-main}: '
set -x
...
set +x
```
- Default `PS4='+ '` tells you nothing about where you are. The first character of PS4 is
  repeated per nesting level (`++` inside a subshell/function).
- `bash -x script.sh` traces the whole script; `set -x` inside toggles regions. For an
  installed script you cannot edit: `bash -x /path/script args`.
- Trace shows commands **after** expansion and quote removal — the fastest way to spot a
  variable that expanded empty or split into several words.

## 2. Keep the trace away from real output
```bash
exec 5> /tmp/trace.log
BASH_XTRACEFD=5
set -x
```
Trace goes to fd 5, stdout/stderr stay clean. Add `$EPOCHREALTIME` to PS4 for timing:
`PS4='+ $EPOCHREALTIME ${BASH_SOURCE##*/}:$LINENO: '`.

## 3. Syntax and parse-level checks before running
```bash
bash -n script.sh            # parse only; catches unbalanced quotes/fi/done
bash -v script.sh            # echo lines as read (before expansion) — pair with -x
shellcheck script.sh         # static analysis: quoting, [ ] vs [[ ]], useless cat, SC2086...
```
`bash -n` does not execute, so it cannot find runtime errors like unbound variables.

## 4. Traps for stepping and failure context
```bash
trap 'echo "ERR at ${BASH_SOURCE}:${LINENO} in ${FUNCNAME[0]:-main}: $BASH_COMMAND (rc=$?)" >&2' ERR
set -E    # errtrace: ERR trap inherited by functions/subshells (otherwise it is not)

trap 'read -rp "$LINENO: $BASH_COMMAND  [Enter]" _' DEBUG   # poor man's single-step
```
(`read -p` shows its prompt only when stdin is a terminal.) Run on bash 5.2.37: without `set -E` a failing function call fires the ERR trap once in the caller, with `set -E` it also fires inside the function. `$BASH_COMMAND` is the command about to run (DEBUG) or that failed (ERR). `caller 0`
inside a function prints line/function/file of the caller — a cheap stack frame.

## 5. Scoping a trace
```bash
f() { local -; set -x; ...; }          # bash 4.4+: 'local -' restores set options on return
( set -x; cmd ) 2>trace.txt            # subshell scope
```
To trace a function called many times, `set -x` only when `[[ $1 == bad-input ]]`.

## 6. Reading a trace
- `+ [[ '' == foo ]]`: variable empty — unset, wrong scope (subshell), or set after use.
- `+ rm -rf /srv/app/ ''` with an unexpected extra argument: unquoted expansion split a path.
- A line with no `+`: it is the command's own output or stderr, not the trace.
- `++` prefixed lines inside `$(...)`: subshell expansion; errors there do not trip `set -e`
  unless the assignment itself is the command.

## Failure modes
- Secrets in traces: `set -x` prints passwords in expanded `curl -u user:pass`. Disable
  around sensitive lines (`set +x`) or pass via env/file.
- Trace missing for pipelines/functions: `set -x` was in a subshell; put it at top level.
- `set -e` seems ignored while debugging: commands in `if`, `&&`, `||` lists are exempt by design.
- Trace output interleaves oddly with stdout buffering: use `BASH_XTRACEFD` or `stdbuf -oL`.

## Verify
- [ ] Running with the PS4 above shows `file:line:function:` prefixes on every traced line.
- [ ] `bash -n` passes and `shellcheck` reports no errors before you reach for `set -x`.
