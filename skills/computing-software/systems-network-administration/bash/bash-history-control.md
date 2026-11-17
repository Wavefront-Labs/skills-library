---
id: computing-software.systems-network-administration.bash.bash-history-control
name: bash-history-control
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, bash-history, histcontrol, histsize, histfilesize, histtimeformat, histignore, histappend, history-command, bang-commands, ctrl-r, shared-history, audit-history, shell-environment, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Configure bash history: HISTSIZE/HISTFILESIZE, histappend and history -a sync, HISTCONTROL/HISTIGNORE, timestamps, Ctrl-R and ! expansion, and keeping secrets out."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html#Bash-History-Facilities
  - https://www.gnu.org/software/bash/manual/bash.html#Bash-Variables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bash history — keep everything useful, lose nothing, leak nothing

**Goal:** a history that survives concurrent sessions, carries timestamps, skips noise and
secrets, and is searchable in a keystroke.

## 1. Recommended ~/.bashrc block
```bash
HISTSIZE=100000            # lines kept in memory
HISTFILESIZE=200000        # lines kept in the history file
HISTCONTROL=ignoreboth:erasedups   # ignorespace + ignoredups; erasedups removes older copies
HISTIGNORE='ls:ll:bg:fg:history:clear:exit'
HISTTIMEFORMAT='%F %T  '   # timestamp format (strftime) for `history`; also written to the file
shopt -s histappend        # append, don't overwrite, on shell exit
shopt -s cmdhist lithist   # multi-line commands saved as one entry, with newlines
PROMPT_COMMAND='history -a'   # append new lines to the file after every command
```
- Without `histappend`, bash overwrites the history file at exit.
- `history -a` appends this session's new lines; `history -n` reads lines other sessions
  appended since this one started (`history -a; history -n` shares between tabs).
- `HISTCONTROL=ignorespace` skips lines that begin with a space.
- HISTIGNORE patterns must match the whole line; they are tested after HISTCONTROL.

## 2. Using history
```bash
history 20                # last 20 entries; with HISTTIMEFORMAT shows times
Ctrl-R  text             # reverse incremental search; Ctrl-G aborts
!!                       # last command;  sudo !!
!$   !^   !*             # last arg, first arg, all args of previous command
!ssh                     # last command starting with ssh;  !?string? contains
^old^new                 # rerun last command with substitution
!!:p                     # print, don't run
fc -l -20                # list; fc -e vim ... edits and re-runs
shopt -s histverify      # history substitution result is loaded into the line for editing
```
`histverify` lets you review the expansion (e.g. `rm !$`) before it runs. History expansion
is on by default in interactive shells and off in non-interactive ones; `set +H` disables it.

## 3. Shared vs per-session
- Default: each shell writes the file at exit, so tabs do not see each other until then.
  Section 1 fixes that.
- A separate file per host or user: set `HISTFILE` in the startup file.

## 4. Secrets and cleanup
```bash
history -d 1234          # delete entry from the list (then history -w to write the file)
history -c; history -w   # clear the list, then overwrite the file
unset HISTFILE           # this session's history is not saved at exit
```
If `HISTFILE` is unset or null, the history is not saved. Commands with inline passwords
end up in the file unless skipped (leading space with `ignorespace`).

## 5. Audit expectations
Bash history is a convenience, not an audit trail: the user controls the variables and the
file. Use a proper audit mechanism for accountability.

## Failure modes
- History from one tab lost: no `histappend`/`history -a`.
- Commands with leading space still recorded: `HISTCONTROL` lacks `ignorespace`.
- `history` shows no timestamps: `HISTTIMEFORMAT` unset or null in that shell.

## Verify
- [ ] Open two terminals, run a distinct command in each, exit both: both are in the history file.
- [ ] ` echo secret` (leading space) does not appear in `history`.

## Checked
2026-11-01: confirmed against the bash man page (man7.org) HISTCONTROL, HISTIGNORE, HISTFILESIZE, HISTTIMEFORMAT, histappend, histverify, cmdhist, lithist, history -a/-n/-c/-d/-w, fc, history expansion designators and `set +H`. Removed: file-permission default, crash and ordering remarks, per-sudoer HISTFILE, auditd/sudo/tlog/chattr specifics, error-message and load-time remarks.
Method: documentation only; no commands were run.
