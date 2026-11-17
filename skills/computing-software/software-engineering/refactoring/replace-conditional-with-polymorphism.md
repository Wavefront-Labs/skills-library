---
id: computing-software.software-engineering.refactoring.replace-conditional-with-polymorphism
name: replace-conditional-with-polymorphism
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, conditional-logic, replace-conditional-with-polymorphism, switch-statements, type-code, strategy, open-closed-principle, fowler-catalog]
level: practitioner
status: docs-checked
description: "Replace conditionals that vary on an object's type or state with polymorphic subclasses, so a new variant is a new class instead of an edit in many conditionals."
sources: ["https://refactoring.guru/replace-conditional-with-polymorphism"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replace Conditional with Polymorphism

**Goal:** when conditionals that vary on the object's class, a field value or a method result are repeated in several places, put each variant's behaviour in its own subclass so adding a variant means adding a class, not editing every conditional.

## Smell
```ts
function airSpeed(bird: Bird) {
  switch (bird.type) {
    case "european": return baseSpeed(bird);
    case "african":  return baseSpeed(bird) - loadFactor(bird) * bird.numberOfCoconuts;
    default: throw new Error("unreachable");
  }
}
// and the same switch again in plumage(), ...
```

## Mechanics
1. You need a class hierarchy for the alternatives. If you have none, create one with Replace Type Code with Subclasses (simple, but you cannot also subclass on another property) or Replace Type Code with State/Strategy (a class per property, with the current class delegating to it).
2. If the conditional sits in a method that does other work too, Extract Method first.
3. In each subclass, override the method and copy in the matching branch of the conditional.
4. Delete that branch from the original conditional. Repeat until the conditional is empty, then delete it and declare the method abstract.

```ts
abstract class Bird { abstract airSpeed(): number; }
class European extends Bird { airSpeed() { return this.baseSpeed(); } }
class African extends Bird { airSpeed() { return this.baseSpeed() - this.loadFactor() * this.coconuts; } }
```

## Why it helps
It follows tell-don't-ask (tell the object what to do, let it decide how), removes near-duplicate conditionals, and respects open/closed: a new variant is a new subclass without touching existing code. The payoff grows with the number of scattered conditionals.

## When not to
- A single conditional in one place: leave it.

## Verify
- [ ] Tests green after each branch moves.
- [ ] Adding a new subclass requires no edits to existing conditionals.

## Checked
2026-11-01. Confirmed against the Refactoring Guru page for this technique: when it applies, preparation (type code to subclasses or State/Strategy), the steps, and the benefits. Removed: the sum-type and expression-problem comparison, the variant-of-base-case section and the factory mechanics from Fowler's book, which that page does not state. The refactoring.com catalog page returns no text and the book chapters were not read, so neither is cited.
Method: documentation only; no commands were run.
