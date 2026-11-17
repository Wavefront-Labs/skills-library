---
id: computing-software.software-engineering.software-architecture.mixins-and-traits
name: mixins-and-traits
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, mixins, traits, composition, multiple-inheritance]
level: practitioner
status: draft
description: "Use mixins and traits for reusable behaviour (Python mixins, Scala/PHP/Rust traits, default interface methods) without diamond problems or hidden state coupling."
sources: ["https://docs.python.org/3/tutorial/classes.html#multiple-inheritance", "https://docs.scala-lang.org/tour/mixin-class-composition.html", "https://doc.rust-lang.org/book/ch10-02-traits.html", "https://www.php.net/manual/en/language.oop5.traits.php"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mixins and traits for composition

A **mixin** packages a piece of behaviour to be combined into many classes without being a
standalone "is-a" parent. A **trait** is the language-supported form, often with conflict
resolution and no (or restricted) state.

## By language
- **Python**: mixin classes via multiple inheritance; put mixins left of the base:
  `class OrderView(LoginRequiredMixin, PermissionRequiredMixin, DetailView)`. MRO (C3
  linearisation, `Cls.__mro__`) decides lookup; use `super()` cooperatively in every mixin.
- **Scala**: `class Service extends Base with Logging with Metrics`; linearisation right-to-left.
- **Rust**: traits with default methods; no inheritance of state; blanket impls.
- **PHP**: `use LoggerTrait;` with `insteadof`/`as` for conflicts.
- **Java/C#**: default interface methods (Java 8, C# 8) give behaviour-only mixins.
- **Ruby**: `include`/`prepend` modules. **TypeScript**: class-expression mixin functions.

## Good mixin rules
- Single, orthogonal capability (`JsonSerializableMixin`, `TimestampedMixin`, `ComparableByKey`).
- No `__init__`/constructor with required args; if state is needed, document the attributes the
  host must provide, or make it a separate collaborator.
- Don't depend on other mixins' internals; depend on a small, documented host interface
  (abstract methods).
- Name with a suffix (`...Mixin`) so readers know it isn't a real parent.

## Prefer composition when
The behaviour has its own state and lifecycle, needs to vary at runtime, or you're stacking more
than 2-3 mixins (debugging MRO chains is painful). Delegate to a member object (strategy,
decorator) instead.

## Diamond problem
Two mixins defining the same method: Python's MRO and cooperative `super()` call each once in
order; Scala linearisation similar; PHP/Rust require explicit resolution. Test the combined class,
not each mixin alone.
