---
id: computing-software.software-engineering.ada.if-case-statements
name: if-case-statements
category: computing-software
field: software-engineering
product: ada
tags: [ada, if-case-statements, ada-control-flow]
level: intro
status: draft
description: "Ada if/elsif/else, case with others and ranges, and if/case expressions in Ada 2012."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/intro-to-ada/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# if, case and conditional expressions
```ada
if X < 0 then ... elsif X = 0 then ... else ... end if;
case C is
   when Red | Green => ...
   when 1 .. 9      => ...
   when others      => ...
end case;
Y : Integer := (if X > 0 then X else -X);
```
- `case` must cover every value (exhaustive); a missing choice is a compile error.
- `and then` / `or else` short-circuit; plain `and` / `or` evaluate both sides.
## Gotchas
- A conditional expression in a call needs its own parentheses only when not the sole argument.
## Self-check
Remove `others` from a case on Integer and read the error.
