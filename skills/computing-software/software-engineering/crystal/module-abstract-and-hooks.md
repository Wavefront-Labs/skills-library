---
id: computing-software.software-engineering.crystal.module-abstract-and-hooks
name: module-abstract-and-hooks
category: computing-software
field: software-engineering
product: crystal
tags: [module-abstract-and-hooks, modules, abstract-def, included-hook, extended-hook, inherited-hook, interface, contract, crystal]
level: advanced
status: docs-checked
description: "Define Crystal interfaces with abstract def in modules and abstract classes, and how the compiler checks implementations and hooks."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/virtual_and_abstract_types.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/macros/hooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Module hooks and abstract methods

Goal: define interfaces.

```crystal
module Shape
  abstract def area : Float64
end

class Sq
  include Shape

  def area : Float64
    4.0
  end
end
```
- An `abstract def` can be declared in an abstract class or in a module; the compiler checks that all subclasses (or including types) implement it, even if the program never calls them.
- The check matches parameter types and names.
- `abstract class Base` cannot be instantiated (`can't instantiate abstract class Animal` in the book's example).
- Hooks are the macros `included`, `extended`, `inherited`, `method_added`, `method_missing` and `finished`; see macro-hooks-finished for when each runs.

Gotchas:
- Marking a class abstract also lets the compiler treat a union of subclasses as the base type (`Animal+`), so calling a method declared abstract on it compiles.
- `finished` runs after parsing finished, which makes it suitable for registries.

Verify: remove `area` from `Sq` and read the compile error.

## Checked

2026-11-03. Confirmed against the Crystal book "Virtual and abstract types" page (abstract classes, abstract methods in classes and modules, parameter types and names are checked, instantiation error) and the "Hooks" page.
Fixed: the skill said argument names are not checked; the book says types and names are matched. Removed: the example `macro included` that defined `describe`, the exact `abstract def Shape#area must be implemented` error text, and "hooks run before the including class body continues", none of which the docs state.
Method: documentation only; no commands were run.
