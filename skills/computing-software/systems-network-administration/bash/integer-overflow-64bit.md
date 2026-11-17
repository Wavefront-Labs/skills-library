---
id: computing-software.systems-network-administration.bash.integer-overflow-64bit
name: integer-overflow-64bit
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, integer-overflow-64bit, bash-integer-limits, shell-scripting]
level: advanced
status: docs-checked
description: "Bash arithmetic uses the largest fixed-width integers available with no overflow check, while division by 0 is trapped; know the constant forms and operators."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Integer limits in bash arithmetic
**Goal:** know what shell arithmetic does at the edges.
```bash
echo $(( 2 ** 10 ))        # ** is exponentiation
echo $(( 7 / 2 )) $(( 7 % 2 ))
echo $(( 10#08 + 1 ))      # base 10 forced; a bare 08 would be octal
echo $(( 0x1F ))           # hexadecimal constant
echo $(( 2#101 ))          # [base#]n, base 2 to 64
echo $(( 1 / 0 ))          # trapped and reported as an error, not wrapped
```
- The manual's rule: "Evaluation is done in the largest fixed-width integers available, with no check for overflow, though division by 0 is trapped and flagged as an error." The manual does not state the width; treat results near the type's limits as unchecked, and test on the target system if you rely on a particular width.
- Operators, precedence, associativity and values "are the same as in the C language": `++ -- + - ! ~ ** * / % + - << >> <= >= < > == != & ^ | && || ?: = *= /= %= += -= <<= >>= &= ^= |= ,`.
- Constants follow the C definition without suffixes or character constants. A leading `0` means octal, a leading `0x` or `0X` hexadecimal, otherwise `[base#]n` with base 2 to 64. Digits above 9 are lowercase letters, uppercase letters, `@`, `_` in that order; for base 36 or less the case is interchangeable.
- A variable that is null or unset evaluates to 0 when referenced by name in an expression. A variable's value is evaluated as an arithmetic expression when referenced.
- Arithmetic is available in `$(( ))`, `(( ))`, `let`, `declare -i`, the arithmetic `for`, and `[[`.
- The manual's arithmetic section describes integer arithmetic only; it documents no floating-point support.

## Checked
Date: 2026-11-07
Method: Read GNU Bash manual section 6.5 Shell Arithmetic in full. Corrections: removed the specific claims that integers are signed 64-bit and that `9223372036854775807 + 1` wraps to `-9223372036854775808` (the manual says only "largest fixed-width integers available" with no overflow check), the division and remainder sign rules, the quoted error text "division by 0", the `bc` and `awk` suggestions and examples (not on the page), and the `(( 2**62 * 2 < 0 ))` self-check. The description was reworded to match.
