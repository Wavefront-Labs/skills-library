---
id: computing-software.systems-network-administration.bash.disown-builtin
name: disown-builtin
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, disown-builtin, disown-h, shell-scripting]
level: practitioner
status: docs-checked
description: "Detach running bash jobs with disown and -h so they survive terminal closure and drop out of the job table."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# disown and SIGHUP
**Goal:** keep a started job alive after logout.
```bash
long_task &                 # start in background
disown -h %1                # keep in table but do not send SIGHUP at exit
disown %1                   # remove from table entirely
disown -a                   # all jobs
# already running in foreground:
# Ctrl-Z ; bg ; disown -h
shopt -s huponexit          # opposite: send SIGHUP to jobs on exit
jobs -l
```
- Redirect the job output when you start it, for example `long_task >out.log 2>&1 </dev/null &`.

## Checked

2026-11-02: Confirmed in Job Control Builtins (`disown [-ar] [-h] [id ...]`: removes from the table or with -h marks so SIGHUP is not sent; -a all jobs) and the `huponexit` shopt option. Removed: SIGPIPE/EIO, setsid/nohup, tmux claims.
Source read: GNU Bash Reference Manual (https://www.gnu.org/software/bash/manual/bash.html).
Method: documentation only; no commands were run.
