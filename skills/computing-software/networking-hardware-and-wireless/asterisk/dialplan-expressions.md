---
id: computing-software.networking-hardware-and-wireless.asterisk.dialplan-expressions
name: dialplan-expressions
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, dialplan, expressions, operators, expr, regex, arithmetic]
level: practitioner
status: docs-checked
description: "Evaluate dialplan expressions with the dollar-bracket syntax: operator precedence, comparison, logical, arithmetic and the colon regular-expression match operator."
sources:
  - https://docs.asterisk.org/Configuration/Dialplan/Expressions/
  - https://docs.asterisk.org/Configuration/Dialplan/Expressions/Operators/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dialplan expressions
Anything inside `$[ ]` is evaluated after variable substitution. Extra spaces are ignored.
```
exten => 1,1,Set(lala=$[1 + 2])
exten => 1,2,Set(koko=$[2 * ${lala}])
```
Here `koko` becomes 6.

Operators, lowest to highest precedence:
- `expr1 ? true_expr :: false_expr`: conditional (lowest precedence).
- `expr1 | expr2`: expr1 if neither empty nor zero, else expr2.
- `expr1 & expr2`: expr1 if neither is empty or zero, else 0.
- `= > >= < <= !=`: floating point comparison if both are numbers, otherwise locale string comparison; result is 1 or 0.
- `+ -`, then `* / %` (floating point division, remainder).
- Unary `-` and `!` (right associative); `!` is true for null, empty, 0 or "0".
- `expr1 : expr2`: regular expression match, anchored at the start with an implicit `^`. With a match group `()` it returns the `\1` text; otherwise it returns the number of characters matched. `expr1 =~ expr2` is the same match without the implicit anchor.

## Checked
2026-11-04: read the cited Asterisk documentation pages (Expressions, Operators) and confirmed the commands, options, defaults and names stated above. Unverified related-pages line removed; conditional and =~ operators added.

Method: documentation only; no commands were run.
