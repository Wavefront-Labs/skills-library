---
id: computing-software.software-engineering.refactoring.decompose-and-consolidate-conditionals
name: decompose-and-consolidate-conditionals
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, conditional-logic, decompose-conditional, consolidate-conditional, complex-conditionals, readability, fowler-catalog]
level: practitioner
status: draft
description: "Make complex if/else logic readable: Decompose Conditional into named functions, and Consolidate Conditional Expression when several checks lead to the same result."
sources: ["https://refactoring.com/catalog/decomposeConditional.html", "https://refactoring.com/catalog/consolidateConditionalExpression.html", "Refactoring, 2nd ed. (Fowler), ch10"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Decompose Conditional / Consolidate Conditional Expression

**Goal:** conditionals that state WHY a branch is taken, not just how the check is
computed.

## Decompose Conditional
Before:
```java
if (!date.isBefore(plan.summerStart()) && !date.isAfter(plan.summerEnd()))
    charge = quantity * plan.summerRate();
else
    charge = quantity * plan.regularRate() + plan.regularServiceCharge();
```
After:
```java
charge = isSummer(date, plan) ? summerCharge(quantity, plan) : regularCharge(quantity, plan);
```
Mechanics: Extract Function on the condition, then on each branch body. Test after each.
The condition's name carries the business meaning ("isSummer", "isEligibleForRefund").

## Consolidate Conditional Expression
Before:
```java
if (employee.seniority() < 2) return 0;
if (employee.monthsDisabled() > 12) return 0;
if (employee.isPartTime()) return 0;
```
After:
```java
if (isNotEligibleForDisability(employee)) return 0;

private boolean isNotEligibleForDisability(Employee e) {
    return e.seniority() < 2 || e.monthsDisabled() > 12 || e.isPartTime();
}
```
Mechanics: ensure none of the conditions has side effects; combine two at a time with
`||` (sequential checks with the same result) or `&&` (nested ifs); test; then Extract
Function on the combined condition.
Only consolidate checks that are really ONE decision. If they are independent reasons
(that may later get different results or messages), keep them separate.

## Related moves
- Replace nested conditional with guard clauses for special cases.
- Replace conditional with polymorphism when the same switch on type recurs.
- Boolean algebra: apply De Morgan to remove negations (`!(a && b)` -> `!a || !b`) and
  prefer positive names (`isEligible` over `isNotIneligible`).

## Verify
- [ ] Tests cover every branch before and after (branch coverage report).
- [ ] The resulting condition reads as a sentence of domain language.
