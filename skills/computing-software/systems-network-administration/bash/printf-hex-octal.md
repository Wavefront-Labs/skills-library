---
id: computing-software.systems-network-administration.bash.printf-hex-octal
name: printf-hex-octal
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, printf-hex-octal, printf-hex, shell-scripting]
level: practitioner
status: docs-checked
description: "Convert numbers and characters with bash printf: hex, octal, ASCII codes, Unicode escapes and base#n arithmetic."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
  - https://pubs.opengroup.org/onlinepubs/9799919799/utilities/printf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hex, octal and char conversion
**Goal:** convert between representations.
```bash
printf '%x\n' 255        # ff       (hexadecimal)
printf '%o\n' 8          # octal
printf '%d\n' 0xff       # 255      (0x prefix is a C hex constant)
printf '%d\n' "'A"       # 65       (leading quote: value of the next character)
printf '%b\n' '\x41'     # A        (%b expands echo -e style escapes)
printf '%b' 'a\tb\n'     # tab and newline escapes in an argument
printf '%q\n' 'a b'      # quote for reuse as shell input
echo $((2#1010))         # binary constant read as base 2
echo $((10#08))          # forces base 10 so the leading 0 is not octal
```
- Arguments to numeric conversions are treated as C constants, plus an optional leading `+` or `-`. If the first character is a single or double quote, the value is the numeric value of the following character in the current locale.
- A leading `0` means octal, so `printf '%d' 08` is a conversion error (the 8 is not an octal digit); use `$((10#08))`. Arithmetic constants take the form `[base#]n`, base 2 to 64.
- `%b` expands backslash escapes in the argument "in the same way as `echo -e`": that includes `\xHH` (one or two hex digits), `\0nnn`, `\uHHHH` and `\UHHHHHHHH`. `%s` prints the argument as is.
- `%q` outputs the argument in a form that can be reused as shell input.
- printf has no binary output conversion: the conversions are `cCsSndiouxXeEfFgGaA` plus bash's `%b`, `%q`, `%Q`, `%(datefmt)T` and `%n`. Convert to binary with your own loop or an external tool.
- With more arguments than conversions the format is reused for each remaining argument; with too few, missing arguments act as zero or the null string.

## Checked
Date: 2026-11-07
Method: Read the GNU Bash manual printf builtin entry, the echo escape list (\xHH, \0nnn, \u, \U), and the arithmetic constants paragraph ([base#]n, leading 0 octal, 0x hex); read the POSIX printf utility page (conversion errors, quote-character rule, format reuse, missing arguments). Trims: removed the `%#o` example (the # flag is not documented on either page), the `printf '\x41'` form (the manual lists \xHH under echo -e and %b, not for the format string), the `é` example, the `xxd` pipeline, the `bc` binary tip, the unsourced "bash 4" style comments, and the invented Verify step. Searched the large manual page by entry rather than reading all of it.
