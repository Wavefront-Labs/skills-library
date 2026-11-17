---
id: computing-software.systems-network-administration.bash.xargs-null-delimited-and-parallel
name: xargs-null-delimited-and-parallel
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, xargs, xargs-0, xargs-null, xargs-p, xargs-i, parallel, print0, arg-max, no-run-if-empty, gnu-parallel, file-management, lfcs, sysadmin]
level: practitioner
status: verified
description: "Build command lines from stdin with xargs: -0 for NUL-safe input, -I {} placement, -n/-L batching, -P parallelism, -r on empty input, ARG_MAX limits, and when GNU parallel is worth it."
sources:
  - https://man7.org/linux/man-pages/man1/xargs.1.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# xargs — NUL-delimited input, batching and parallel execution

**Goal:** feed thousands of filenames or arguments into commands without breaking on
spaces, without exceeding the kernel argument limit, and using all CPU cores when it helps.

## 1. The safe default: -0
```bash
find . -name '*.log' -print0 | xargs -0 gzip
grep -rlZ 'pattern' . | xargs -0 sed -i 's/a/b/'
printf '%s\0' "${files[@]}" | xargs -0 rm -f          # from a bash array
```
Without `-0`, xargs splits on whitespace **and** interprets quotes/backslashes: `it's.txt`
produces "unmatched single quote". `-d '\n'` is the second-best option for line input you
trust not to contain newlines.

## 2. Placing the argument
```bash
ls *.jpg | xargs -I{} convert {} -resize 50% small/{}    # {} may appear several times
cat hosts | xargs -I{} ssh {} uptime
cat hosts | xargs -I{} sh -c 'echo "== {}"; ssh {} uptime'
```
`-I` implies one argument per command (`-L 1`) and disables the batching speed-up; it also
runs commands sequentially unless combined with `-P`. For many files prefer `-n`/batching
without `-I` when the command accepts multiple trailing arguments.

## 3. Batching and limits
```bash
xargs -n 100 rm -f            # 100 args per invocation
xargs -L 2 echo               # 2 input lines per invocation
xargs --show-limits </dev/null   # ARG_MAX and what xargs will use
getconf ARG_MAX               # Linux: 1/4 of the stack limit (execve(2)), so 2 MiB with an 8 MiB stack; one string max 32 pages = 128 KiB on 4 KiB pages
```
xargs automatically splits to stay under the limit, which is exactly why `rm $(find ...)`
("Argument list too long") should be `find ... | xargs -0 rm`.

## 4. Parallelism
```bash
find . -name '*.png' -print0 | xargs -0 -P"$(nproc)" -n 20 optipng -quiet
cat urls | xargs -P 8 -n 1 curl -sO
seq 1 100 | xargs -P 4 -I{} sh -c 'sleep 0.1; echo job {}'
```
- Output from parallel jobs interleaves; use `-P` with commands that write to their own
  files, or wrap with `flock` / `--process-slot-var` (GNU) to tag output.
- Exit status (tested with GNU xargs 4.10): 123 if any invocation exited 1–125, 124 if one exited 255 (xargs stops),
  125 if killed by a signal, 126 if the command cannot be run, 127 if not found. Check `$?` — a failing batch is not silent.

## 5. Edge cases
```bash
echo | xargs -r rm            # -r / --no-run-if-empty: don't run rm with no args
xargs -t cmd                  # trace: print each command line before running
xargs -p cmd                  # prompt before each
xargs -a file cmd             # read from file, keep stdin for the command (e.g. ssh)
```
Without `-r`, `echo "" | xargs rm` runs `rm` with no args (harmless) but `xargs ls` lists
the cwd — surprising in scripts. FreeBSD's xargs never runs the utility on empty input and accepts `-r` as a no-op (its man page).

## 6. When to use GNU parallel instead
`parallel` keeps per-job output grouped (`--group`, default), tags lines (`--tag`), distributes over SSH hosts (`-S`), and writes a `--joblog` (GNU parallel man page; not installed here, so not run). For a one-off `-P` loop xargs
is enough; for a nightly job whose log must be readable, use `parallel -j8 --joblog run.log`.

## Failure modes
- "xargs: unmatched single quote": input not NUL-delimited — add `-0`/`-d '\n'`.
- Command sees `{}` literally: `-I` missing, or `{}` inside a quoted string with `-I` and
  the replacement string contains unbalanced quotes.
- Nothing happened on an empty result but exit 0: that is `-r` behaviour; fine, but check
  the producer if you expected matches.
- `sudo` with xargs prompts once per batch: `sudo xargs ...` (sudo outside) or `-P1`.

## Verify
- [ ] `... | xargs -0 -t cmd 2>&1 | head` shows correctly quoted argument lists.
- [ ] Echo `$?` after the pipeline; 0 means every batch succeeded (set `pipefail` in scripts).
