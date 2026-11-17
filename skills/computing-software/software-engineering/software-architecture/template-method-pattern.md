---
id: computing-software.software-engineering.software-architecture.template-method-pattern
name: template-method-pattern
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, behavioral-patterns, template-method, gof, hook-methods, inheritance, hollywood-principle]
level: practitioner
status: draft
description: "Use Template Method to fix an algorithm's skeleton in a base class with overridable steps and hooks; when to prefer composition (Strategy, callbacks) instead."
sources:
  - https://refactoring.guru/design-patterns/template-method
  - https://en.wikipedia.org/wiki/Template_method_pattern
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Template Method pattern

**Intent (GoF):** define the skeleton of an algorithm in an operation, deferring some steps to subclasses, so subclasses redefine certain steps without changing the algorithm's structure.

## Shape
```java
public abstract class DataImporter {
    // The template: final so subclasses cannot reorder the steps.
    public final ImportResult run(Path file) {
        var raw = read(file);
        var rows = parse(raw);
        validate(rows);
        if (shouldDeduplicate()) rows = dedupe(rows);   // hook with default
        return save(rows);
    }
    protected abstract List<Row> parse(byte[] raw);     // primitive operation: must override
    protected boolean shouldDeduplicate() { return false; } // hook: may override
    private byte[] read(Path f) { ... }                // invariant steps stay private
    private void validate(List<Row> rows) { ... }
    private ImportResult save(List<Row> rows) { ... }
}
public class CsvImporter extends DataImporter {
    protected List<Row> parse(byte[] raw) { ... }
}
```
Hollywood principle: "don't call us, we'll call you" - the base class calls the subclass steps.

## Where you already meet it
`HttpServlet.service` calling `doGet`/`doPost`, JUnit `setUp`/`tearDown`, `AbstractList.get` with the rest provided, React class components' lifecycle methods, Django class-based views (`get_queryset`, `get_context_data`).

## Rules
- Mark the template method `final` (Java/C# `sealed override`) and invariant steps private.
- Keep the number of abstract steps small; many hooks mean the skeleton is not really shared.
- Document which hooks are called, in what order, and what state is valid at each.

## Prefer composition when
- Subclasses vary along two independent axes (inheritance explodes: CsvS3Importer, JsonS3Importer...).
- Steps need to be swapped at runtime or tested in isolation.
Then pass the steps in: `Importer(parser=CsvParser(), dedupe=True)` - that is Strategy. Fowler's Replace Subclass with Delegate is the refactoring.

## Verify
- [ ] A test subclass records the call order of steps and asserts the skeleton.
- [ ] No subclass overrides the template method itself.
