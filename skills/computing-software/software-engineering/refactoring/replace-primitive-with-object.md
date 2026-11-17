---
id: computing-software.software-engineering.refactoring.replace-primitive-with-object
name: replace-primitive-with-object
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, encapsulation, replace-primitive-with-object, primitive-obsession, value-objects, domain-types, fowler-catalog]
level: practitioner
status: docs-checked
description: "Cure primitive obsession by replacing strings and numbers that carry meaning (money, phone, priority) with small immutable value objects that own validation and comparison."
sources:
  - https://refactoring.guru/smells/primitive-obsession
  - https://martinfowler.com/bliki/ValueObject.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replace Primitive with Object

**Smell (primitive obsession):** primitives used instead of small objects for simple tasks such as currency, ranges or special strings for phone numbers; constants used to code information (a role constant for admins); string constants used as field names in data arrays.

## Treatment (from the smell's catalogue entry)
- Group related primitive fields into their own class and move the behaviour that goes with them: Replace Data Value with Object.
- Primitives passed as method parameters: Introduce Parameter Object or Preserve Whole Object.
- Complicated data coded in variables: Replace Type Code with Class, Subclasses or State/Strategy.
- Arrays of mixed data: Replace Array with Object.

## Sketch
```python
@dataclass(frozen=True)
class Priority:
    _LEVELS = ("low", "normal", "high", "rush")
    value: str
    def __post_init__(self):
        if self.value not in self._LEVELS: raise ValueError(f"bad priority {self.value!r}")
    def higher_than(self, other): return self._LEVELS.index(self.value) > self._LEVELS.index(other.value)
```
Steps: wrap the primitive in a small class, make the owner create and hold it, then move validation and comparison onto the class.

## Value object rules (Fowler's bliki)
- Treat the object as a value: equality is by contents, not by reference (JavaScript compares object references by default, so define equality yourself).
- Keep value objects immutable. To change one, make a new object; this avoids aliasing bugs where changing a value in one place surprises another.
- Small things such as points, monies and ranges suit value objects.

## Gotchas
- Do not wrap every primitive; target ones with rules or units.

## Verify
- [ ] Constructing an invalid value raises; tests cover boundaries.
- [ ] Two values with the same contents compare equal.

## Checked
2026-11-01. Confirmed against the Refactoring Guru Primitive Obsession page (symptoms, treatments, payoff) and Fowler's Value Object bliki (equality, immutability, aliasing bugs, examples). Removed: the mechanics copied from the catalogue, ORM and JSON serialiser notes, money-handling rules, branded types and performance claims, which those pages do not state. The refactoring.com catalog page returns no text and is not cited.
Method: documentation only; no commands were run.
