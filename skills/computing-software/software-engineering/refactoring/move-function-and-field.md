---
id: computing-software.software-engineering.refactoring.move-function-and-field
name: move-function-and-field
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, moving-features, move-function, move-field, feature-envy, cohesion, fowler-catalog]
level: practitioner
status: draft
description: "Move Function and Move Field to put behaviour and data where they are used most (feature envy), with mechanics for moving data that is persisted or shared."
sources:
  - https://refactoring.com/catalog/moveFunction.html
  - https://refactoring.com/catalog/moveField.html
  - https://refactoring.guru/smells/feature-envy
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Move Function / Move Field

## Signals
- **Feature envy:** a method uses another object's data more than its own.
- A function reaches into another module for most of its inputs.
- Every change to one record means passing an extra field to another, or two records always change together (data clump split across them).

## Move Function mechanics
1. Look at everything the function uses in its current context; decide whether helpers move with it.
2. Check for polymorphism: if it overrides or is overridden, moving is harder.
3. Copy the function to the target, adjusting to the new home (the source object may become a parameter).
4. Make the original a delegating call to the new one; test.
5. Inline the delegating function into callers (or keep it if many callers and it reads well); test.
IDE: IntelliJ F6 Move, Rider/ReSharper "Move instance method", VS Code TypeScript "Move to file", Rope/PyCharm Move.

## Move Field mechanics
1. Encapsulate the field (all access via accessors) so moving changes one place.
2. Create the field and accessors on the target.
3. Make the source accessors read/write the target field; test.
4. Remove the source field once nothing references it.

## Persisted or shared data
Moving a field between tables or documents is a data migration, so use expand-contract:
1. Add the new column; write to both places (dual write).
2. Backfill existing rows in batches.
3. Switch reads to the new location; verify (compare counts/checksums).
4. Stop writing the old column; drop it in a later release.
Same for API fields: add the new one, deprecate the old, remove after consumers move.

## Gotchas
- Moving into a class hierarchy (shared field in a superclass) can change object size and serialisation.
- Circular imports after a move point to a missing third module.
- Moving functions across packages changes their public surface; keep a deprecated re-export for external callers.

## Verify
- [ ] Tests green after each step; no field accessed outside its new owner (grep or ArchUnit rule).
- [ ] For persisted moves, reconciliation query shows zero mismatches before dropping the old column.
