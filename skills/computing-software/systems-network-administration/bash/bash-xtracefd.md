---
id: computing-software.systems-network-administration.bash.bash-xtracefd
name: bash-xtracefd
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, bash-xtracefd, xtrace-fd, shell-scripting]
level: advanced
status: docs-checked
description: "Send bash xtrace output to a separate file descriptor with BASH_XTRACEFD so debug traces do not mix with script output."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BASH_XTRACEFD
**Goal:** trace without polluting stderr.
```bash
exec 5> /path/to/trace.log       # any free fd
BASH_XTRACEFD=5
PS4='+ ${BASH_SOURCE##*/}:${LINENO}:${FUNCNAME[0]:-main}: '
set -x
do_work
set +x
```
- If `BASH_XTRACEFD` is set to an integer naming a valid file descriptor, bash writes the `set -x` trace to that descriptor instead of standard error, which separates trace output from diagnostic and error messages.
- The descriptor is closed when `BASH_XTRACEFD` is unset or assigned a new value. Unsetting it, or assigning the empty string, sends the trace back to standard error.
- Setting it to 2 and then unsetting it results in standard error being closed; avoid that.
- `PS4` is expanded like `PS1` and the result is printed before each traced command and its expanded arguments; its default is `+ `. Its first character is replicated to indicate multiple levels of indirection.
- Traces include the expanded values of commands, so secrets passed as arguments can land in the log; turn tracing off with `set +x` around them.

## Checked
Date: 2026-11-07
Method: Read GNU Bash manual BASH_XTRACEFD, PS4 and the set -x entries (searched by name rather than reading all of the 523k-character page). Trims: removed "bash 4.1+ only" (version not on the page), the claim that closing the fd while tracing is the way to stop output (the manual says unset or reassign closes it), "set -x is inherited by functions but not subshells' env vars" (unsupported and unclear), the `/tmp/trace.$$.log` path, and the invented Verify step.
