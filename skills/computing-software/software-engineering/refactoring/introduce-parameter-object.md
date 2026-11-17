---
id: computing-software.software-engineering.refactoring.introduce-parameter-object
name: introduce-parameter-object
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, refactoring-first-set, introduce-parameter-object, data-clumps, long-parameter-list, value-objects, code-smell]
level: practitioner
status: draft
description: "Replace data clumps and long parameter lists with a parameter object (range, period, address), then move behaviour onto it."
sources: ["https://refactoring.com/catalog/introduceParameterObject.html", "Refactoring, 2nd ed. (Fowler), ch3 Data Clumps / Long Parameter List, ch6 Introduce Parameter Object"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Introduce Parameter Object

**Goal:** when the same group of values travels together through many functions
(`start, end`; `lat, lon`; `street, city, postcode`), make the group an explicit type.

## Smell it fixes
- **Data clumps**: the same 2-4 parameters appear together in many signatures.
- **Long parameter list**: callers pass values in the wrong order and the compiler
  can't tell (`book(roomId, guestId, start, end)` with two ints and two dates).

## Mechanics
1. If no suitable structure exists, create one, preferably an immutable value object:
   ```ts
   class DateRange {
     constructor(readonly start: Date, readonly end: Date) {
       if (end < start) throw new RangeError("end before start");
     }
     contains(d: Date) { return d >= this.start && d <= this.end; }
   }
   ```
2. Test.
3. Use Change Function Declaration to add a parameter of the new type.
4. Test.
5. At each caller, pass an instance of the new structure. Test.
6. For each element of the new structure, replace use of the original parameter with
   the element of the structure; remove the original parameter. Test.

Before / after:
```ts
readingsOutsideRange(station, min, max)        // before
readingsOutsideRange(station, operatingPlan.temperatureRange)   // after
```

## The real payoff
Once the concept has a name, behaviour that was scattered across callers moves onto it
(`range.contains(x)`, `range.overlaps(other)`, validation in the constructor). That is
where the design improves; stopping at a dumb struct captures only half the value.

## Pitfalls
- Grouping values that don't belong together just to shorten a signature creates a
  meaningless "Params" bag; the group should be a domain concept.
- Mutable parameter objects shared between callers: make them immutable.
- Languages with named/keyword arguments reduce the ordering risk but not the clump smell.

## Verify
- [ ] The new type has at least one behaviour or invariant, not just fields.
- [ ] No remaining signatures pass the original values separately.
