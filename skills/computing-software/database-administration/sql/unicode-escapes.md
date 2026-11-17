---
id: computing-software.database-administration.sql.unicode-escapes
name: unicode-escapes
category: computing-software
field: database-administration
product: sql
tags: [sql, unicode-escapes]
level: advanced
status: docs-checked
description: "Write unicode characters with E'' escapes and U& strings in PostgreSQL."
sources: ["https://www.postgresql.org/docs/current/sql-syntax-lexical.html", "https://www.postgresql.org/docs/current/functions-string.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unicode escapes in strings and identifiers

- `U&'d\0061t\+000061'` yields `data`: a backslash plus a 4-digit hex code point, or a backslash, plus sign and 6-digit code point. `U&` must be directly before the quote (no space) and can be upper or lower case; write spaces around the `&` operator to avoid ambiguity.
- `UESCAPE '!'` after the string picks another escape character (`U&'d!0061t!+000061' UESCAPE '!'`). It cannot be a hex digit, plus sign, single or double quote, or whitespace; write it twice to get it literally. Note the escape character is in single quotes, even for identifiers.
- Identifiers use double quotes: `U&"d\0061t\+000061"`.
- 4-digit or 6-digit forms can express UTF-16 surrogate pairs for code points above U+FFFF; the pairs are combined into a single code point. The 6-digit form makes that unnecessary.
- If the server encoding is not UTF-8, the code point is converted to the server encoding, and an error is reported if that is not possible.
- `E'é'` and `E'\n'` are C-style escape strings (E before the quote): `\uxxxx` and `\Uxxxxxxxx` give Unicode characters, `\n` newline, `\xhh` and octal escapes give raw bytes that you must keep valid in the server encoding. Prefer Unicode escapes so the server checks the conversion.
- With `standard_conforming_strings` on (the default since PostgreSQL 9.1) backslash is literal in a plain `'...'` string and special only in E strings. The U& string syntax is only accepted while it is on and is rejected with an error when it is off.
- A string constant cannot contain the character with code zero.
- Self-check: `SELECT U&'\00e9', char_length(E'é');` returns an e-acute and 1 (char_length counts characters).

## Checked

2026-11-08. Confirmed against the PostgreSQL Lexical Structure page (identifiers, string constants, C-style escapes, Unicode escapes, standard_conforming_strings) and the String Functions page (char_length counts characters). Removed the claim that a lone surrogate errors, which the page does not state, and replaced the SQLite lang.html source, which does not cover this topic.

Method: documentation only; no commands were run.
