---
id: computing-software.systems-network-administration.bash.time-pipeline
name: time-pipeline
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, time-pipeline, timeformat, shell-scripting]
level: practitioner
status: docs-checked
description: "Time whole pipelines with the bash time keyword and TIMEFORMAT, and tell it apart from /usr/bin/time."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timing pipelines: time keyword
**Goal:** measure elapsed, user and system time of a pipeline.
```bash
time sort big.txt | uniq -c > /dev/null    # times the WHOLE pipeline
TIMEFORMAT='real=%R user=%U sys=%S'; time make
```
- `time` is a reserved word that precedes a pipeline: Bash prints elapsed (wall-clock), user and system time once the pipeline finishes. Because it is a reserved word it can time shell builtins, functions and pipelines, which an external `time` command cannot do easily.
- `time -p` prints in the POSIX format. In POSIX mode `time` by itself is a simple command showing total shell and children times, and `time` followed by a token beginning with `-` is not treated as the reserved word.
- TIMEFORMAT controls the output: `%R` elapsed seconds, `%U` user CPU seconds, `%S` system CPU seconds, `%P` CPU percentage ((%U + %S) / %R), `%%` a literal percent. An optional digit sets precision (default 3, at most 6) and `l` gives the `MMmSS.FFs` form, for example `%3lR`.
- If TIMEFORMAT is unset the format is `$'\nreal\t%3lR\nuser\t%3lU\nsys\t%3lS'`; a null value prints nothing; a trailing newline is added.
- Self-check: `time sleep 1` shows real near 1s.

## Checked
2026-11-08: confirmed against the GNU Bash Reference Manual (single-page bash.html): the Pipelines section (time reserved word, -p, POSIX-mode note) and the TIMEFORMAT variable. Removed the `/usr/bin/time -v` line, the "report goes to stderr" assertion and the capture-into-a-variable idiom, which the manual does not state.
Method: documentation only; no commands were run.
