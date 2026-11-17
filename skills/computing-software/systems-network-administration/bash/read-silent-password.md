---
id: computing-software.systems-network-administration.bash.read-silent-password
name: read-silent-password
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, read-silent-password, read-s-silent, shell-scripting]
level: practitioner
status: docs-checked
description: "Read passwords in bash with read -s without echo, keep the value out of arguments, and clean up the variable."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Silent input with read -s
**Goal:** prompt for a secret without echoing it.
```bash
read -r -s -p "Password: " pw; echo          # -s hides input; echo adds the newline
some_cmd <<<"$pw"                             # pass on stdin (here-string), not as an argument
unset pw
```
- `read -s`: silent mode; if input is coming from a terminal, characters are not echoed.
- `read -p prompt` shows the prompt without a trailing newline, but only if input comes from a terminal. That is why the example adds an `echo` afterwards.
- `read -r` stops backslash acting as an escape character, so the secret is stored as typed.
- `read -t seconds` makes read time out and return a status greater than 128; `-N nchars` reads exactly that many characters.
- With no terminal (cron, pipes) there is nothing to prompt: read the secret from a file or descriptor (`read -u fd`) with restrictive permissions instead.
- Prefer passing the value on stdin over putting it in a command argument, and keep `set -x` off around it (practice advice, not from the manual).
- Self-check: `read -r -s v` shows no characters while typing, and `echo "${#v}"` prints the length typed.

## Checked
Checked 2026-11-08 against the Bash Reference Manual `read` builtin (options -r, -s, -p, -t, -N, -u). Removed: the kinit/curl examples, the stty echo-restore advice and the `stty -a` self-check, which the manual does not cover.

Method: docs-only read of cited pages, 2026-11-08
