---
id: computing-software.software-engineering.perl.taint-mode-untainting
name: taint-mode-untainting
category: computing-software
field: software-engineering
product: perl
tags: [perl, taint-mode, untaint, perl-t, tainted-data, perlsec, taint-mode-untainting, perl-security]
level: advanced
status: docs-checked
description: "Use perl -T: what is tainted, which operations refuse tainted data, how to untaint with capturing regexes, and PATH hygiene."
sources: ["https://perldoc.perl.org/perlsec", "https://perldoc.perl.org/perlrun"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Taint mode and untainting

**Goal:** force validation of external data before dangerous operations.

```perl
#!/usr/bin/perl -T
use strict; use warnings;
$ENV{PATH} = '/usr/bin:/bin';                  # taint mode requires a safe PATH
delete @ENV{qw(IFS CDPATH ENV BASH_ENV)};
my ($file) = $ARGV[0] =~ m{\A([\w./-]+)\z} or die "bad filename";    # untaint via a capture
open(my $fh, '<', $file) or die $!;
system('/bin/ls', '-l', $file);                # list form with a clean env
```
- Tainted: command-line arguments, `%ENV`, locale information, results of certain system calls such as `readdir` and `readlink`, all file input, and data derived from tainted values.
- Operations that die on tainted data: `system`/`exec`/backticks, pipe opens, `open` for writing, `unlink` and `umask` (perlsec lists more)
- Untaint only by extracting with a regex capture `($1)`; a capture of `.*` is the same as turning the check off: write strict allow-list patterns.
- Check with `Scalar::Util::tainted($var)`; the `-t` switch runs the taint checks as warnings, for testing (perlrun).

## Rules
- `-T` must be on the `#!` line **and** on the command line if the interpreter was started as `perl script.pl`; with taint checks Perl does not consult `PERL5LIB` or `PERLLIB` (perlrun).
- Taint mode is a safety net against mistakes, not a sandbox; it does not prevent SQL injection, XSS or logic errors.
- Hash keys are not tainted, values are.

## Self-check
- [ ] `perl -T -e 'system("echo $ARGV[0]")' x` is rejected by taint checks (perlsec marks a one-string `system` with tainted data as insecure).

## Checked
2026-11-03: confirmed against perlsec (what is tainted, hash keys never tainted, unsafe operations system exec backticks open-for-write unlink umask, PATH and IFS CDPATH ENV BASH_ENV clean-up, untainting through a regex capture) and perlrun (-T and -t, PERL5LIB and PERLLIB not consulted under taint). Removed: Taint::Util, ${^TAINT}, the longer operation list, PERL5OPT and . in @INC claims, setuid advice, prove -T, and the exact error text in the self-check.
Method: documentation only; no commands were run.
