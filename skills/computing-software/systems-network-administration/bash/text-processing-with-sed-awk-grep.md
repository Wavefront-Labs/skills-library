---
id: computing-software.systems-network-administration.bash.text-processing-with-sed-awk-grep
name: text-processing-with-sed-awk-grep
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, shell, text-processing, grep, egrep, ripgrep, rg, sed, sed-in-place, awk, gawk, mawk, regex, bre, ere, pcre, cut, sort, uniq, tr, join, comm, column, xargs, jq, log-parsing, field-separator, ofs, nr, fnr, csv, locale, lc-all, gnu-vs-bsd, one-liners, pipelines]
level: practitioner
status: gated
description: "Process logs and configs with grep, sed and awk: regex flavours, safe in-place edits, field and aggregate one-liners, sort/uniq pipelines, GNU vs BSD, and when to use jq instead."
sources:
  - https://www.gnu.org/software/sed/manual/sed.html
  - https://www.gnu.org/software/gawk/manual/gawk.html
  - https://www.gnu.org/software/grep/manual/grep.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Text processing with sed, awk and grep — the admin's pipeline toolkit

**Goal:** answer questions about logs and edit config files from the shell, quickly and
correctly — and recognise when a one-liner has become a liability.

**Pick the tool:** `grep` to *select lines*, `sed` to *rewrite lines*, `awk` to work
with *fields and aggregates*. If you need all three in one pipeline, awk alone can
usually do it.

## 1. grep
```bash
grep -rn --include='*.conf' 'listen' /etc/nginx/      # recursive, line numbers, filtered
grep -E 'ERROR|FATAL' app.log | grep -v healthcheck     # ERE alternation, exclude
grep -c 'status=500' access.log                         # count matching lines
grep -oE '[0-9]{1,3}(\.[0-9]{1,3}){3}' auth.log | sort | uniq -c | sort -rn | head
grep -F -f blocklist.txt access.log                     # fixed strings from a file (fast)
grep -A3 -B1 'Traceback' app.log                        # context
zgrep 'pattern' app.log.*.gz                            # rotated, compressed logs
```
- Regex flavours: `grep` = BRE (`\+`, `\|` are GNU extensions), `-E` = ERE, `-P` = PCRE
  (GNU only; `\d`, lookarounds; needs a locale grep's PCRE support accepts, e.g. a UTF-8 or unibyte one). `\d` does **not** work without `-P` (tested: BRE `\d` matched nothing).
- `-q` for tests in scripts; exit 1 means "no match", 2 means error.
- `ripgrep` (`rg`) is much faster on large trees and respects `.gitignore` — often hides
  files you wanted; add `-uu` (`-u` stops honouring `.gitignore`, `-uu` also searches hidden files; `-uuu` adds binary files: ripgrep GUIDE).

## 2. sed
```bash
sed -n '120,140p' big.log                      # print a range
sed -n '/^\[mysqld\]/,/^\[/p' my.cnf           # print a section
sed -i.bak 's/^#\?PermitRootLogin .*/PermitRootLogin no/' /etc/ssh/sshd_config
sed -E 's/(user=)[^ ]+/\1REDACTED/g' app.log   # capture groups with -E
sed '/^\s*#/d; /^\s*$/d' file.conf             # strip comments and blank lines
```
- **In-place differs:** GNU `sed -i[SUFFIX]` takes an attached suffix; FreeBSD's man page shows the extension as a separate word (`sed -i '' -e ...`). `sed -i.bak` as a portable form is common practice (gated: unconfirmed, source is paywalled or blocked), then remove the `.bak`.
- `sed -i` replaces the file (new inode): it breaks hard links and can reset
  ownership/SELinux context in some cases; for symlinked targets use
  `--follow-symlinks` (GNU; listed in `sed --help`, behaviour not run here because symlinks are emulated on this host).
- Pick another delimiter for paths: `s|/old/path|/new/path|g`.
- Before editing configs, preview without `-i`, then validate (`sshd -t`, `nginx -t`).
  For anything structural (YAML, JSON, INI with sections) prefer a real tool or
  config management — regex edits drift.

## 3. awk
```bash
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head      # top client IPs
awk '$9 >= 500 {c[$9]++} END {for (s in c) print s, c[s]}' access.log
awk -F: '$3 >= 1000 {print $1}' /etc/passwd                         # custom separator
awk '{sum+=$NF; n++} END {if (n) printf "avg=%.2f n=%d\n", sum/n, n}' times.txt
awk 'NR==FNR {bad[$1]; next} $1 in bad' blocklist.txt access.log     # join two files
awk -v OFS='\t' '{print $1, $4}' file                                # tab-separated output
df -P | awk 'NR>1 && $5+0 > 90 {print $6, $5}'                       # skip header, numeric compare
```
- `$0` whole line, `$NF` last field, `NR` total line number, `FNR` per-file. The
  `NR==FNR` idiom processes the first file into an array, then filters the second.
- Default field splitting collapses whitespace runs; with `-F','` empty fields count.
  **awk does not understand quoted CSV** (`"a,b",c`) — use `gawk --csv` (gawk 5.3.0 NEWS; gawk 5.0.0 rejects it),
  `mlr`, `csvkit` or Python.
- `$5+0` forces numeric comparison (`"9%" > "10%"` is true as strings).
- mawk (Debian's default `awk`) documents `strftime` as available (mawk 1.3.4) but has no `asort` or `gensub`; call `gawk` explicitly when you use gawk features.

## 4. The pipeline helpers
`cut -d: -f1,7`, `tr -s ' '` (squeeze), `sort -t, -k3,3n` (numeric on field 3),
`sort -h` (human sizes), `uniq` (needs **sorted** input), `comm -13 a b` (lines only in b;
both sorted), `column -t` (align), `xargs -0` with `find -print0`.

## 5. Gotchas that produce wrong answers silently
- **Locale:** `sort`, ranges like `[a-z]`, and case-folding depend on `LC_ALL`. For
  byte-wise, reproducible results and speed: `LC_ALL=C sort`.
- `grep pattern file | wc -l` vs `grep -c`: same, but `grep -o ... | wc -l` counts
  *matches*, not lines.
- Windows line endings: `\r` makes `$NF` comparisons and `==` fail invisibly (gated: unconfirmed, source is paywalled or blocked); strip with
  `tr -d '\r'` or `sed 's/\r$//'`.
- Log lines with variable field counts (user agents with spaces) shift awk fields; anchor
  on a regex or split on quotes (`-F'"'`).
- JSON logs: use `jq` (for example `jq -r 'select(.level=="error") | .msg'`; jq was not installed here, so that filter was not run (gated: unconfirmed, source is paywalled or blocked)), never grep fields out.
- When a one-liner grows past ~3 pipes or needs state across lines, write a short
  awk script file or Python — and test it on a sample with known answers.

**Unconfirmed:** `gawk --csv` availability depends on distro gawk version; BSD tools
on macOS differ in more flags than listed here.

## Verify
- [ ] Spot-check the one-liner's answer on a small sample you can count by hand.
- [ ] In-place edits were previewed, a `.bak` kept, and the service config validated.
- [ ] Sorting/counting ran with `LC_ALL=C` where reproducibility matters.
- [ ] No CSV or JSON was parsed with field splitting or regex.
