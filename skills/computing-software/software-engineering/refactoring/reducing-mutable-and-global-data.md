---
id: computing-software.software-engineering.refactoring.reducing-mutable-and-global-data
name: reducing-mutable-and-global-data
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, mutable-data, global-data, code-smells, immutability, encapsulate-variable]
level: practitioner
status: draft
description: "Tame the Mutable Data and Global Data smells: encapsulate globals, narrow their scope, split variables, separate queries from modifiers, and move to immutable values."
sources: ["https://martinfowler.com/books/refactoring.html", "https://refactoring.com/catalog/encapsulateVariable.html", "https://refactoring.com/catalog/separateQueryFromModifier.html", "https://refactoring.com/catalog/changeReferenceToValue.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reducing mutable and global data

Fowler lists **Global Data** and **Mutable Data** as smells: any code anywhere can change the value,
and finding who did is hard. Bugs appear far from their cause.

## Global data (module variables, singletons, static fields, class-level mutable defaults)
1. **Encapsulate Variable**: wrap the global in functions/accessors so every read/write goes through
   one place you can log, guard or break on.
2. Narrow visibility: make it module-private; expose only what callers need.
3. Move it into an object passed explicitly (context/config object, dependency injection), so
   dependencies are visible in signatures and tests can supply their own.
4. Make it immutable once initialised (frozen config loaded at startup).
Legacy code with many static dependencies: see Encapsulate Global References / introduce instance
setter (Feathers) to get tests around it first.

## Mutable data
- **Split Variable**: a variable assigned for two purposes becomes two variables (ideally `const`).
- **Slide Statements / Extract Function** to group mutation with what it affects.
- **Separate Query from Modifier**: functions that both return a value and change state become two.
- **Remove Setting Method** for fields that shouldn't change after construction.
- **Replace Derived Variable with Query**: compute instead of storing and updating.
- **Change Reference to Value**: share immutable values; changes create new instances.
- **Combine Functions into Transform** returning new copies instead of mutating inputs.

## Tooling that helps
`const`/`final`/`readonly`/`val` by default; linters (`prefer-const`, `no-param-reassign`, Ruff `B006`
mutable default args, Error Prone); immutable collections (`List.of`, `ImmutableList`, `tuple`,
`frozenset`, `ReadonlyArray`, Immer for structured updates).

## Watch for
Mutable globals in multithreaded code (data races), test pollution (one test changes a global and
another fails depending on order: run tests in random order to expose it).
