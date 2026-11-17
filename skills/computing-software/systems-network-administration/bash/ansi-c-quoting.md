---
id: computing-software.systems-network-administration.bash.ansi-c-quoting
name: ansi-c-quoting
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, ansi-c-quoting, dollar-single-quote, shell-scripting]
level: practitioner
status: docs-checked
description: "Embed newlines, tabs and escapes in bash strings with dollar-single-quote ANSI-C quoting, and know where POSIX 2024 matches it."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
  - https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ANSI-C quoting: $'...'
**Goal:** write control characters literally without printf or echo -e.
```bash
nl=$'\n'; tab=$'\t'
printf '%s\n' $'line1\nline2' $'\x41' $'it\'s'
[[ $'a\tb' == *$'\t'* ]] && echo has-tab
```
- `$'string'` is a special kind of single quote: backslash escapes in `string` are decoded and "the expanded result is single-quoted, as if the dollar sign had not been present".
- Bash decodes: `\a \b \e \E \f \n \r \t \v \\ \' \" \?`, `\nnn` (octal, one to three digits), `\xHH` (one or two hex digits), `\uHHHH`, `\UHHHHHHHH` and `\cx` (control-x). `\e` and `\E` are an escape character "not in ANSI C".
- Inside `$'..'` a single quote is written `\'`. In ordinary single quotes a single quote cannot occur, even preceded by a backslash.
- POSIX.1-2024 (Issue 8) specifies dollar-single-quotes too (section 2.2.4), but with a smaller set: `\" \' \\ \a \b \e \f \n \r \t \v \cX \xXX \ddd`. It does not list `\E`, `\?`, `\u` or `\U`; and for `\xXX` more than two hex digits give unspecified results. Older shells that predate that edition may not support the syntax, so check the target shell before using it in `#!/bin/sh` scripts.
- If `\xXX` or `\ddd` yields a zero byte, POSIX says it is unspecified whether the null byte is kept or that byte and the rest up to the closing quote are discarded.
- POSIX says an unescaped backslash followed by any other character is unspecified.

## Checked
Date: 2026-11-07
Method: Read GNU Bash manual section 3.1.2 Quoting (escape character, single quotes, double quotes, ANSI-C Quoting) and POSIX Shell Command Language 2.2.4 Dollar-Single-Quotes in full. Corrections: replaced the draft's "Not POSIX" claim (POSIX.1-2024 now defines `$'...'`), `\0NNN` became `\nnn` (the manual documents one to three octal digits with no leading 0), added the missing `\b`, `\E`, `\?`, `\U`. Removed the unsourced claims about dash output, the portable `printf` workaround, "bash cannot hold NUL in variables", the `$'é'` example and the `IFS=$' \t\n'` line (the manual page does not state a default IFS in the section I read).
