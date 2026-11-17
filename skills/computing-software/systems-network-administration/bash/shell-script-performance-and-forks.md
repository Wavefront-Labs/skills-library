---
id: computing-software.systems-network-administration.bash.shell-script-performance-and-forks
name: shell-script-performance-and-forks
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, sh-performance, subshell-forks, builtins-vs-external, loops-vs-pipelines]
level: advanced
status: docs-checked
description: "Make bash scripts faster by avoiding subshells and external commands in loops: $(< file), printf -v, mapfile, (( )) and wait -n."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shell performance

- Each command in a multi-command pipeline runs in its own subshell (a separate process), and `$(...)` command substitution runs in a subshell environment. A loop that starts external commands or subshells per line multiplies that cost. Prefer builtins and expansions: parameter expansion, `[[ =~ ]]`, `read`, `printf -v`, arithmetic `(( ))`, or run one tool over the whole input.
- The bash manual says `$(cat file)` can be replaced by the equivalent but faster `$(< file)`.
- `mapfile` reads lines from standard input into an indexed array, so you can read a file once and iterate the array instead of running a command per line.
- Sequence expressions like `{1..n}` need literal numbers: brace expansion happens first, before parameter expansion, so a variable inside the braces is not expanded in time. Use the C-style `for ((i=1; i<=n; i++))` with a variable.
- `wait -n` waits for any one background job to finish and returns its exit status; combined with a counter it bounds parallel background jobs. Avoid unbounded `&`.
- `set -x` with a custom `PS4` shows what each command expands to; the `PS4` value is printed before every traced command.
- `lastpipe` (with job control off) lets the last pipeline element run in the current shell, so variables set in it survive.
- Measure first; consider another language when logic outgrows a shell script.

## Checked
2026-11-09. Confirmed in the bash manual: pipeline subshells and `lastpipe`, command substitution subshell and `$(< file)`, `mapfile`, expansion order (brace expansion first), `wait -n`, `PS4` tracing. Removed: claims that `while read` is slow for more than a few thousand lines, `expr`, `seq`, `xargs -P`, GNU parallel, `time`, `EPOCHREALTIME` in `PS4` (bash 5), `strace` and `perf`, which the cited pages do not state; the POSIX root URL (a stub page) was dropped from sources.
Method: documentation only; no commands were run.
