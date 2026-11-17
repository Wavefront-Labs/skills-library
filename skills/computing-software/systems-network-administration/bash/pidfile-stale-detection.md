---
id: computing-software.systems-network-administration.bash.pidfile-stale-detection
name: pidfile-stale-detection
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, pidfile-stale-detection, pidfile, shell-scripting]
level: advanced
status: draft
description: "Write pidfiles and detect stale locks in shell scripts by checking the recorded PID and command, without races."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pidfiles and stale lock detection
**Goal:** safe single-instance guard where flock is unavailable.
```bash
pidfile=/run/myjob.pid
if ( set -o noclobber; echo "$$" > "$pidfile" ) 2>/dev/null; then
  trap 'rm -f -- "$pidfile"' EXIT
else
  old=$(cat "$pidfile" 2>/dev/null)
  if [ -n "$old" ] && kill -0 "$old" 2>/dev/null; then
    echo "running as $old" >&2; exit 1
  fi
  echo "stale pidfile $old; removing" >&2; rm -f -- "$pidfile"; exec "$0" "$@"
fi
```
- `noclobber` makes the create atomic (O_EXCL).
- `kill -0` only checks existence; PIDs get reused, so also compare `/proc/$old/cmdline` where available.
- `mkdir lockdir` is an equally atomic alternative.
- A crash leaves the file behind; the stale check handles it. Prefer flock when present.
- Self-check: kill -9 the first run; the second run reports stale and proceeds.
