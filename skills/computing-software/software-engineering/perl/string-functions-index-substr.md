---
id: computing-software.software-engineering.perl.string-functions-index-substr
name: string-functions-index-substr
category: computing-software
field: software-engineering
product: perl
tags: [perl, substr, index, string-functions, lc-uc, repeat-string, string-functions-index-substr, perl-core-functions]
level: intro
status: docs-checked
description: "Use the core string functions correctly: substr (4-arg and lvalue), index/rindex, lc/uc/fc, ucfirst, length, reverse, sprintf and join/repeat."
sources: ["https://perldoc.perl.org/perlfunc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String functions: index, substr, sprintf, lc, uc, reverse

**Goal:** the building blocks of string handling.

```perl
length($s);                       index($s, 'x');  index($s, 'x', $from);  rindex($s, 'x');   # -1 when not found
substr($s, 0, 3);                 substr($s, -3);            # extract; negative counts from the end
substr($s, 1, 2) = 'XX';          substr($s, 1, 2, 'XX');    # replace (lvalue / 4-arg form returns old part)
my $r = \substr($s, 0, 1);        # lvalue substr reference (rare)
lc $s; uc $s; ucfirst lc $s; lcfirst $s; fc $s;     # fc: feature 'fc' (5.16+), for caseless comparisons
reverse(scalar reverse "abc");    # scalar reverse of a string; print reverse() uses list context
join(', ', @items);   my $line = '-' x 40;   sprintf('%-10s|', $s);
sprintf('%s', join ',', map { sprintf '%02x', ord } split //, $s);
ord('A'); chr(65); lc(); quotemeta($s); sprintf('%vd', "1.2.3");
my @parts = unpack('(A3)*', $s);  my $count = () = $s =~ /x/g;  my $n = ($s =~ tr/x//);
```

## Rules
- `substr` beyond the end warns "substr outside of string" and returns undef; assignment beyond dies.
- `index` returns -1 (not false): test `>= 0` or `!= -1`.
- Strings are mutable; `chomp`, `chop`, `lc`, `uc` return copies (except `chomp`/`chop`, which edit in place).
- `.` concatenates; `.=` appends in place efficiently.
- `length` returns characters for decoded text, bytes for undecoded; `length undef` is undef.
- `x` with a fractional count truncates it (perlop).
- `builtin::trim` exists from 5.36 (see builtin for its status); portable: `s/^\s+|\s+$//g`.
- `lc`/`uc` on bytes outside ASCII depend on the `unicode_strings` feature and on `use locale` (perlfunc).

## Self-check
- [ ] `perl -e '$s="hello"; substr($s,0,1)="J"; print $s, index($s,"z")'` prints `Jello-1`.

## Checked

2026-11-02. Confirmed in perlfunc: `substr` 4-arg/lvalue forms and out-of-range behaviour (partly outside warns, entirely outside raises an exception for assignment), `index`/`rindex` return -1, `length undef` is undef, `sprintf '%vd'`; perlop for `x` truncation; perl5160delta for `fc`; perl5360delta/builtin for `builtin::trim`. Removed: the unverified `sprintf('%s', undef)`, case-mapping and collation bullets.

Method: documentation only; no commands were run.
