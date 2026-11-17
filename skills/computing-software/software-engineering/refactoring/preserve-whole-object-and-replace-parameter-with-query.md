---
id: computing-software.software-engineering.refactoring.preserve-whole-object-and-replace-parameter-with-query
name: preserve-whole-object-and-replace-parameter-with-query
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, refactoring-apis, preserve-whole-object, replace-parameter-with-query, replace-query-with-parameter, long-parameter-list, fowler-catalog]
level: practitioner
status: draft
description: "Shorten parameter lists with Preserve Whole Object and Replace Parameter with Query, and know when the inverse (Replace Query with Parameter) improves purity."
sources:
  - https://refactoring.com/catalog/preserveWholeObject.html
  - https://refactoring.com/catalog/replaceParameterWithQuery.html
  - https://refactoring.com/catalog/replaceQueryWithParameter.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Preserve Whole Object / Replace Parameter with Query

## Preserve Whole Object
**Smell:** caller pulls several values from one object to pass them separately.
```javascript
const low = room.daysTempRange.low, high = room.daysTempRange.high;
if (!plan.withinRange(low, high)) alerts.push("out of range");
// after
if (!plan.withinRange(room.daysTempRange)) alerts.push("out of range");
```
Mechanics:
1. Create an empty function with the desired parameters (`xxNewWithinRange(range)`).
2. Make its body call the old function, extracting the values.
3. Switch callers one by one; test.
4. Inline the old function into the new one; rename the new one to the old name.

Do not apply when you do not want the function to depend on the whole object's type (crossing module boundaries, or the callee lives in a lower layer that must not know the higher type). Then a parameter object or plain values are right.

## Replace Parameter with Query
**Smell:** a parameter whose value the function could determine itself; callers are forced to compute it.
```python
def final_price(base_price, discount_level): ...
final_price(self.base_price, self.discount_level)      # discount_level derivable from self
# after
def final_price(self, base_price): ... uses self.discount_level
```
Mechanics: Extract Function on the calculation if needed, replace references to the parameter with the query, then Change Function Declaration to drop the parameter.

## The inverse: Replace Query with Parameter
Move a query out to the caller to make the function **pure** (referentially transparent) or to remove a dependency on a global/clock/config:
```python
def target_temp(plan): return plan.temp if thermostat.selected_temp > plan.temp else ...   # global read
def target_temp(plan, selected_temp): ...                                                  # pure, testable
```
Typical targets: `datetime.now()`, `random`, singletons, environment variables. Inject the value (or a clock/random source).

## Decision rule
Fewer parameters is good, but not at the cost of hidden dependencies. Prefer the query when the value is the callee's own responsibility; prefer the parameter when it ties the callee to global or mutable state.

## Verify
- [ ] Call sites shrink; no callee reaches into globals that tests cannot control.
