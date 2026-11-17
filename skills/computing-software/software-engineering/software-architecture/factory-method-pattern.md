---
id: computing-software.software-engineering.software-architecture.factory-method-pattern
name: factory-method-pattern
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, creational-patterns, factory-method, gof, virtual-constructor, static-factory, dependency-inversion]
level: practitioner
status: draft
description: "Apply the GoF Factory Method: let subclasses or injected creators decide which concrete product to build, and when a static factory or plain constructor suffices."
sources: ["Design Patterns: Elements of Reusable Object-Oriented Software (Gamma, Helm, Johnson, Vlissides), Factory Method", "https://refactoring.guru/design-patterns/factory-method", "https://refactoring.com/catalog/replaceConstructorWithFactoryFunction.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Factory Method

**Intent (GoF):** define an interface for creating an object, but let subclasses decide
which class to instantiate.

## When it fits
- A framework/base class runs an algorithm that needs a product object, but the concrete
  product depends on the application (`Document` creates its `Page` type).
- Creation must be hookable in tests or plugins without the caller knowing concrete types.

## Classic form
```java
abstract class ReportExporter {
    public final byte[] export(Report r) {
        Writer w = createWriter();        // factory method
        w.header(r.title()); r.rows().forEach(w::row);
        return w.finish();
    }
    protected abstract Writer createWriter();
}
class CsvExporter extends ReportExporter { protected Writer createWriter() { return new CsvWriter(); } }
```

## Modern variants (more common today)
- **Injected creator function**: pass `Supplier<Writer>` / a lambda instead of
  subclassing. Composition over inheritance; same intent.
- **Static factory method** (Effective Java item 1): `Duration.ofSeconds(5)`,
  `List.of(...)`. Named, can cache instances, can return subtypes. Not GoF Factory
  Method, but often what people mean.
- **Registry / map of creators** keyed by type string for plugin-style creation:
  `Map<String, Supplier<Parser>>`.

## Consequences
+ Callers depend on the abstract product, not concrete classes.
+ Adding a product = new subclass/creator, no edits to the algorithm.
- Parallel hierarchies (one creator subclass per product) when overused.

## Smells it addresses / creates
Use it to remove `switch (type) { case "csv": new CsvWriter() ... }` scattered across
the codebase (centralise the switch in one factory). Don't introduce a factory for a
class with one implementation and no test seam need; `new` is fine.

## Verify
- [ ] Each factory has more than one product or a real substitution need (tests/plugins).
- [ ] Callers of the algorithm never reference concrete product classes.

Related: computing-software.software-engineering.software-architecture.abstract-factory-pattern
