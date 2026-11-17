---
id: computing-software.software-engineering.cobol.replace-and-conditional-compilation
name: replace-and-conditional-compilation
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, replace-and-conditional-compilation, cobol-directives, replace-statement, compiler-directive, conditional-compilation, define-if]
level: advanced
status: docs-checked
description: "Apply source-level substitutions with REPLACE and choose code per target with >>DEFINE, >>IF and >>EVALUATE directives in Enterprise COBOL."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# REPLACE, >>DEFINE, >>IF and >>EVALUATE
**Goal:** one source for several targets (Enterprise COBOL for z/OS 6.4 rules).

```cobol
REPLACE ==:MAXN:== BY ==500==.
...
>>DEFINE ZOS AS 1
>>IF ZOS IS DEFINED
    DISPLAY 'z/OS build'
>>ELSE
    DISPLAY 'other build'
>>END-IF
```
- `REPLACE ==a== BY ==b==.` (format 1) replaces text from that point until the next REPLACE statement, `REPLACE OFF.` or the end of the separately compiled program. It must be preceded by a separator period (unless first in the program) and end with a period. Compared with COPY ... REPLACING it acts on all source text, not only copybooks.
- Format 1 also takes `LEADING ==x== BY ==y==` and `TRAILING ==x== BY ==y==` for partial words (one text word each; no literals). The `:TAG:` pattern with colons as separators makes the tag a stand-alone operand, so `:TAG:-WEEK` can have its tag replaced.
- Matching is by whole text words, character for character; a comma, semicolon or run of spaces counts as a single space. Pseudo-text delimiters `==` must open and close on one line, and a text word can be up to 322 characters.
- REPLACE runs after COPY processing. A REPLACE statement cannot contain COPY, and its output must not contain a REPLACE statement.
- Compiler directives start with `>>`: `>>DEFINE name [AS] literal | arithmetic-expression | PARAMETER | OFF [OVERRIDE]`, `>>IF ... >>ELSE ... >>END-IF`, and `>>EVALUATE ... >>WHEN ... >>WHEN OTHER ... >>END-EVALUATE`. Each directive keyword goes on its own line (Area A or B) with nothing else on that line; the controlled text begins on a new line.
- Conditions in `>>IF` and `>>WHEN` are constant conditional expressions: relation conditions on literals or compilation variables (non-numeric operands only with IS EQUAL TO / IS NOT EQUAL TO), `name IS [NOT] DEFINED`, boolean conditions (`B'1'`/`B'0'` literals), combined with AND, OR, NOT. Compile-time arithmetic is integer only, with no exponentiation.
- A DEFINE literal may be an alphanumeric literal (including hex), an integer, or a boolean literal; national, DBCS and Z literals are not supported. `AS PARAMETER` takes the value from a DEFINE compiler option if one was given, else the variable is undefined. `>>DEFINE name OFF` undefines it; `OVERRIDE` changes an existing definition (a plain redefinition to a different value is an error).
- Predefined variables include `IGY-CICS` (B'1' if the CICS option is in effect), `IGY-ARCH` (the ARCH value) and `IGY-COMPILER-VRM` (VVRRMM). Example: `>>IF IGY-CICS` to choose EXEC CICS or batch I/O.
- Listing control statements are different and only affect the source listing: `EJECT`, `SKIP1`, `SKIP2`, `SKIP3` and `TITLE literal`, each alone on its line.

## Gotchas
- Substitution happens before parsing, on whole words (except LEADING/TRAILING), so look at the listing to see the resulting text. The listing shows included and excluded text; the CONDCOMP(SKIPSRC) option (Programming Guide) hides excluded text.
- DEFINE directives inside text that conditional compilation omits are not processed.
- In a BASIS file, conditional directives are passed through and processed later, not applied at that point.
- Heavy conditional compilation hurts readability; prefer separate programs for large differences (a style judgement, not from the manual).

## Self-check
Compile twice, once with `DEFINE(ZOS=1)` style option and once without, using `>>DEFINE ZOS AS PARAMETER`, and compare the listings for the included branch.

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted): REPLACE statement (formats, comparison and replacement rules, :TAG:), EJECT, SKIP and TITLE statements, and Chapter 114 compiler directives (DEFINE, EVALUATE, IF, constant conditional expressions, defined conditions, boolean conditions, compile-time arithmetic, predefined compilation variables, examples). Removed the claims that IBM support is limited to >>SOURCE and that conditional compilation is unconfirmed for IBM (it is documented), the CEE3ABD example call, `STOP RUN WITH ERROR STATUS` and the `cobc -D` GnuCOBOL option, none of which are in the source. Replaced `>>IF ZOS DEFINED` with the documented `IS DEFINED` form. Removed the unread ISO, ibm.com/docs and GnuCOBOL sources.
Method: documentation only; no commands were run.
