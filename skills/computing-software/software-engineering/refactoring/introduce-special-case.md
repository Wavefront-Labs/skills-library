---
id: computing-software.software-engineering.refactoring.introduce-special-case
name: introduce-special-case
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, conditional-logic, special-case, null-object, missing-value, null-checks, fowler-catalog]
level: practitioner
status: draft
description: "Replace repeated checks for a special value (null, 'unknown customer', missing config) with a Special Case / Null Object that supplies the default behaviour."
sources: ["https://refactoring.com/catalog/introduceSpecialCase.html", "https://martinfowler.com/eaaCatalog/specialCase.html", "Refactoring, 2nd ed. (Fowler), ch10 Introduce Special Case"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Introduce Special Case (Null Object)

**Goal:** stop repeating `if (customer == null || customer.name == "unknown") ...` in
every caller by giving the special case its own object with sensible behaviour.

## Symptom
```js
const name     = customer === "unknown" ? "occupant" : customer.name;
const plan     = customer === "unknown" ? registry.billingPlans.basic : customer.billingPlan;
const weeksLate = customer === "unknown" ? 0 : customer.paymentHistory.weeksDelinquentInLastYear;
```
Many callers, same check, same default responses.

## Mechanics
1. Add a special-case check property to the subject: `get isUnknown() { return false; }`.
2. Create a special-case class: `class UnknownCustomer { get isUnknown() { return true; } }`.
3. Extract Function on the special-case comparison; make all clients use it. Test.
4. Return the special-case object where the special value used to be produced
   (constructor/repository/factory). Test.
5. Change the comparison function body to use `isUnknown`. Test.
6. Move each common response into the special case:
   ```js
   class UnknownCustomer {
     get isUnknown() { return true; }
     get name() { return "occupant"; }
     get billingPlan() { return registry.billingPlans.basic; }
     get paymentHistory() { return new NullPaymentHistory(); }   // nested special case
   }
   ```
   and delete the now-redundant conditionals in callers. Test after each.

## Variants
- Literal object / record with fixed values when the special case needs no behaviour.
- Transform: enrich a record with special-case fields when working with plain data.
- Language support: `Optional`/`Option` + `map`/`unwrap_or` when the absence is
  meaningful to callers; null object when callers should NOT care.

## Pitfalls
- A null object that silently swallows operations that SHOULD fail (e.g.
  `save()` doing nothing) hides bugs; only give it behaviour that is genuinely the
  correct default.
- Callers that still need to distinguish use `isUnknown`, not identity checks.
- Don't use one null object as a shared mutable singleton.

## Verify
- [ ] grep finds no remaining comparisons with the special value outside the factory.
- [ ] Tests exercise every caller with the special-case object.
