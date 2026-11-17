---
id: computing-software.systems-network-administration.bash.sed-address-ranges
name: sed-address-ranges
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, sed-address-ranges, sed-ranges, shell-scripting]
level: practitioner
status: docs-checked
description: "Address lines in sed by number, last line, regex and range, with -n, p, d, negation and the POSIX rules for them."
sources:
  - https://pubs.opengroup.org/onlinepubs/9799919799/utilities/sed.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sed addresses and ranges
**Goal:** operate on exactly the lines you mean.
```bash
sed -n '5,10p' f            # lines 5-10
sed '1d;$d' f               # delete first and last
sed -n '/START/,/END/p' f   # regex range
sed '/^#/d;/^$/d' f         # drop comments and blank lines
sed -n '$=' f               # print the last line number
sed '/pat/!d' f             # keep only matching lines (negation)
sed -n '/old/s//new/p' f    # empty RE reuses the last RE
```
- POSIX sed (synopsis `sed [-En] script [file...]`, plus `-e` and `-f`) has no `-i`; in-place editing, step addresses like `0~3`, and `\+` / `\|` in basic REs are implementation extensions that this POSIX page does not define.
- An address is a decimal line number (counted cumulatively across files), `$` for the last line of input, or a context address `/RE/` or `\cREc`.
- No address selects every line; one address selects each line that matches; two addresses select the inclusive range from the first line matching the first address through the next line matching the second. If the second address is a number less than or equal to the line first selected, only one line is selected. After the range, sed looks again for the first address.
- `!` before a function applies it where the addresses do not select the line. Do not put blanks after the `!`.
- `-n` suppresses the default output: only lines selected by the script (for example with `p`) are written. `-E` selects extended REs instead of basic ones.
- `=` writes the current line number; in `[1addr]=` form it takes one address.
- `\n` in a sed RE matches an embedded newline in the pattern space; a literal newline must not be used in a context address RE.
- Self-check: `seq 10 | sed -n '3,4p'` prints 3 and 4.

## Checked
2026-11-09. Confirmed in the POSIX sed page: synopsis and options, address forms, one- and two-address semantics, `!`, `=`, `-n`, `-E`, empty-RE rule, `\n`. Removed: `sed -i` / `-i.bak` portability notes and BSD remarks, GNU step addressing, the claim that an unterminated range runs to end of file (the page only describes ranges that end), and the GNU manual source (not readable).
Method: documentation only; no commands were run.
