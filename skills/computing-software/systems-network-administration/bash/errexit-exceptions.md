---
id: computing-software.systems-network-administration.bash.errexit-exceptions
name: errexit-exceptions
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, errexit-exceptions, errexit-pitfalls, shell-scripting]
level: advanced
status: docs-checked
description: "Know where bash set -e does not trigger: conditions, && and || lists, negation, command substitution and functions in tests."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# When set -e is ignored
**Goal:** avoid trusting errexit where it is silently off.
```bash
set -e
false || true            # ok: part of an || list
if false; then :; fi     # conditions never trigger exit
! false                  # negated commands never trigger exit
f() { false; echo "still runs"; }
f || echo handled        # inside f errexit is DISABLED because of ||
x=$(false)               # DOES exit: a plain assignment takes the substitution's status
```
- errexit is ignored in any command whose status is tested (if/while/until conditions, `&&`/`||` except the last, `!`), and inside functions called in such contexts.
- Command substitution does not inherit errexit unless `shopt -s inherit_errexit` is set.
- Explicit checks are more reliable: `cmd || { log fail; exit 1; }`.
- Self-check: `set -e; f(){ false; echo reached; }; f || :` prints reached.

## Checked

2026-11-02: Confirmed in The Set Builtin (`-e`: not triggered in while/until/if tests, in && or || lists except the last command, for `!`, or in a function or compound command running where -e is ignored) and Simple Command Expansion (status of an assignment-only command is the last command substitution) and shopt `inherit_errexit`. Removed: local-masks-status claim and version tag.
Source read: GNU Bash Reference Manual (https://www.gnu.org/software/bash/manual/bash.html).
Method: documentation only; no commands were run.
