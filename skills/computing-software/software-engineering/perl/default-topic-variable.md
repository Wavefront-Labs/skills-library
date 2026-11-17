---
id: computing-software.software-engineering.perl.default-topic-variable
name: default-topic-variable
category: computing-software
field: software-engineering
product: perl
tags: [perl, topic-variable, underscore-default, implicit-arguments, perlvar, default-topic-variable, perl-special-variables]
level: intro
status: docs-checked
description: "Know which built-ins default to $_ and @ARGV/@_, and protect $_ from clobbering."
sources: ["https://perldoc.perl.org/perlvar", "https://perldoc.perl.org/perlfunc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# $_ and @_ defaults

**Goal:** use implicit variables confidently and safely.

```perl
for (@lines) { chomp; next unless length; print; }       # all on $_
print for grep { /x/ } @l;                                # postfix for aliases $_
my @u = map { uc } @words;
s/^\s+//, s/\s+$// for @fields;
while (<$fh>) { ... }                                     # assigns to $_ (implicit defined test)
```

## Functions defaulting to `$_`
`print`, `say`, `chomp`, `chop`, `lc`, `uc`, `lcfirst`, `ucfirst`, `length`, `ord`, `chr`, `quotemeta`, `split` (its string), `m//`, `s///`, `tr///`, `-e` file tests, `defined`, `ref`, `abs`, `int`, `sqrt`, `log`, `hex`, `oct`, `pos`, `unlink`, `stat`, `lstat`, `eval`, `require`, `reverse` in scalar context. Outside subs `shift`/`pop` default to `@ARGV`, inside subs to `@_`.

## Gotchas
- `$_` is a global (package) variable; a sub that does `while (<FH>)` or `for (...)` can clobber the caller's value. Use `local $_;` or `for my $line (...)`.
- `foreach` and `map`/`grep` localise `$_` for their duration (aliasing elements).
- `given` (the discouraged `switch` feature) also assigns `$_`. `my $_` worked from 5.10 to 5.24 and is now a fatal error (perlvar).
- Functions called inside a `map` block that modify `$_` change the original data.
- `for (my $i...)` loops do not touch `$_`.
- `print` with no arguments prints `$_`.
- Lexical topic alternatives: `for my $x (...)`, or `local $_ = $value;`.

## Self-check
- [ ] `perl -e '@a=(" a "," b "); s/^\s+|\s+$//g for @a; print join "|", @a'` prints `a|b`.

## Checked

2026-11-02. Confirmed in perlfunc that every function in the list defaults to `$_` (the `shift`/`pop` defaults to `@ARGV`/`@_` and scalar `reverse` included); in perlvar that `$_` is global, `local $_` is the documented protection and `my $_` (allowed 5.10 to 5.24) is now a fatal error; in perlsyn that foreach localises its variable and the switch feature is discouraged; in perlop the implicit `defined($_ = <STDIN>)` of `while (<...>)`. Removed: the `-n` loop claim and the removed/experimental wording for `given`.

Method: documentation only; no commands were run.
