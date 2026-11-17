---
id: computing-software.software-engineering.perl.one-liner-switches
name: one-liner-switches
category: computing-software
field: software-engineering
product: perl
tags: [perl, one-liner, perl-e, perl-n, perl-p, perl-i, perlrun, one-liner-switches, perl-text-processing]
level: practitioner
status: docs-checked
description: "Use perl -e/-E, -n, -p, -i, -l, -a, -F, -0 and -M for sed/awk-style edits, with the documented backup-extension rules for in-place editing."
sources: ["https://perldoc.perl.org/perlrun"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Command-line switches and one-liners

**Goal:** fast text surgery from the shell.

| Switch | Meaning (per perlrun) |
|---|---|
| `-e 'code'` | run one line of program; several `-e` build a multi-line script; perl then does not look for a filename |
| `-E` | like `-e`, but implicitly enables all optional features and builtin functions (for example `say`) |
| `-n` | wrap the program in `while (<>) { ... }`; lines are not printed |
| `-p` | like `-n` with an automatic `print` after each iteration; `-p` overrides `-n` |
| `-l[octnum]` | chomp `$/` on input with `-n`/`-p`, and set `$\` (to octnum, or to the current `$/` if omitted) so prints get a line ending |
| `-a` | autosplit into `@F` as the first thing in the `-n`/`-p` loop; implicitly sets `-n` |
| `-Fpattern` | split pattern for `-a`; implicitly sets `-a` and `-n`; no literal whitespace or NUL in the pattern |
| `-i[ext]` | edit `<>` files in place, optionally keeping a backup (rules below) |
| `-0[digits]` | set `$/` from an octal or hex number; `-00` is paragraph mode; 0400 or above slurps whole files, by convention `-0777`; `-g` is an alias for `-0777` |
| `-M`/`-m` | `-Mmodule` is `use module;`, `-mmodule` is `use module ();` (no import); `-MMODULE=a,b` means `use MODULE split(/,/,q{a,b})`; a leading `-` gives `no` |
| `-I dir` | prepend a directory to the module search path (`@INC`) |
| `-c` | check syntax and exit (BEGIN, UNITCHECK, CHECK blocks and `use` still run; INIT and END are skipped) |
| `-w` / `-W` | `-w` enables the global `$^W` warnings (lexical `use warnings` is preferred); `-W` enables all warnings regardless of `no warnings` |
| `-T` / `-t` | taint checks (`-t` only warns, a temporary aid) |

```bash
perl -ne 'print if /ERROR/' app.log
perl -pe 's/foo/bar/g' in.txt > out.txt
perl -pi.bak -e 's/\bcolour\b/color/g' *.txt           # keeps *.txt.bak
perl -lane 'print $F[2]' data.txt                     # third whitespace field
perl -F, -lane 'print "$F[0]:$F[1]"' data.csv         # naive CSV (no quotes)
perl -0777 -pe 's/\n{3,}/\n\n/g' file                 # slurp then squeeze blank lines
perl -MList::Util=sum -lane '$s += $F[0]; END { print $s }' nums
perl -E 'say for 1..3'
```

## In-place editing rules (`-i`)
- It renames the input file, opens a new file under the original name and selects it for `print`.
- No extension (and the system supports it): the original is kept open without a name and unlinked when perl exits; no backup remains.
- An extension without `*` is appended to the filename (`-i.orig` gives `fileA.orig`). Each `*` in the extension is replaced by the filename, so `-i'orig_*'` backs up to `orig_fileA` and `-i'old/*.orig'` into an existing directory `old/`.
- Perl creates the backup whether or not any output changed. If the backup cannot be created, that file is skipped.
- It cannot create directories or strip extensions, and it does not preserve Unix soft or hard links (the original is renamed or deleted).
- With no files given, no backup is made and processing runs from STDIN to STDOUT.

## Rules
- `-n`/`-p` programs can use `BEGIN { }` and `END { }` to run before or after the implicit loop, as in awk.
- `-l` copies `$/` to `$\` when the switch is processed, so the order of `-l` and `-0` matters: `-ln0e` sets `$\` to newline then `$/` to the null character.
- The `#!` line is examined for switches. `-T` must be seen early by perl, so put it early on the command line or in the `#!` line; the docs say `-C` on the `#!` line must also be on the command line.
- `<>` passes command-line arguments to `open`, which does not necessarily treat them as filenames; perlrun points to perlop for the security implications.

## Self-check
- [ ] `printf 'a b\nc d\n' | perl -lane 'print $F[1]'` prints `b` then `d`.

## Checked

Date: 2026-11-08. Confirmed against the perlrun page on perldoc.perl.org: each switch row above (-e, -E, -n, -p, -l, -a, -F, -i with its extension rules and caveats, -0 and -g, -M/-m, -I, -c, -w, -W, -T, -t), the -l and -0 ordering example, and the #! line notes. Removed: the Windows quoting and "-i may refuse without an extension on Windows" claims, the flip-flop line-range example, the JSON::PP/CSV parser advice and the claim that -E enables the "current feature bundle", which differ from or go beyond what the page states.

Method: docs-only read of cited pages, 2026-11-08
