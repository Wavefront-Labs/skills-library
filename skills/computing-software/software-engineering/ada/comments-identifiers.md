---
id: computing-software.software-engineering.ada.comments-identifiers
name: comments-identifiers
category: computing-software
field: software-engineering
product: ada
tags: [ada, comments-identifiers, ada-lexical]
level: intro
status: draft
description: "Ada lexical basics: -- comments, case-insensitive identifiers, reserved words and underscores in names."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/intro-to-ada/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Comments and identifiers
Comments start with `--` and run to end of line; there is no block comment.
```ada
-- compute total
Total_Count : Integer := 0;   -- identifiers are case-insensitive
```
- Identifiers: letters, digits, single underscores; must start with a letter. `Max_Value` = `MAX_VALUE`.
- Reserved words (`begin`, `end`, `is`, `new`, `range`) cannot be identifiers.
## Gotchas
- No double or trailing underscores (`A__B`, `A_` are illegal).
- Mixed_Case is convention only; `-gnaty` style checks enforce it.
## Self-check
Compile a unit using `Foo` and `FOO` for one object and confirm it builds; add `A__B` and confirm the error.
