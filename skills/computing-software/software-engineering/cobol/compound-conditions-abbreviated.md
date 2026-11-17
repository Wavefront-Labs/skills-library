---
id: computing-software.software-engineering.cobol.compound-conditions-abbreviated
name: compound-conditions-abbreviated
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, compound-conditions-abbreviated, logical-operators, and-or-not, abbreviated-conditions]
level: practitioner
status: docs-checked
description: "Write compound conditions with correct precedence and read abbreviated forms like IF A = 1 OR 2."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AND, OR, NOT and abbreviated combined conditions
**Goal:** avoid precedence and implied-subject surprises (Enterprise COBOL for z/OS rules).

- Precedence, highest to lowest, unless parentheses change it: arithmetic operations, simple conditions, NOT, AND, OR. Parenthesize anything mixed; parentheses are never needed when only ANDs or only ORs are used. Each logical operator must be preceded and followed by a space.
- Abbreviation: in consecutive relation conditions the missing subject is the last stated subject and the missing relational operator is the last stated one. `IF A = 1 OR 2` means `A = 1 OR A = 2`. `IF A > B AND C` means `A > B AND A > C`. `IF NOT A = B OR C` means `(NOT (A = B)) OR (A = C)`: NOT negates only the relation condition that follows it. NOT directly before GREATER THAN, >, LESS THAN, <, EQUAL TO or = is part of the relational operator.
```cobol
IF (WS-A = 1 OR WS-A = 2) AND WS-FLAG-ON
```
- IBM documents the evaluation order: left to right within each hierarchical level, and a level stops as soon as its truth value is known, so later conditions (and their arithmetic or functions) are evaluated only if needed. This is documented for Enterprise COBOL; check the manual of other compilers before relying on it.

## Gotchas
- Use explicit subjects in new code; abbreviated conditions are easy to misread.
- Insertion of an omitted subject or operator stops at another simple condition or a condition-name, so `IF STATE-DONE OR WS-ERR > 0` is a condition-name combined with a relation.
- Consecutive logical NOT operators cancel each other and give an S-level diagnostic.

## Self-check
Rewrite an abbreviated condition in full form, compile both, and compare behaviour on edge values.

## Checked
Date: 2026-11-08. Read, in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted), the sections Logical operators and precedence, Combined conditions, Order of evaluation of conditions, and Abbreviated combined relation conditions including Table 31. Confirmed the abbreviation expansions against Table 31 and the text. Corrected: the old claim that short-circuit evaluation is "not guaranteed by the standard" and the advice not to guard on it; IBM specifies left-to-right evaluation that stops once the truth value is determined. Removed the unread ISO source; the ISO standard and other compilers are not covered.
Method: documentation only; no commands were run.
