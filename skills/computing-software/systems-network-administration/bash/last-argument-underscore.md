---
id: computing-software.systems-network-administration.bash.last-argument-underscore
name: last-argument-underscore
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, last-argument-underscore, dollar-underscore, shell-scripting]
level: advanced
status: docs-checked
description: "Use bash $_ and Esc-dot to reuse the last argument of the previous command, and know the other special variables."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# $_ last argument
**Goal:** reuse the previous command's final word.
```bash
mkdir -p /srv/app/releases/v2 && cd "$_"     # $_ = last arg of previous command
cp big.iso /mnt/usb/; echo "$_"              # /mnt/usb/
# interactive readline: M-. (yank-last-arg) inserts the last word of the previous line
```
- `$_` is set after each simple command to its last argument; at shell start it holds the invoked path; in `MAILPATH` checks it is the mail filename.
- It is overwritten by every command, including `echo`: use it on the very next command.
- Self-check: `echo a b; echo "$_"` prints `b`.

## Checked

2026-11-02: Confirmed in Bash Variables / Special Parameters (`$_`: last argument of the previous simple command, invoked path at startup, mail file name when checking mail) and Commands For Manipulating The History (yank-last-arg, M-. or M-_). Removed: POSIX claim and the `!$` history shortcut.
Source read: GNU Bash Reference Manual (https://www.gnu.org/software/bash/manual/bash.html).
Method: documentation only; no commands were run.
