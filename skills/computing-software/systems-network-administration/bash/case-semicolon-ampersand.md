---
id: computing-software.systems-network-administration.bash.case-semicolon-ampersand
name: case-semicolon-ampersand
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, case-semicolon-ampersand, case-fallthrough-terminators, shell-scripting]
level: advanced
status: docs-checked
description: "Use bash case terminators ;; ;& and ;;& to control fallthrough and multi-pattern matching."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# case terminators ;; ;& ;;&
**Goal:** continue past the first matching case branch deliberately.
```bash
case $level in
  debug) enable_debug ;&        # run next branch body unconditionally
  info)  enable_info  ;&
  warn)  enable_warn  ;;        # stop here
esac
case $f in
  *.gz)  gz=1 ;;&               # keep testing later patterns
  *.tar.*) tar=1 ;;
esac
```
- `;;` stops; `;&` falls into the NEXT body without testing; `;;&` goes on testing the NEXT patterns.
- Patterns are globs, not regex; `|` separates alternatives.
- Self-check: `case a in a) echo 1;& b) echo 2;; esac` prints 1 then 2.

## Checked

2026-11-02: Confirmed in Conditional Constructs (case clause terminators `;;`, `;&`, `;;&` and their meaning). Removed: version, POSIX and macOS claims.
Source read: GNU Bash Reference Manual (https://www.gnu.org/software/bash/manual/bash.html).
Method: documentation only; no commands were run.
