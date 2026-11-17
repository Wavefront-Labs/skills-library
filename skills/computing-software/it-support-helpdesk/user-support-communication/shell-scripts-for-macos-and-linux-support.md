---
id: computing-software.it-support-helpdesk.user-support-communication.shell-scripts-for-macos-and-linux-support
name: shell-scripts-for-macos-and-linux-support
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, scripting, bash-script, zsh, sh, shebang, set-euo-pipefail, macos-scripting, linux-scripting, current-user, comptia-a-plus]
level: intro
status: draft
description: "Write small bash/zsh support scripts for Macs and Linux: shebang and strict mode, quoting, exit codes, running as root vs the logged-in user, logging, and MDM delivery."
sources:
  - "https://www.gnu.org/software/bash/manual/bash.html"
  - "https://support.apple.com/guide/terminal/welcome/mac"
  - "https://www.comptia.org/certifications/a"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# shell-scripts-for-macos-and-linux-support

Goal: automate small support tasks on Macs and Linux safely (A+ 220-1202
4.8: .sh use cases).

## Template
```bash
#!/bin/bash
# Reset the printing system queue for the current user's printer issue
set -euo pipefail
LOG="/var/log/corp-support.log"
log(){ echo "$(date '+%F %T') $*" >> "$LOG"; }

currentUser=$(stat -f%Su /dev/console)          # macOS logged-in user
[ -z "$currentUser" ] || [ "$currentUser" = "root" ] && { log "no user"; exit 0; }

log "cancelling jobs for all queues"
cancel -a || log "cancel returned $?"

# run something as the user (MDM scripts run as root)
uid=$(id -u "$currentUser")
launchctl asuser "$uid" sudo -u "$currentUser" open -a "Printers & Scanners" || true
log "done"
exit 0
```
Linux logged-in user: `loginctl list-sessions` or `who`.

## Rules
- Shebang first line (`#!/bin/bash` or `#!/bin/zsh`; macOS default
  interactive shell is zsh, `/bin/bash` is old 3.2 — avoid bash-4 features
  or use zsh/sh).
- `set -euo pipefail`: stop on errors, undefined variables, pipe failures —
  then handle expected failures explicitly with `|| true`.
- **Quote variables** (`"$path"`) — unquoted paths with spaces break and can
  delete the wrong thing.
- Exit codes: 0 success, non-zero failure — MDM (Jamf/Intune) reports based
  on it.
- `chmod +x script.sh`; run with `sudo` only when needed.
- Log to a file the desk can collect.

## Context
- Jamf/Intune macOS scripts run as **root**; user-level actions need
  `launchctl asuser` + `sudo -u`.
- Jamf passes parameters `$4`–`$11` (and `$3` = username).
- Linux remote: `ssh user@host 'bash -s' < script.sh`.

## Gotchas
- `rm -rf "$dir/"*` with an empty `$dir` deletes from `/` — guard:
  `[ -n "$dir" ] || exit 1`, or `${dir:?}`.
- Windows line endings (CRLF) break scripts (`/bin/bash^M: bad
  interpreter`) — save as LF.
- macOS privacy (TCC) blocks scripts from some folders unless the MDM grants
  Full Disk Access to the agent.

## Verify
Run on a test machine through the same delivery path (MDM/SSH); exit code 0
and log entries as expected; `shellcheck script.sh` reports no warnings.
