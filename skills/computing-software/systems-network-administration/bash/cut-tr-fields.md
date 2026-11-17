---
id: computing-software.systems-network-administration.bash.cut-tr-fields
name: cut-tr-fields
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, cut-tr-fields, cut-fields, shell-scripting]
level: intro
status: docs-checked
description: "Extract fields and transform characters with cut and tr in pipelines, with delimiters, byte versus character mode and squeeze."
sources:
  - https://pubs.opengroup.org/onlinepubs/9799919799/utilities/cut.html
  - https://pubs.opengroup.org/onlinepubs/9799919799/utilities/tr.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cut and tr for field extraction
**Goal:** simple columns without awk.
```bash
cut -d: -f1,3 /etc/passwd          # fields 1 and 3, colon-delimited
cut -d, -f2- file.csv              # field 2 to the last field
cut -c1-8 file                     # characters 1 to 8 (-b selects bytes)
echo "$x" | tr '[:lower:]' '[:upper:]'   # case conversion with classes
tr -d '\r' < dos.txt               # delete carriage returns
tr -s ' ' <<< "a    b"              # squeeze repeated spaces to one
tr -cd '[:alnum:]\n' < f           # delete everything except alphanumerics and newline
```
- `cut` selects bytes (`-b`), characters (`-c`) or delimiter-separated fields (`-f`). `-d delim` sets the field delimiter to one character; the default is tab. Selected output fields are joined with a single delimiter.
- A list is comma- or blank-separated numbers and ranges: `N`, `N-M`, `-M`, `N-` (to the last).
- `cut -f` passes lines that contain no delimiter through unchanged unless `-s` is given, which suppresses them. It is not an error to select fields that are not present.
- `cut` writes selected fields in input order, each at most once: `-f3,1` prints field 1 then field 3. Reordering needs another tool.
- Because every delimiter occurrence separates fields, repeated spaces give empty fields; squeeze them first with `tr -s ' '`.
- `tr` copies standard input to standard output; it takes no file operands. `-d` deletes the characters in string1, `-s` replaces repeated occurrences with one, `-c` / `-C` complement string1 (`-C` by characters, `-c` by values).
- `tr` supports `\\ \a \b \f \n \r \t \v` and `\octal` escapes, and classes such as `[:alnum:]`. A `c-c` range is defined only in the POSIX locale; in other locales its behavior is unspecified, so prefer classes.
- With `tr string1 string2`, a string2 shorter than string1 gives unspecified results; an empty string1 or string2 produces undefined results.

## Checked
Date: 2026-11-07
Method: Read the POSIX cut and tr utility pages in full (options, operands, lists, escapes, classes, ranges, -d/-s/-c/-C rules, rationale example). Corrections: replaced `tr 'a-z' 'A-Z'` with class-based case conversion because ranges are only defined in the POSIX locale. Removed the claims that tr "works on bytes" and that multibyte UTF-8 is better handled by `sed`, `awk` or `perl -CS`, and the `awk` fallback for cut (none are on the pages), and kept the self-check out because its output is not stated in the specs.
