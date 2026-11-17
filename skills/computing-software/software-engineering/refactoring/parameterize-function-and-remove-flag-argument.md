---
id: computing-software.software-engineering.refactoring.parameterize-function-and-remove-flag-argument
name: parameterize-function-and-remove-flag-argument
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, refactoring-apis, parameterize-function, remove-flag-argument, boolean-parameters, duplicate-code, fowler-catalog]
level: practitioner
status: draft
description: "Parameterize Function to merge near-duplicate functions, and Remove Flag Argument to replace boolean switches with explicit functions; mechanics and API readability rules."
sources:
  - https://refactoring.com/catalog/parameterizeFunction.html
  - https://refactoring.com/catalog/removeFlagArgument.html
  - https://martinfowler.com/bliki/FlagArgument.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Parameterize Function / Remove Flag Argument

They pull in opposite directions: merge functions that differ only by a **value**, split functions whose argument selects a different **behaviour**.

## Parameterize Function
```python
def ten_percent_raise(p): p.salary *= 1.10
def five_percent_raise(p): p.salary *= 1.05
# after
def raise_salary(p, factor): p.salary *= 1 + factor
```
Mechanics:
1. Pick one of the similar functions.
2. Change Function Declaration to add the literal as a parameter.
3. Replace the literal in the body with the parameter; update callers to pass the value; test.
4. For each other similar function, replace calls with the parameterised one; test; delete it.
Range-based bands (`bottom_band`, `middle_band`, `top_band` with different bounds) collapse into `within_band(usage, bottom, top)`.

## Remove Flag Argument
**Smell:** `book_concert(customer, True)` - the call site does not say what `True` means, and the function body is an `if flag:` fork of two behaviours.
```python
# before
def deliver_date(order, is_rush): ...
deliver_date(order, True)
# after
def rush_delivery_date(order): ...
def regular_delivery_date(order): ...
```
Mechanics:
1. Create an explicit function for each value of the flag (Decompose Conditional first if the branching is tangled).
2. Replace callers that pass a literal with the matching explicit function.
3. When a caller passes a computed value (`deliver_date(order, order.priority == "rush")`), keep a dispatching function for those, or push the decision to the caller.

## Rules of thumb
- A boolean literal at a call site is the trigger. If the flag is data flowing through (from config or a request), a parameter is fine.
- Several flags multiply combinations; consider a parameter object or separate functions.
- Languages with keyword-only arguments soften the readability issue (`deliver_date(order, *, rush)` forces `rush=True`), but not the dual-behaviour body.

## Verify
- [ ] No boolean literal arguments at call sites of the refactored API (lint: Sonar S2301, `flake8-boolean-trap` FBT001/FBT003, ruff FBT).
- [ ] Tests green after each caller switch.
