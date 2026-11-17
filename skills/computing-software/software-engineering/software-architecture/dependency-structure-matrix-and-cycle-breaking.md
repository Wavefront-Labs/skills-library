---
id: computing-software.software-engineering.software-architecture.dependency-structure-matrix-and-cycle-breaking
name: dependency-structure-matrix-and-cycle-breaking
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, architecture-evaluation, dependency-structure-matrix, dependency-cycles, layering, acyclic-dependencies]
level: advanced
status: draft
description: "Analyse module dependencies with a dependency structure matrix and graphs, find cycles and layering violations, and break them with inversion, extraction or moves."
sources: ["https://en.wikipedia.org/wiki/Design_structure_matrix", "https://www.archunit.org/userguide/html/000_Index.html#_cycle_checks", "https://github.com/sverweij/dependency-cruiser", "https://import-linter.readthedocs.io/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dependency structure analysis and cycle breaking

## The DSM
Square matrix, modules on both axes; cell (row i, column j) marks that i depends on j (conventions
vary; tools label it). Ordered by layers (partitioned), a clean layered system is **lower-
triangular**; marks above the diagonal are upward dependencies / cycles. Blocks along the diagonal
show subsystems; tightly coupled clusters appear as dense squares.
Tools: Structure101, NDepend, IntelliJ "Analyze > Dependency Matrix", Lattix; for graphs:
`dependency-cruiser --output-type dot src | dot -Tsvg`, `madge --circular src`, `pydeps`, `jdeps`.

## Find cycles
```
npx madge --circular --extensions ts src
npx depcruise src --config      # rule: no-circular
lint-imports                    # import-linter contracts (layers, independence) for Python
```
ArchUnit: `slices().matching("com.acme.(*)..").should().beFreeOfCycles()`.

## Break a cycle (A -> B -> A)
1. **Dependency inversion**: B depends on an interface owned by A (or a shared abstractions module);
   A implements/provides it. Most common fix.
2. **Extract** the shared piece both need into a new lower module C.
3. **Move** the misplaced class/function to the module that uses it.
4. **Events/callbacks**: B publishes, A subscribes, so B doesn't call A.
5. Merge A and B if they're really one module.
Pick the weakest link: the edge with the fewest references (DSM cell counts show it).

## Keep it fixed
Add the rule to CI (ArchUnit test, depcruise `forbidden` rules, import-linter contracts) with the
current violations as a frozen baseline (ArchUnit `FreezingArchRule`), so new cycles fail while
old ones are burned down.
