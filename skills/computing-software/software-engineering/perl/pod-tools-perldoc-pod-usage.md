---
id: computing-software.software-engineering.perl.pod-tools-perldoc-pod-usage
name: pod-tools-perldoc-pod-usage
category: computing-software
field: software-engineering
product: perl
tags: [perl, perldoc, podchecker, pod2man, pod2html, test-pod, pod-tools-perldoc-pod-usage]
level: practitioner
status: docs-checked
description: "Read and check documentation with perldoc, podchecker, pod2text/pod2man/pod2html and Test::Pod in the suite."
sources: ["https://perldoc.perl.org/perldoc", "https://perldoc.perl.org/podchecker", "https://perldoc.perl.org/pod2man", "https://perldoc.perl.org/Pod::Usage"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# perldoc, podchecker and pod2man

**Goal:** find, render and validate documentation.

```bash
perldoc perlop                       # core docs by name (perltoc lists them)
perldoc -f push ; perldoc -v '$/' ; perldoc -q 'sort a hash'   # function, variable, FAQ search
perldoc -m List::Util                # entire module: code plus unformatted pod
perldoc -l List::Util                # only the file name of the module found
perldoc -t Some::Module              # plain text converter instead of nroff
perldoc -T Some::Module              # send to STDOUT, no pager
perldoc -oman Some::Module           # pick another output format class
podchecker lib/My/Module.pm          # syntax check
pod2man --section=3 lib/My/Module.pm > my.3pm
```
Online: perldoc.perl.org (core docs).

## What the tools do (from their own docs)
- `perldoc -f NAME` extracts a built-in function from perlfunc; `-v NAME` a predefined variable from perlvar; `-q REGEX` searches FAQ question headings in perlfaq1-9; `-a NAME` an API function from perlapi.
- `-F` treats arguments as file names (no directory search), for reading a pod file by path. `-r` searches recursively, `-i` ignores case, `-u` shows raw pod source, `-D` describes the search.
- For simple names perldoc retries with a `perl` prefix, so `perldoc intro` finds `perlintro`.
- In a directory with `Makefile.PL` or `Build.PL`, perldoc adds `.` and `lib` first to its search path; the `PERLDOC` environment variable supplies default switches and `PERLDOC_PAGER`, `MANPAGER`, `PAGER` pick the pager. Run as the superuser, perldoc tries to drop privileges (see its SECURITY section before using `-U`).
- `podchecker [-help] [-man] [-quiet] [-(no)warnings] [file ...]` prints POD syntax errors to STDERR and a status line; exit status 0 means all files are ok, 1 means at least one file has syntax errors, 2 means at least one file contains no POD commands (1 overrides 2, so call it with one file for unambiguous results). Repeating `-warnings` to level two also flags unescaped `<` and `>`.
- `pod2man` options `--section`, `--release`, `--center`, `--date` and `--official` set the man page headers and footers; `--name` overrides the manual name, which otherwise is the uppercased base name of the file (for section 3 the module name is derived from a path like `.../lib/Pod/Man.pm`). `--errors=die|stderr|pod|none` sets the error style.
- `Pod::Usage`: `pod2usage($message)`, `pod2usage($exit_status)` or a hash with `-message`, `-exitval` and `-verbose`; verbosity 99 also needs `-sections`.

## Rules
- `perldoc Module` finds the module only if it is installed or on the search path; `perldoc -l` verifies which file is used.
- Document public API with examples that run (copy from the SYNOPSIS into a test).
- Keep `podchecker` clean for every `.pm` and script before release.

## Self-check
- [ ] `podchecker` exits 0 for every file with POD.

## Checked
2026-11-08. Confirmed against perldoc (switch meanings, environment, search behaviour), podchecker (options, exit statuses 0/1/2, warnings levels), pod2man (option list, --section/--center/--name/--errors, name derivation) and Pod::Usage (call forms, -exitval, -verbose, 99 with -sections). Corrected: `perldoc -T` sends output to STDOUT without a pager (`-t` is the plain-text converter); `-o` only selects a formatter class. Removed: pod2text/pod2html examples, Test::Pod and Test::Pod::Coverage test snippets (third-party, MetaCPAN source dropped), xt/ directory advice, L<> linking and 'pod2man needs --section=3' claims.
Method: documentation only; no commands were run.
