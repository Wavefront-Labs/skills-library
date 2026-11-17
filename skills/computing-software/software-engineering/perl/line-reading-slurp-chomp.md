---
id: computing-software.software-engineering.perl.line-reading-slurp-chomp
name: line-reading-slurp-chomp
category: computing-software
field: software-engineering
product: perl
tags: [perl, slurp, chomp, input-record-separator, eof, diamond-operator, perlop, line-reading-slurp-chomp]
level: practitioner
status: docs-checked
description: "Read files line by line, slurp whole files, change $/ for paragraphs or fixed records, and use <<>> safely."
sources: ["https://perldoc.perl.org/perlvar", "https://perldoc.perl.org/perlop", "https://perldoc.perl.org/perlfunc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading lines, slurping and record separators

**Goal:** pick the right read pattern.

```perl
while (my $l = <$fh>) { chomp $l; ... }            # line at a time (memory-friendly)
my @lines = <$fh>;                                  # all lines (list context)
my $text = do { local $/; <$fh> };                  # slurp ($/ undef)
my $para = do { local $/ = ""; <$fh> };             # paragraph mode: blank-line separated
my $rec  = do { local $/ = \4096; <$fh> };          # fixed-size records
read($fh, my $buf, 1024) == 0 and last;             # block read, returns bytes or 0 at EOF
chomp(my $line = <STDIN> // '');
```

## The diamond operator
- `while (<>)` reads files named in `@ARGV` (or STDIN). A file named like a shell pipe (perlop's example is `rm -rfv *|`) is opened as a pipe by `<>`. Use `<<>>` (double diamond), which uses the three-argument form of open so every `@ARGV` entry is a literal file name.
- Inside it `$ARGV` is the current filename; `$.` the line number (reset with `close ARGV if eof`).

## Rules
- `chomp` removes the current `$/` from the end (default "\n") and returns count removed; `chop` removes any last character.
- `while (my $l = <$fh>)` is implicitly `defined(...)`; reading a last line "0" is safe.
- `eof($fh)` tests end; `eof` without args tests the last read handle; `eof()` tests end of all `<>` input.
- Slurping huge files uses memory; stream instead.
- `$.` counts per handle; `close` resets it.

## Self-check
- [ ] `printf 'a\nb\n' | perl -e '@l=<STDIN>; print scalar @l'` prints `2`.

## Checked
2026-11-03: confirmed against perlvar ($/ undef, empty string and reference-to-integer modes, $. and $ARGV), perlop (<> versus <<>>, the rm -rfv *| example, implicit defined in while) and perlfunc (chomp, chop, read, eof forms). Removed: Path::Tiny, the 5.22 version for <<>>, CRLF regex advice, scalar print claim and the encoding equivalence claim.
Method: documentation only; no commands were run.
