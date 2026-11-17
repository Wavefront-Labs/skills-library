---
id: computing-software.systems-network-administration.linux.writing-man-pages
name: writing-man-pages
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, writing-man-pages, groff, man-pages, pandoc, scdoc, roff, help2man, documentation]
level: practitioner
status: docs-checked
description: "Write and ship a man page for your own tool: roff man macros vs pandoc/scdoc/help2man sources, section numbering, install paths, mandb indexing and linting."
sources:
  - https://man7.org/linux/man-pages/man7/man-pages.7.html
  - https://man7.org/linux/man-pages/man7/man.7.html
  - https://pandoc.org/MANUAL.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Writing man pages

## Sections
1 user commands, 5 file formats, 7 overviews, 8 admin commands. Name the file `mytool.1` / `mytool.conf.5`.

## Easiest: write Markdown, generate roff
```markdown
% MYTOOL(1) mytool 1.4 | User Commands
% Ops Team
% October 2026

# NAME

mytool - rotate application secrets

# SYNOPSIS

**mytool** [**-n**] [**-c** *file*] *target*...

# OPTIONS

**-n**, **\--dry-run**
:   Show what would change.

# EXIT STATUS

0 success, 1 error, 2 usage.

# SEE ALSO

**vault**(1)
```
`pandoc -s -t man mytool.1.md -o mytool.1`. The title line is `% TITLE(section) footer | header`; pandoc takes the date from the third `%` line.
Two traps (run with pandoc 3.13): a `#` heading needs a blank line before it, otherwise pandoc treats the whole file as one paragraph and the page is garbage; and pandoc's smart typography turns `--` into an en dash, so `**--dry-run**` renders as `\(endry-run`. Write `\--dry-run` (as above) or convert with `-f markdown-smart`.

## Hand-written roff (man macros)
```roff
.TH MYTOOL 1 2026-10-18 "mytool 1.4" "User Commands"
.SH NAME
mytool \- rotate application secrets
.SH SYNOPSIS
.B mytool
.RB [ \-n ]
.I target
.SH OPTIONS
.TP
.BR \-n ", " \-\-dry\-run
Show what would change.
```
Escape hyphens in options as `\-`.

## Install and index
```bash
install -Dm644 mytool.1 /usr/local/share/man/man1/mytool.1
gzip -9 /usr/local/share/man/man1/mytool.1      # optional; packages usually compress
mandb -q                                          # so man -k finds it (-q: no warnings)
```
The directory must be on the man path (see `manpath`, `/etc/manpath.config`).

## Lint
`man --warnings -E UTF-8 -l mytool.1 >/dev/null` (man-db: groff warnings, local file).

## Verify
- [ ] `man mytool` renders; `man -k mytool` finds it; no warnings from `man --warnings -l`.

## Checked
2026-10-27. Checked against the Pandoc User's Guide (man page title line and variables), man-pages man(7) (.TH arguments, macro usage and escaped hyphens), man-pages man-pages(7) (section meanings) and Debian man(1) (-l, --warnings, -E) and mandb(8). Confirmed: pandoc -t man with the title block `% PAGE(1) footer | header`; .TH title section date source manual; .SH, .B, .I, .BR, .RB and .TP macros and \- hyphens; man -l and --warnings; mandb -q. Removed: scdoc and help2man alternatives, the mandoc and lintian lint tools, debhelper and RPM packaging names, and the /usr/local/share/man default location, none of which were confirmed from readable sources.

Run 2026-11-01: the corrected Markdown example through `pandoc -s -t man` (pandoc 3.13) produced `.TH "MYTOOL" "1" "October 2026" "mytool 1.4" "User Commands"`, `.SH` sections, a `.TP` option entry with `\-\-dry\-run`, and the author as `.SH AUTHORS`; the original example (no blank lines, unescaped `--`) produced the broken output described above. Not run (no man-db, groff or mandb here, so status stays docs-checked): the hand-written roff, `install`, `gzip`, `mandb -q`, `man --warnings -l`.

Method: documentation, plus the pandoc conversion run locally; the man-db and groff steps were not run.
