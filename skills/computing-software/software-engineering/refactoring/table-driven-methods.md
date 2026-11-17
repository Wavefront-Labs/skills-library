---
id: computing-software.software-engineering.refactoring.table-driven-methods
name: table-driven-methods
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, lookup-table, table-driven-methods, conditional-logic, switch-statements, data-driven]
level: practitioner
status: verified
description: "Replace long switch/if-else chains that map inputs to values or behaviour with lookup tables (maps of data or functions), and know when polymorphism is better."
sources: ["https://www.gov.uk/income-tax-rates", "https://www.oreilly.com/library/view/code-complete-2nd/0735619670/", "https://refactoring.com/catalog/replaceConditionalWithPolymorphism.html", "https://docs.python.org/3/reference/compound_stmts.html#the-match-statement"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replacing switches with lookup tables

McConnell (Code Complete, ch. 18 "Table-Driven Methods"): look information up in a table instead
of encoding it in logic. Shorter, easier to change, often data you can move to configuration.

## Value mapping
```python
# before
def shipping_days(region):
    if region == "UK": return 1
    elif region == "EU": return 3
    elif region == "US": return 5
    else: return 10
# after
SHIPPING_DAYS = {"UK": 1, "EU": 3, "US": 5}
def shipping_days(region): return SHIPPING_DAYS.get(region, 10)
```

## Behaviour dispatch
```ts
const handlers: Record<EventType, (e: Event) => void> = {
  created: onCreated, paid: onPaid, refunded: onRefunded,
};
const h = handlers[e.type];
if (h) h(e); else log.warn("unhandled", e.type);
```
With TypeScript `Record<EventType, ...>` the compiler forces an entry for each enum member (run with tsc 5 `--strict`: omitting `refunded` gives TS2741 "Property 'refunded' is missing").
Do not write `handlers[e.type]?.(e) ?? log.warn(...)`: a handler that returns `undefined` (every `void` handler) triggers the `??` branch, so the warning fires after a successful dispatch (run: "created handled" then "WARN unhandled created").

## Table shapes (McConnell)
- **Direct access**: key -> value (dicts, arrays indexed by enum ordinal).
- **Indexed access**: map a sparse key to an index into a smaller table.
- **Stair-step**: ranges (`income -> tax band`): sorted boundaries + binary search (`bisect` in Python,
  `TreeMap.floorEntry` in Java).
```python
BOUNDS, RATES = [12570, 50270, 125140], [0.0, 0.2, 0.4, 0.45]   # UK bands as published on gov.uk for England, Wales and NI; Scotland differs
rate = RATES[bisect.bisect_left(BOUNDS, income)]   # upper bound inclusive: 12,570 is still in the 0% band
```
`bisect_right` puts a value equal to a boundary in the next band (run: income 12,570 returned 20%, 50,270 returned 40%); pick `bisect_left` when bands are "up to and including". The gov.uk table lists 20% from 12,571 to 50,270, 40% from 50,271 to 125,140 and 45% above, with the Personal Allowance tapering away between 100,000 and 125,140, so a lookup like this gives the band rate, not a full tax calculation (check the current tax year on gov.uk).
- Multi-dimensional: tuple keys `(customer_type, region)`.

## Steps
1. Characterisation tests over every branch, including the default.
2. Build the table beside the conditional; route the function through it.
3. Test, delete the conditional.
4. Optionally move the table to config/data with validation at load.

## Choose polymorphism instead when
Each case has several behaviours that vary together (price, ship, describe) or substantial
logic: subclasses/strategies per type. Tables are best for data-like variation and single
operations.
