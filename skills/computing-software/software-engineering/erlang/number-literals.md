---
id: computing-software.software-engineering.erlang.number-literals
name: number-literals
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-lexical, number-literals]
level: intro
status: docs-checked
description: "Erlang literal syntax: percent comments, based integers, character literals, strings as lists, underscores in numbers."
sources:
  - https://www.erlang.org/doc/system/reference_manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Comments, numbers, strings and characters
**Goal:** read and write every literal form.

- A comment begins with `%` and runs to the end of the line; it can appear anywhere except inside strings and quoted atoms.
- Integer notations: `$a` (the character code, 97, ASCII or Unicode code point), `Base#Digits` with a base from 2 to 36 (`16#FF`, `2#1010`). There is no `0x` or leading-zero octal syntax.
- Single underscores can separate digits (`1_000_000`). Based floats exist too (`16#ff.fe#e+6`).
- Floats are not exact IEEE 754: infinity and NaN are not supported, and an operation that would produce them raises `badarith`.
- `/` is floating-point division; use `div` and `rem` for integers.
- Strings `"abc"` are shorthand for lists of code points: `"abc" =:= [97,98,99]`. Binaries `<<"abc">>` are bytes.
- Adjacent string literals are concatenated at compile time (since OTP 27 they must be separated by white space).
- OTP 27 added triple-quoted strings and sigils: `~` (UTF-8 binary), `~b`, `~B`, `~s`, `~S`.
```erlang
16#FF + 2#11 + $a + 1_000.   % 255 + 3 + 97 + 1000 = 1355
```

## Gotchas
- Compare floats numerically with `==` and an `is_float/1` guard; `=:=` and pattern matching treat `0.0` and `-0.0` as different terms (this changed in OTP 27).

## Self-check
Evaluate `"abc" =:= [97,98,99]` and `16#FF` in the shell.

## Checked
2026-11-02. Erlang Reference Manual "Data Types" (numbers, `$char`, base notation, underscores, float limits and comparison, strings, concatenation, triple-quoted strings, sigils), "Modules" (comments), "Expressions" (arithmetic operators). Removed: the `%%%`/`%%` convention, "OTP 23+" for underscores, arbitrary precision wording, and the `io:format ~p` gotcha (not in these pages).
Method: documentation only; no commands were run.
