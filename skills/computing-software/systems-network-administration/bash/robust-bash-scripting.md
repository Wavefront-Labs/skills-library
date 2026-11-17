---
id: computing-software.systems-network-administration.bash.robust-bash-scripting
name: robust-bash-scripting
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, shell, shell-scripting, sh, posix, set-e, errexit, nounset, pipefail, strict-mode, quoting, arrays, trap, cleanup, mktemp, shellcheck, cron, crontab, flock, locking, exit-codes, getopts, idempotent, linux, unix, zsh]
level: practitioner
status: verified
description: "Write bash scripts that fail safely: set -euo pipefail and its traps, quoting, arrays, trap cleanup, mktemp, shellcheck, flock locking and cron env gotchas."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
  - https://www.shellcheck.net/
  - https://mywiki.wooledge.org/BashPitfalls
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Robust bash scripting — fail loudly, clean up, never run twice

**Goal:** admin scripts that stop on errors, handle any filename, clean up after
themselves, and behave the same under cron as in your terminal.

## 1. Skeleton
```bash
#!/usr/bin/env bash
set -Eeuo pipefail

readonly SCRIPT_NAME=${0##*/}
log() { printf '%s %s: %s\n' "$(date -Is)" "$SCRIPT_NAME" "$*" >&2; }
die() { log "ERROR: $*"; exit 1; }

tmpdir=$(mktemp -d) || die "mktemp failed"
cleanup() { rm -rf -- "$tmpdir"; }
trap cleanup EXIT
trap 'log "failed at line $LINENO: $BASH_COMMAND"' ERR

main() {
  [[ $# -ge 1 ]] || die "usage: $SCRIPT_NAME <dir>"
  local target=$1
  [[ -d $target ]] || die "not a directory: $target"
  # work here
}
main "$@"
```

## 2. `set -euo pipefail`: useful, not magic
- `-e` exits on an unchecked failing command. It is **ignored** inside `if`, `while`,
  `&&`/`||` lists, and in functions called from those contexts. A function used as
  `if myfunc; then` runs with `-e` effectively off.
- `local var=$(cmd)` hides `cmd`'s failure (exit status is `local`'s). Declare first:
  `local var; var=$(cmd)`.
- `((count++))` returns 1 when count was 0 and kills the script. Use `count=$((count+1))`.
- `grep` returning 1 for "no match" is a failure: write `grep pattern file || true`
  when no match is acceptable.
- `-u` breaks on unset optional vars: use `${VAR:-default}`; for arrays `"${arr[@]}"` is
  fine on bash 4.4+ but errors when empty on older bash (fixed in 4.4, bash CHANGES).
- `pipefail` makes `cmd | head -1` fail with SIGPIPE (141) in some cases.
- `-E` makes the ERR trap fire inside functions too.

Always check critical steps explicitly anyway: `cp "$a" "$b" || die "copy failed"`.

## 3. Quoting and arrays
- Quote every expansion: `"$file"`, `"$@"`, `"$(cmd)"`. Unquoted values word-split and
  glob, so a file named `a b*` breaks or matches extra files.
- Use arrays for argument lists, never strings:
```bash
opts=(-a -v)
cp "${opts[@]}" -- "$src" "$dst"
```
- Iterate files safely: `find "$dir" -type f -print0 | while IFS= read -r -d '' f; do ...; done`
  or `mapfile -d '' files < <(find ... -print0)`. Never `for f in $(ls)`.
- `[[ ]]` over `[ ]` in bash; `--` before user-supplied paths (`rm -- "$f"`).
- `rm -rf "$dir/"*` with an empty `$dir` deletes from `/`. Guard: `${dir:?}`.

## 4. Temp files and cleanup
`mktemp` / `mktemp -d` create unique paths (files `u+rw`, directories `u+rwx`, minus umask restrictions: mktemp(1)); never hand-build
`/tmp/myscript.$$` (predictable, race-prone). The `EXIT` trap runs on normal exit, on
`exit` and after `set -e` aborts; for SIGINT/SIGTERM add `trap 'exit 130' INT TERM` so
EXIT cleanup still runs.

## 5. Never run twice: `flock`
```bash
exec 9>/var/lock/myjob.lock
flock -n 9 || { log "already running"; exit 0; }
```
Or wrap in cron: `flock -n /var/lock/myjob.lock /usr/local/bin/myjob.sh`. A flock lock is dropped when the file is closed (flock(1)), which happens when the process exits, so there is no stale PID file to clean up.

## 6. Cron gotchas
- Cron's `PATH` is minimal and implementation-specific (crontab(5) does not fix a value). Set `PATH=` at the top of the crontab
  or the script, or use absolute paths.
- No login profile: env vars from `~/.bashrc` do not exist. Set them explicitly.
- `%` is special in crontab lines (newline); escape as `\%` in `date +\%F`.
- Output is mailed or lost. Redirect: `>> /var/log/myjob.log 2>&1`, or log via
  `logger -t myjob`.
- Cron runs commands with `/bin/sh` unless `SHELL` is set in the crontab (crontab(5)); your shebang still applies to scripts.
- Test exactly as cron runs it: `env -i PATH=/usr/bin:/bin /bin/sh -c '/usr/local/bin/myjob.sh'`.
- Consider a systemd timer instead (see
  `computing-software.systems-network-administration.linux.systemd-service-management`).

## 7. Lint and test
`shellcheck -x script.sh` catches most quoting and logic bugs; treat warnings as errors
in CI. `bash -n` checks syntax; `bash -x` (or `set -x` around a section) traces.
Make scripts idempotent (safe to rerun) and support `--dry-run` for destructive steps.
Exit codes: 0 success, non-zero failure; never `exit` with a value above 255.

## Verify
- [ ] `shellcheck` reports nothing (or each disable is commented with a reason).
- [ ] Script fails with a clear message when a required command fails or an argument is missing.
- [ ] Works on filenames containing spaces, newlines and leading dashes.
- [ ] Temp files are gone after normal exit, error exit and Ctrl-C.
- [ ] A second concurrent run exits immediately because of `flock`.
- [ ] Runs correctly under `env -i` with cron's minimal PATH.
