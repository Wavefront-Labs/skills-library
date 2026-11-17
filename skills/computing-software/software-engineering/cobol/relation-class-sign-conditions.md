---
id: computing-software.software-engineering.cobol.relation-class-sign-conditions
name: relation-class-sign-conditions
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, relation-class-sign-conditions, cobol-conditions, class-condition, numeric-test, sign-condition]
level: practitioner
status: docs-checked
description: "Compare values correctly and use IS NUMERIC, IS ALPHABETIC and IS POSITIVE tests with their pitfalls."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Relation, class and sign conditions
**Goal:** write comparisons that mean what you intend (Enterprise COBOL for z/OS 6.4 wording).

- Relation: operators are `IS [NOT] GREATER THAN | >`, `IS [NOT] LESS THAN | <`, `IS [NOT] EQUAL TO | =`, `IS GREATER THAN OR EQUAL TO | >=`, `IS LESS THAN OR EQUAL TO | <=`. Each operator is preceded and followed by a space; the two characters of `>=` and `<=` have no space between them. At least one operand must be an identifier.
- Numeric operands compare by algebraic value; alphanumeric operands by alphanumeric character value; national, DBCS and UTF-8 by their own character values. A comparison with an alphanumeric group item is a group comparison on alphanumeric character values.
- Class: `IS [NOT] NUMERIC | ALPHABETIC | ALPHABETIC-LOWER | ALPHABETIC-UPPER | class-name | DBCS | KANJI`.
- Sign: `operand IS [NOT] POSITIVE | NEGATIVE | ZERO`.
```cobol
IF IN-AMT IS NUMERIC
    IF IN-AMT IS POSITIVE
        ...
    END-IF
END-IF
```
- NUMERIC: usage must be DISPLAY, NATIONAL, COMPUTATIONAL-3 or PACKED-DECIMAL, and the item must not be of class alphabetic. If the PICTURE has no sign, the item is numeric only if the contents are digits 0 to 9 and no operational sign is present. If the PICTURE has a sign, the item is numeric only if it is an elementary item, the contents are numeric and a valid operational sign is present.
- ALPHABETIC: only A to Z, a to z and space. ALPHABETIC-LOWER: only a to z and space. ALPHABETIC-UPPER: only A to Z and space. These apply to DISPLAY or NATIONAL items that are not of class numeric.
- class-name tests that a DISPLAY item contains only the characters in the SPECIAL-NAMES CLASS definition.
- An alphanumeric group item can be used in a class condition where an elementary alphanumeric item can, except the NUMERIC test cannot be used if the group contains a signed elementary item.
- Sign: operand must be a numeric identifier or an arithmetic expression with at least one variable (floating-point identifiers allowed). POSITIVE is greater than zero, NEGATIVE less than zero, ZERO equal to zero; an unsigned operand is POSITIVE or ZERO. `NOT ZERO` is true when the operand is positive or negative.

## Gotchas
- ALPHABETIC accepts letters and space, so an all-space field is ALPHABETIC.
- A numeric literal compared with an alphanumeric item must be an integer (Table 23 marks this combination "Alph (Int)"); a numeric-to-alphanumeric comparison with a noninteger is not allowed.
- Which operational signs count as valid depends on the NUMCLS installation option and the NUMPROC compiler option, and sign-condition results depend on NUMPROC; those options are described in the Programming Guide (not read here).
- A relation condition between an alphanumeric item and a numeric literal appears in Table 23; check the table for every pair of categories you mix rather than assuming a conversion.

## Self-check
Test fields `'12 '`, `'1A '` and `'123'` with IS NUMERIC in a test program; by the rules above the first two are not numeric (space and A are not digits) and the third is. These results follow from the manual and were not run.

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted) the Class condition section with Table 21, the Relation conditions introduction, the General relation conditions section (format, Table 22 operators, comparison types, Tables 23 and 24 key) and the Sign condition section. Confirmed all claims above. Removed: "alphanumeric compared by collating sequence with space padding of the shorter operand" (the alphanumeric comparison subsection was not read), "digits sort after letters in EBCDIC / ASCII vs EBCDIC ordering" (not read), "converts differently across compilers" (replaced by the Table 23 integer rule), "on an unsigned PIC 9 field a sign overpunch fails the test" (reworded to IBM's rule), and the unread ISO, ibm.com/docs root and GnuCOBOL sources.
Method: documentation only; no commands were run.
