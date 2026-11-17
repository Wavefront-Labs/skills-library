---
id: computing-software.systems-network-administration.bash.shell-scripting-patterns-and-error-handling
name: shell-scripting-patterns-and-error-handling
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, shell, shell-scripting, patterns, error-handling, getopts, long-options, argument-parsing, usage, logging, log-levels, err-trap, stack-trace, funcname, bash-lineno, inherit-errexit, pipestatus, retry, backoff, timeout, wait-for, dry-run, confirm-prompt, non-interactive, exit-codes, sysexits, parallel, xargs-p, wait-n, background-jobs, bats, testing, idempotent]
level: advanced
status: verified
description: "Bash patterns beyond strict mode: long-option parsing, levelled logging, ERR-trap stack traces, PIPESTATUS, retry/backoff, timeouts, dry-run, parallel jobs and bats tests."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
  - https://man7.org/linux/man-pages/man1/timeout.1.html
  - https://bats-core.readthedocs.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shell scripting patterns and error handling — the reusable building blocks

**Goal:** a toolbox of tested idioms for the parts every admin script reinvents:
options, logging, diagnosable failures, retries, parallelism and tests. The baseline
(strict mode caveats, quoting, `mktemp`, `flock`, cron) is in
`computing-software.systems-network-administration.bash.robust-bash-scripting`; this
assumes it.

## 1. Argument parsing with short and long options
`getopts` handles only short options; for long ones use a `while`/`case` loop:
```bash
usage() { printf 'Usage: %s [-n|--dry-run] [-v] --host HOST [FILE...]\n' "${0##*/}"; }
dry_run=0 verbose=0 host=
while (($#)); do
  case $1 in
    -n|--dry-run) dry_run=1 ;;
    -v|--verbose) verbose=$((verbose+1)) ;;
    --host)       host=${2:?--host needs a value}; shift ;;
    --host=*)     host=${1#*=} ;;
    -h|--help)    usage; exit 0 ;;
    --)           shift; break ;;
    -*)           usage >&2; exit 64 ;;     # EX_USAGE
    *)            break ;;
  esac
  shift
done
[[ -n $host ]] || { usage >&2; exit 64; }
```
`getopt(1)` implementations differ: traditional ones cannot cope with whitespace and many lack optional-argument support (getopt(1) man page), so avoid it in portable scripts.

## 2. Logging with levels, to stderr
```bash
LOG_LEVEL=${LOG_LEVEL:-1}   # 0=debug 1=info 2=warn 3=error
_log() { local lvl=$1; shift; (( lvl >= LOG_LEVEL )) || return 0
         printf '%s [%s] %s\n' "$(date -u +%FT%TZ)" "${LVLS[$lvl]}" "$*" >&2; }
LVLS=(DEBUG INFO WARN ERROR)
debug() { _log 0 "$@"; }; info() { _log 1 "$@"; }; warn() { _log 2 "$@"; }
```
Logs go to **stderr** so stdout stays clean data for pipes. Colour only when `[[ -t 2 ]]`.

## 3. Failures you can diagnose: ERR trap with a stack
```bash
set -Eeuo pipefail
shopt -s inherit_errexit 2>/dev/null || true   # bash 4.4+: -e applies inside $(...)
on_err() {
  local rc=$? i
  printf 'ERROR rc=%d: %s\n' "$rc" "$BASH_COMMAND" >&2
  for ((i=1; i<${#FUNCNAME[@]}; i++)); do
    printf '  at %s (%s:%d)\n' "${FUNCNAME[$i]}" "${BASH_SOURCE[$i]}" "${BASH_LINENO[$((i-1))]}" >&2
  done
}
trap on_err ERR
```
Without `inherit_errexit`, a failure inside `$(...)` doesn't stop the outer script.

**Pipelines:** `pipefail` gives the rightmost failing status; when you need to know
*which* stage failed, read `PIPESTATUS` immediately (the next command overwrites it):
```bash
set +e; pg_dump db | gzip > db.gz; st=("${PIPESTATUS[@]}"); set -e
(( st[0] == 0 )) || die "pg_dump failed (${st[0]})"
```

## 4. Retry with backoff, and timeouts
```bash
retry() {  # retry <attempts> <cmd...>
  local n=$1 i delay=2; shift
  for ((i=1; i<=n; i++)); do
    "$@" && return 0
    (( i < n )) && { warn "attempt $i/$n failed: $*; sleep ${delay}s"; sleep "$delay"; delay=$((delay*2)); }
  done
  return 1
}
retry 5 timeout 30 curl -fsS "https://<HOST>/health"
```
- Wrap anything network- or lock-bound in `timeout` (coreutils); exit 124 means timed
  out. Use `timeout -k 5 30` to SIGKILL if SIGTERM is ignored.
- Only retry **idempotent** operations. Retrying a non-idempotent POST or `mv` can
  double-apply.
- Wait for a condition rather than `sleep 60`:
  `timeout 120 bash -c 'until (exec 3<>/dev/tcp/db/5432) 2>/dev/null; do sleep 2; done'` (bash's `/dev/tcp`, no netcat needed; tested against open and closed local ports).

## 5. Dry-run and confirmation
```bash
run() { if ((dry_run)); then printf 'DRY-RUN:' >&2; printf ' %q' "$@" >&2; echo >&2; else "$@"; fi; }
run rm -rf -- "${target:?}"
confirm() { [[ -t 0 ]] || { [[ ${ASSUME_YES:-0} == 1 ]]; return; }
            read -rp "$1 [y/N] " a; [[ $a == [yY]* ]]; }
```
`printf %q` shows exactly what would run (print the `DRY-RUN:` prefix once; `printf 'DRY-RUN: %q '` would repeat it per argument). Non-interactive runs must never hang on a prompt.

## 6. Parallel work without losing failures
```bash
fail=0
for h in "${hosts[@]}"; do ssh -o BatchMode=yes "$h" uptime & done
# `rc=0; wait -n || rc=$?` keeps set -e and the ERR trap from firing on a failed job
while :; do rc=0; wait -n || rc=$?; ((rc==127)) && break; ((rc)) && fail=1; done  # bash 5.1+: wait -n -p VAR gives the PID
((fail==0)) || die "at least one host failed"
```
Or `printf '%s\0' "${hosts[@]}" | xargs -0 -P 8 -I{} ssh {} uptime` — xargs exits
**123** if any invocation failed. Cap concurrency; a plain `&` per item can fork-bomb
a 5,000-host list. A job exiting 127 itself is indistinguishable from "no jobs left";
use GNU `parallel --joblog` when that matters.

## 7. Exit codes as a contract
0 OK, 1 general failure, 2 misuse (bash builtins), 64-78 per `sysexits.h` (64 usage,
69 unavailable, 75 temp-fail → caller may retry). Document them in `--help`.

## 8. Test with bats
`run` saves the command's exit status in `$status` and its combined output in `$output`/`$lines` and returns 0 (bats docs).
```bash
@test "rejects missing --host" { run ./tool.sh; [ "$status" -eq 64 ]; }
```
Put functions in a sourced library with a `[[ ${BASH_SOURCE[0]} == "$0" ]] && main "$@"`
guard so tests can source it without running `main`.

**Unconfirmed:** the `wait -n` loop semantics differ slightly across bash 4.3-5.2; test
on the target bash version.

## Verify
- [ ] `--help`, unknown options and missing values give usage and exit 64.
- [ ] An injected failure prints the failing command and a function/line stack.
- [ ] `--dry-run` executes nothing destructive and prints exact commands.
- [ ] Non-interactive runs never block on a prompt.
- [ ] One failed parallel job makes the script exit non-zero.
