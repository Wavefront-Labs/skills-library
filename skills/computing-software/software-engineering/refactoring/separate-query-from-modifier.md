---
id: computing-software.software-engineering.refactoring.separate-query-from-modifier
name: separate-query-from-modifier
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, refactoring-apis, separate-query-from-modifier, command-query-separation, side-effects, fowler-catalog]
level: practitioner
status: verified
description: "Separate Query from Modifier: split functions that both return a value and change state, following command-query separation, with mechanics and the legitimate exceptions."
sources:
  - https://refactoring.com/catalog/separateQueryFromModifier.html
  - https://martinfowler.com/bliki/CommandQuerySeparation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Separate Query from Modifier

**Principle (Meyer's command-query separation):** a function either returns a value (query, no observable side effects) or changes state (command, returns nothing). Queries can then be called freely, reordered, cached and tested without setup.

## Smell
```javascript
function alertForMiscreant(people) {
  for (const p of people) {
    if (p === "Don")  { setOffAlarms(); return "Don"; }
    if (p === "John") { setOffAlarms(); return "John"; }
  }
  return "";
}
```
A caller that only wants to know who the miscreant is also sets off alarms.

## Mechanics
1. Copy the function and name it as a query (`findMiscreant`).
2. Remove every side effect from the copy.
3. Run static checks / tests.
4. Find each call of the original that uses its return value; replace with a call to the query followed by a call to the original. Test.
5. Remove the return values from the original (now a pure modifier, `alertForMiscreant`) and simplify it, possibly using the query.

```javascript
function findMiscreant(people) { return people.find(p => p === "Don" || p === "John") ?? ""; }
function alertForMiscreant(people) { if (findMiscreant(people) !== "") setOffAlarms(); }
```

Run in Node: for the inputs `[]`, `['x']`, `['x','John']`, `['Don','John']` and `['John','Don']` the split version returned the same name as the original and set off the alarms the same number of times (0 or 1), and `Array.prototype.find(...) ?? ""` returns the first match.

## "Observable" side effects
Caching inside a query (memoisation), lazy initialisation, metrics counters and logging do not change observable state; they are allowed.

## Legitimate exceptions
- Atomic read-modify-write in concurrent code: `queue.pop()`, `map.putIfAbsent`, `AtomicInteger.incrementAndGet`, `INSERT ... RETURNING`. Splitting into query + command creates a race (check-then-act). Keep them combined and name them clearly.
- Iterators (`next()`) by design.

## Verify
- [ ] Queries have no writes/I/O (review; in Rust, `&self` vs `&mut self` makes it visible; C++ `const` member functions).
- [ ] Tests can call the query repeatedly with identical results.
