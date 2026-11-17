---
id: computing-software.software-engineering.software-architecture.composite-pattern
name: composite-pattern
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, structural-patterns, composite-pattern, gof, tree-structures, part-whole-hierarchy, recursion, uniform-treatment]
level: practitioner
status: verified
description: "Use the GoF Composite to treat individual objects and trees of objects uniformly (file systems, UI trees, rule sets, org charts), with safe child management."
sources: ["Design Patterns: Elements of Reusable Object-Oriented Software (Gamma, Helm, Johnson, Vlissides), Composite", "https://refactoring.guru/design-patterns/composite"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Composite

**Intent (GoF):** compose objects into tree structures to represent part-whole
hierarchies; let clients treat individual objects and compositions uniformly.

## When it fits
Recursive structures where operations apply to leaves and groups the same way: files
and directories (size), UI components (render, hit-test), pricing bundles (total),
permission rule groups (`all`/`any`), expression trees (evaluate).

## Shape
```typescript
interface PriceComponent { total(): Money; }

class Product implements PriceComponent {
  constructor(readonly sku: string, private readonly price: Money) {}
  total() { return this.price; }
}

class Bundle implements PriceComponent {
  private readonly items: PriceComponent[] = [];
  constructor(private readonly discountPct: number) {}
  add(c: PriceComponent) { this.items.push(c); return this; }
  total() {
    const sum = this.items.reduce((acc, c) => acc.plus(c.total()), Money.zero());
    return sum.times(1 - this.discountPct / 100);
  }
}
const cart = new Bundle(0).add(new Product("A", eur(10))).add(new Bundle(10).add(new Product("B", eur(5))));
```

## Design decisions
- **Where child management lives**: on the component interface ("transparency": clients
  never check types, but leaves must reject `add`) or only on composites ("safety":
  type-checked, clients occasionally downcast). Most modern code chooses safety.
- **Parent references**: useful for navigation, but keep them consistent on add/remove.
- **Cycles**: a composite added to its own descendant causes infinite recursion; guard
  in `add` if the tree is user-editable.
- **Ordering and caching**: cache expensive aggregates (sizes) and invalidate up the
  parent chain on change.

## Alternatives
In languages with algebraic data types, a recursive sum type plus pattern matching
(`enum Node { Leaf(..), Group(Vec<Node>) }`) is often simpler than an interface hierarchy,
especially when many different operations run over the tree (see Visitor).

## Verify
- [ ] Operations produce identical results for a leaf and a group containing only that leaf (uniformity).
- [ ] Deep trees don't overflow the stack (iterative traversal if depth is user-controlled).
