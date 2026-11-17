---
id: computing-software.software-engineering.crystal.case-when-values
name: case-when-values
category: computing-software
field: software-engineering
product: crystal
tags: [case-when-values, case-when, case, when, case-equality, range-when, regex-when, else, switch, crystal]
level: intro
status: docs-checked
description: "Use Crystal case/when with values, ranges, types, regex, implicit receivers and no subject."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/case.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# case/when with values, ranges and types

Goal: use case as an expression.

```crystal
kind = case x
       when 0, 1  then "small"
       when 2..10 then "mid"
       when Int32 then "big"
       when /ab/  then "regex"
       when .nil? then "nil"     # implicit-object form
       else            "other"
       end
```
- A comma lists several values for one branch (`when value1, value2`).
- Matching uses the case subsumption operator `===` (`pattern === value`), defined on `Object` and overridable. `Class` matches instances, `Regex` matches the string, `Range` matches inclusion.
- A type in `when` uses `is_a?`; if the subject is a variable or assignment, its type is restricted in that branch.
- `case` without a subject treats each `when` as a boolean condition (an if/elsif chain).
- `when .even?` calls the method on the subject.
- `in` (exhaustive) is a separate form; see case-in-pattern-matching. An exhaustive case cannot contain `when` or `else`.

Verify: spec every branch plus the else.

## Checked
Checked 2026-11-02 against the crystal-book `case` page. Removed: the claim that a case without `else` returns nil, `Proc` matching, and enum `when` forms.

Method: documentation only; no commands were run.
