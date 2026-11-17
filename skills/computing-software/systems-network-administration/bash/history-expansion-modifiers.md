---
id: computing-software.systems-network-administration.bash.history-expansion-modifiers
name: history-expansion-modifiers
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, history-expansion-modifiers, history-designators, shell-scripting]
level: advanced
status: docs-checked
description: "Use bash history expansion: !!, !$, !^, word designators, :s substitution and modifiers, plus safe handling in scripts."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# History expansion designators and modifiers
**Goal:** reuse earlier commands accurately.
```bash
sudo !!                 # rerun last command with sudo
!$ ; !^ ; !*            # last arg ; first arg ; all args of previous command
!ssh                    # last command starting with ssh
!?pattern?              # last command containing pattern
^old^new                # substitute in the previous command
!!:s/a/b/ ; !!:gs/a/b/  # substitute once / globally
!:2-3                   # words 2..3
cd !$:h                 # modifier :h dirname, :t basename, :r strip extension
!!:p                    # print without executing
```
- History expansion is on by default in interactive shells (`set +H` disables it); non-interactive shells have it off unless `set -H` is used. `!` inside double quotes can still expand; single quotes and a backslash inhibit it.
- A `!` followed by space, tab, newline, `=` or another shell metacharacter does not start an expansion, and a `!` immediately before the closing double quote is treated as quoted, so `echo "Hello!"` is safe but `echo "Hello!you"` tries to expand `!you`.
- Preview with `:p`, or with `history -p`; `shopt -s histverify` (with Readline) loads the expansion into the edit buffer before it runs, and `histreedit` reloads a failed expansion for correction.
- `^old^new^` is shorthand for `!!:s^old^new^`. `g` (or `a`) applies `s` over the whole event line and `G` applies it once to each word; `&` repeats the previous substitution.
- Word 0 is the command word; `$` is the last word (word 0 if the line has only one word) and `*` is words 1 to last.
- Self-check: `echo a b; echo !$` prints `b`.

## Checked
2026-11-08. Confirmed against the Bash Reference Manual, History Expansion chapter (event designators, word designators, modifiers, quoting rules, `histverify`, `histreedit`, `history -p`, `set +H`/`-H`). Corrected the claim that `echo "Hello!"` triggers an error: the manual treats a `!` right before the closing double quote as quoted. Removed the quoted error text "event not found", which the manual does not give.
Method: documentation only; no commands were run.
