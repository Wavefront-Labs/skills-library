---
id: computing-software.systems-network-administration.bash.bash-printf-formatting
name: bash-printf-formatting
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, printf, bash-printf, format-strings, printf-v, padding, alignment, tables, printf-q, date-format, echo-vs-printf, shell-scripting, lpic-1, sysadmin]
level: practitioner
status: verified
description: "Produce reliable output with bash printf: why not echo, width/precision/alignment for tables, %q shell-quoting, -v assignment, %(fmt)T timestamps, repeating formats over arguments, and escapes."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html#Bash-Builtins
  - https://man7.org/linux/man-pages/man1/printf.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# printf — output you can predict

**Goal:** print values exactly (no surprise `-n`/`-e` behaviour), build aligned reports,
and quote strings safely for re-use.

## 1. Why printf over echo
```bash
echo "$var"          # if var is "-n" or "-e" the option is eaten; backslash handling varies by shell/xpg_echo
printf '%s\n' "$var" # always prints the value, then newline
printf '%s\n' "${arr[@]}"   # one per line — the format REPEATS for extra arguments
printf '%s' "$x"     # no trailing newline
```
Treat `echo` as fine for literal messages, `printf '%s\n'` for anything variable.

## 2. Conversions
`%s` string, `%d` integer, `%f` float, `%x %o` hex/octal, `%e`, `%c` first char,
`%b` interpret backslashes in the argument, `%q` shell-quote, `%%` literal percent,
`%(fmt)T` strftime.
```bash
printf '%5d|%-10s|%8.2f\n' 42 name 3.14159      # width 5 right; width 10 left; 8 wide 2 decimals
printf '%05d\n' 7                               # zero pad: 00007
printf '%+d %x %#x %o\n' 5 255 255 8             # +5 ff 0xff 10
printf '%.3s\n' abcdef                           # abc (truncate)
printf '%*d\n' 8 42                              # width from argument
printf "%'d\n" 1234567                           # thousands separators (locale)
```

## 3. Tables
```bash
printf '%-20s %10s %8s\n' HOST STATUS LOAD
while read -r h s l; do printf '%-20s %10s %8.2f\n' "$h" "$s" "$l"; done < data
printf '%-20.20s\n' "$longname"     # pad AND truncate to 20 → fixed column
printf '=%.0s' {1..40}; echo        # a line of 40 '='
```
Width counts bytes or characters depending on version and locale (on bash 5.2 under msys `%-5s` padded `é` to 4 characters, i.e. by bytes); non-ASCII can misalign.
`column -t` is an alternative when the data is already delimited.

## 4. Special uses
```bash
printf -v out '%s-%03d' "$prefix" "$n"   # -v: assign instead of print (no subshell)
printf '%q\n' "$path"                    # it\'s\ a\ \"test\" — safe to paste into a shell/ssh command
ssh host "$(printf '%q ' rm -rf -- "$dir")"
printf '%(%Y-%m-%d %H:%M:%S)T\n' -1      # now (-1), or epoch seconds; no date fork
printf '%(%F)T\n' "$(( $(printf '%(%s)T') - 86400 ))"   # yesterday
printf '%b\n' 'line1\nline2'             # backslashes in DATA (not format)
printf '\x1b[1;31m%s\x1b[0m\n' ERROR     # colours (escape in FORMAT)
printf '%s\0' "${files[@]}" | xargs -0 ...   # NUL delimiters
```

## 5. Argument handling
- Format reused until arguments are exhausted: `printf '%s=%s\n' a 1 b 2`.
- Missing arguments become empty/0; extra are cycled through again.
- Non-numeric to `%d`: "invalid number" warning, prints 0, exit 1.
- `--` ends options when the format starts with `-`: `printf -- '-%s\n' x`.

## Failure modes
- Output literally shows `\n`: backslashes in the argument with `%s` (use `%b` or put them
  in the format).
- Columns drift: a value longer than its width; use `%-20.20s`.
- `printf '%d' 08`: octal error — `10#$n`.
- Float locale: `printf '%.2f' 3.5` fails under a comma-decimal locale ("invalid number");
  `LC_NUMERIC=C` in scripts.
- `%q` output pasted into `sh`/dash: bash `$'...'` quoting is not POSIX.

## Verify
- [ ] `printf '%s\n' -n -e` prints both strings literally.
- [ ] A generated table viewed with `cat -A` has consistent column offsets.
