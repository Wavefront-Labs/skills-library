---
id: computing-software.software-engineering.perl.numeric-functions-bigint
name: numeric-functions-bigint
category: computing-software
field: software-engineering
product: perl
tags: [perl, int-abs-sqrt, rounding-numbers, bigint, rand-srand, numeric-functions-bigint]
level: practitioner
status: docs-checked
description: "Do arithmetic correctly in Perl: int truncation, POSIX floor/ceil, sqrt, oct, rand/srand, use integer and the bigint pragma."
sources: ["https://perldoc.perl.org/perlfunc", "https://perldoc.perl.org/perlnumber", "https://perldoc.perl.org/bigint", "https://perldoc.perl.org/Math::BigInt", "https://perldoc.perl.org/POSIX", "https://perldoc.perl.org/functions/int", "https://perldoc.perl.org/functions/oct", "https://perldoc.perl.org/functions/rand", "https://perldoc.perl.org/functions/srand"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Numeric functions, rounding and big numbers

**Goal:** correct number handling.

```perl
int(7.9); int(-7.9);                       # 7, -7: truncates toward zero
use POSIX qw(floor ceil fmod); floor(-1.5); ceil(1.2); fmod(7, 3);
my $s = sprintf('%.2f', $x);               # format/round with sprintf, not int
sqrt(16); log(10); atan2(1, 1) * 4;        # sqrt: non-negative operands only
oct('0755'); oct('0x1f'); oct('0b101');    # oct also reads 0x and 0b strings
srand(42); my $r = int(rand(10));          # integer 0..9
```

## Rules (perlfunc, POSIX)
- `int` returns the integer portion. perlfunc says not to use it for rounding: it truncates towards 0, and floating-point representation can surprise (`int(-6.725/0.025)` gives -268, not -269). Use `sprintf`, `printf`, `POSIX::floor` or `POSIX::ceil`.
- `POSIX::floor` is the largest integer value less than or equal to the argument; `ceil` the smallest greater than or equal; `fmod` is the C function.
- `sqrt` works only for non-negative operands unless `Math::Complex` is loaded.
- `oct EXPR` handles octal strings, with `0x`/`x` interpreted as hex and `0b`/`b` as binary; an optional `0o` or `o` prefix is accepted as of Perl 5.33.5. It handles non-negative integers only. Convert back with `sprintf "%o"`.
- `rand(N)` returns a float at least 0 and below N (N omitted means 1; 0 is treated as 1). As of Perl 5.20 it uses the drand48 PRNG, fine for games and test data. It is not suitable for passwords, tokens, salts or keys; perlfunc lists `Crypt::SysRandom`, `Crypt::URandom` and `Crypt::PRNG` as alternatives.
- `srand` seeds `rand`; `rand` calls it implicitly on first use. Use `srand($seed)` with the same integer for repeatable sequences; do not call `srand()` without an argument more than once per process; consider calling it after `fork`. Since 5.14 it returns the seed.
- `NaN` is not equal to anything, including itself (POSIX page).

## `use integer` and `bigint`
- Under `use integer`, nearly all arithmetic operators force integer arguments and results; `abs`, `++` and `--` are unchanged (perlnumber). It is limited to what a Perl scalar can hold.
- `use bigint` converts every numeric literal in scope to a `Math::BigInt` object, so integers can be arbitrarily large. Non-integer literals and all expression results are truncated to integer, so it is not a way to get exact fractions.
- Under `bigint`, `hex()` and `oct()` are lexically overridden (Perl 5.10+) to handle big values.
- Object API examples from Math::BigInt: `Math::BigInt->new('123456789012345678901234567890')`, methods `badd`, `bmul`, `bpow`, `bstr`.

## Checked
2026-11-09. Read in full: perldoc functions pages int, oct, rand, srand; read bigint, perlnumber (integer sections), and POSIX floor/ceil/fmod/NaN entries; searched perlfunc for sqrt and log and Math::BigInt for method names. Removed as not confirmed: the `%` sign rule for negatives, half-even `sprintf` rounding, Math::BigFloat claims and `bpi(50)`, IV size and 2**53 statements, `**` overflow, `use integer` division and `bignum` notes, `hex('0xFF')` details, Number::Format, `log` of non-positive dying, and the `perl -e` self-check.
Method: documentation only; no commands were run.
