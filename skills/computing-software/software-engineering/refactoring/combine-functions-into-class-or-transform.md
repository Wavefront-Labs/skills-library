---
id: computing-software.software-engineering.refactoring.combine-functions-into-class-or-transform
name: combine-functions-into-class-or-transform
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, refactoring-first-set, combine-functions-into-class, combine-functions-into-transform, derived-data, enrichment, cohesion]
level: practitioner
status: draft
description: "Gather functions that operate on the same data into a class, or into a transform that enriches a record with derived values, to stop duplicated derivation logic."
sources: ["https://refactoring.com/catalog/combineFunctionsIntoClass.html", "https://refactoring.com/catalog/combineFunctionsIntoTransform.html", "Refactoring, 2nd ed. (Fowler), ch6"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Combine Functions into Class / into Transform

**Goal:** when several functions all take the same record and compute things from it,
give that group one home so derived values are calculated in one place.

## Symptom
```js
const base = baseRate(reading.month, reading.year) * reading.quantity;   // in billing.js
const taxable = Math.max(0, base - taxThreshold(reading.year));           // in report.js
const base2 = baseRate(reading.month, reading.year) * reading.quantity;  // duplicated in ui.js
```

## Option A: Combine Functions into Class
```js
class Reading {
  constructor(data) { this._data = data; }
  get quantity() { return this._data.quantity; }
  get baseCharge() { return baseRate(this._data.month, this._data.year) * this.quantity; }
  get taxableCharge() { return Math.max(0, this.baseCharge - taxThreshold(this._data.year)); }
}
```
Mechanics: Encapsulate Record on the common data; Move Function each related function
into the class; extract any duplicated derivation logic into methods. Choose this when
the source data can change (derived values recomputed on access) or when you want
methods alongside the data.

## Option B: Combine Functions into Transform
```js
function enrichReading(original) {
  const result = structuredClone(original);       // never mutate the input
  result.baseCharge = calculateBaseCharge(result);
  result.taxableCharge = Math.max(0, result.baseCharge - taxThreshold(result.year));
  return result;
}
```
Mechanics: create a transform that deep-copies the input; Move each derivation into it,
adding a field; change callers to read the field. Choose this for read-only data in
pipelines (JSON from an API, rows from a query, functional codebases): the enriched
record flows on.

## Choosing
Fowler's rule: if the source data gets updated in place, prefer the class; a transform's
derived fields go stale when someone modifies the original data later.

## Verify
- [ ] Each derivation exists in exactly one place (grep for the formula).
- [ ] Transform tests assert the input object is not mutated.
