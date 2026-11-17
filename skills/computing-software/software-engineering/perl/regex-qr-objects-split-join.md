---
id: computing-software.software-engineering.perl.regex-qr-objects-split-join
name: regex-qr-objects-split-join
category: computing-software
field: software-engineering
product: perl
tags: [perl, qr, split, join, regex-objects, perlfunc, regex-qr-objects-split-join]
level: practitioner
status: docs-checked
description: "Use qr// objects, split with patterns and limits (including the ' ' special case), and join to rebuild strings."
sources: ["https://perldoc.perl.org/perlfunc", "https://perldoc.perl.org/perlre", "https://perldoc.perl.org/perlop"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# qr// objects, split and join with regexes

**Goal:** correct tokenising of strings.

```perl
my @f  = split /,/, $line;             # drops trailing empty fields
my @f2 = split /,/, $line, -1;         # keep trailing empties
my @w  = split ' ', $text;             # awk-style: skips leading whitespace, splits on runs
my @ch = split //, $word;              # characters
my ($k, $v) = split /=/, $pair, 2;     # limit 2: value may contain '='
my @p  = split /(,)/, "a,b";           # captures are returned too: a , b
my $re = qr/\s*;\s*/;
my @c  = split $re, $cmds;
my $csv_ish = join ',', map { qq("$_") } @items;
```

## Rules
- `split /^/` is treated as `split /^/m`. `split /\s+/, " a b"` yields a leading empty field; `split ' '` does not (only the literal single-space string, not a regex `/ /`).
- A pattern that can match empty (`//`, `/x*/`) splits between characters.
- Trailing empty fields are removed when limit is omitted or 0; negative limit keeps them; positive limit caps the field count.
- `split` in scalar context returns the number of fields.
- `qr//` returns a blessed `Regexp` reference; `ref($re)` is "Regexp"; use `re::regexp_pattern($re)` to see pattern and flags.
- `join` first argument is a separator, not a regex.

## Failure modes
- `split '|', $s` treats `|` as a regex (alternation of empties): write `split /\|/, $s` or `split quotemeta('|'), $s`.

## Self-check
- [ ] `perl -e '@a=split /,/,"a,b,,"; print scalar @a'` prints `2`; with `-1` it prints `4`.

## Checked

2026-11-02. Confirmed in perlfunc `split` (trailing empty fields, limit, `' '` special case, `/^/` as `/^/m`, scalar-context field count, pattern that can match empty, captures returned) and `ref(qr/x/)` is `Regexp` (perlop); re.pm exports `regexp_pattern`. Removed: the Text::CSV advice and undef warning bullet.

Method: documentation only; no commands were run.
