---
id: computing-software.software-engineering.nim.literals-and-operators
name: literals-and-operators
category: computing-software
field: software-engineering
product: nim
tags: [literals-and-operators, lexical-analysis, operator, precedence, literal, user-defined-operator, string-literal, nim]
level: practitioner
status: docs-checked
description: "Read numeric, string and char literal syntax, custom operator rules, and the precedence by first character."
sources:
  - https://nim-lang.org/docs/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Literals, operators and precedence

Goal: predict how expressions parse.

- Unary operators always bind stronger than any binary operator: `$a + b` is `($a) + b`. Binary operators whose first character is `^` are right-associative; all other binary operators are left-associative.
- Binary precedence is set by rules in this order. Arrow-like operators (ending in `->`, `~>` or `=>`) have the lowest precedence. An operator ending in `=` whose first character is not one of `< > ! = ~ ?` is an assignment operator with the second-lowest. Otherwise the first character decides:

| Level | Operators | First character |
|---|---|---|
| 10 (highest) | | `$` `^` |
| 9 | `*` `/` `div` `mod` `shl` `shr` `%` | `*` `%` `\` `/` |
| 8 | `+` `-` | `+` `-` `~` `|` |
| 7 | `&` | `&` |
| 6 | `..` | `.` |
| 5 | `==` `<=` `<` `>=` `>` `!=` `in` `notin` `is` `isnot` `not` `of` `as` `from` | `=` `<` `>` `!` |
| 4 | `and` | |
| 3 | `or` `xor` | |
| 2 | | `@` `:` `?` |

- Keyword operators: `and or not xor shl shr div mod in notin is isnot of as from`. `not` is always unary. Operator characters: `= + - * / < > @ $ ~ & % | ! ? ^ . : \`; `.`, `=`, `:` and `::` alone are not general operators.
- A leading `@` on a unary operator binds stronger than a suffix: `@x.abc` is `(@x).abc` whereas `$x.abc` is `$(x.abc)`.
- Spacing matters: `echo $foo` is `echo($foo)`; `echo(1, 2)` passes two arguments while `echo (1, 2)` passes a tuple.
- Numeric literals: underscores allowed; prefixes `0b` `0o` `0x`. A literal without suffix is `int` if in `low(int32)..high(int32)`, otherwise `int64`, and `float` if it has a dot or `e`/`E`. Type suffixes: `'i8 'i16 'i32 'i64 'u 'u8 'u16 'u32 'u64 'f 'd 'f32 'f64`.
- A unary minus is part of a number literal when the preceding character is one of space, tab, newline, return, `,` `;` `(` `[` `{`: `echo -1`, `echo 3,-1` are single tokens, but `echo x-1` is `x - 1`.
- Custom numeric literals: an unknown suffix calls a proc named with a leading quote, for example ``proc `'u4`(n: string): u4``, so `5'u4` works; extra parameters are passed as `5'u4(123)`.
- Non-base-10 literals are checked on bit width: `0b10000000'u8 == 0x80'u8 == 128` but `0x80'i8 == -1`.

Verify: `echo 2 + 3 * 4` prints 14.

## Checked

2026-11-08. Confirmed against the Nim Manual (doc/manual.md from the Nim repository): numeric literal grammar and text (read in full), Operators, Associativity and Precedence including the table (read in full). The string and character literal sections of the Lexical Analysis chapter were not read. Removed: the claim that `a -b` parses as a command call, the difference between `echo -1` and `echo - 1`, the old precedence summary (replaced by the table), and the placement of assignment operators as "lowest" (arrow-like operators are lower). tut1 and lib were not read and were dropped from sources.
Method: documentation only; no commands were run.
