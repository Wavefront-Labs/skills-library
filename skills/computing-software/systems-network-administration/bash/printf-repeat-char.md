---
id: computing-software.systems-network-administration.bash.printf-repeat-char
name: printf-repeat-char
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, printf-repeat-char, printf-padding-repeat, shell-scripting]
level: intro
status: docs-checked
description: "Repeat or pad characters with bash printf, such as ruler lines and zero padding, without seq or loops."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
  - https://pubs.opengroup.org/onlinepubs/9799919799/utilities/printf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Repeating characters with printf
**Goal:** draw separators and pad strings.
```bash
printf -v line '%40s' ''; echo "${line// /-}"    # 40 dashes
n=30; printf -v line "%${n}s" ''; echo "${line// /=}"
printf '%05d\n' 42                                # zero padded to width 5
printf '%-10s|%10s|\n' left right
printf '=%.0s' {1..20}; echo                      # format reused once per argument
```
- `printf -v var` assigns the output to `var` instead of printing it, so no command substitution is needed.
- `${var//pattern/string}` replaces every match of the pattern; `${line// /-}` turns each space into `-`.
- The format is reused as necessary to consume all arguments, so `'=%.0s'` with 20 arguments writes one `=` per argument (precision 0 writes none of the argument).
- Brace expansion happens before any other expansion and is strictly textual, so `{1..$n}` does not use the value of `n`. Build the width into the format with a variable instead, as in `"%${n}s"`.
- POSIX does not require `*` for width or precision taken from an argument, and says the `*` can instead be replaced in the format by shell variable substitution, which is why the examples use `"%${n}s"`.

## Checked
Date: 2026-11-07
Method: Read GNU Bash manual printf entry (-v, format reuse), Shell Parameter Expansion pattern substitution, and Brace Expansion (strictly textual, performed first, sequence expression x..y); read the POSIX printf utility page on `*` width and precision and on extra specifiers. Trims: removed the `tr` pipeline and `$COLUMNS` and `%*s` forms, the `seq` advice and the "use printf instead of echo" advice (not confirmed on the pages), and the invented `[ ${#line} -eq 40 ]` self-check. Read relevant sections rather than the whole 523k manual page.
