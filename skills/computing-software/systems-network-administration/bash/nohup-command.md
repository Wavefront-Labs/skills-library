---
id: computing-software.systems-network-administration.bash.nohup-command
name: nohup-command
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, nohup-command, setsid, shell-scripting]
level: practitioner
status: docs-checked
description: "Run commands immune to hangup with nohup, handling output files, stdin, backgrounding and exit status."
sources:
  - https://www.gnu.org/software/coreutils/manual/html_node/nohup-invocation.html
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nohup
**Goal:** start a process that keeps running after you log out.
```bash
nohup ./job.sh > job.log 2>&1 < /dev/null &
echo $! > job.pid
nohup make > make.log &              # as in the coreutils manual's make example
```
- `nohup command [arg]...` runs the command with hangup signals ignored, so it can continue in the background after logout.
- If standard input is a terminal, nohup redirects it to an unreadable substitute (a GNU extension); the manual suggests `nohup command [arg]... 0>/dev/null` for portability.
- If standard output is a terminal, output is appended to `nohup.out`, else to `$HOME/nohup.out`, and if neither can be written the command is not run. A file created this way is readable and writable only by the user, regardless of umask. A terminal standard error is redirected to the same place as standard output.
- Redirect output yourself to avoid `nohup.out`: `nohup make > make.log`.
- nohup does not put the command in the background and does not change its niceness; end the line with `&` to background it, and use `nohup nice command` for niceness.
- `$!` is the process ID of the most recent job started in the background (bash special parameter), used here to write the pidfile.
- The command must not be a special built-in utility. Options are only `--help` and `--version`, and they must precede operands.
- Exit status: 125 if nohup itself fails (127 if `POSIXLY_CORRECT` is set), 126 if the command is found but cannot be invoked, 127 if it cannot be found, otherwise the command's exit status.

## Checked
Date: 2026-11-07
Method: Read the GNU coreutils nohup page in full and the Bash manual entry for the `!` special parameter. Trims: removed `setsid` and `systemd-run` lines and the "SIGTERM/SIGKILL still kill it" and "real services deserve a systemd unit" advice (neither is in these sources), and the log-out `pgrep` self-check. Added the stdin redirection rule, nohup.out fallbacks, niceness note and the correct exit statuses (the draft said only 126/127). The description was reworded to drop setsid.
