---
id: computing-software.software-engineering.refactoring.remove-subclass-refactoring
name: remove-subclass-refactoring
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, remove-subclass, inheritance, fowler, replace-subclass-with-fields]
level: practitioner
status: draft
description: "Apply Fowler Remove Subclass: fold a subclass that does too little back into its superclass as a field or flag, safely and in small steps."
sources: ["https://refactoring.com/catalog/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Remove Subclass

**When:** a subclass varies only by constants or a trivial method; or over time it was emptied out. The reverse of Replace Type Code with Subclasses.

## Mechanics (small steps, tests green each time)
1. Find every creation of the subclass (`new Sub(...)`, factories). Replace constructor calls with a factory method on the superclass if there is not one yet (Replace Constructor with Factory Function).
2. If clients test the type (`instanceof Sub`, switch on class), first move that check into a method on the superclass (Extract Function, Move Function) and use it.
3. Add a field to the superclass to hold what the subclass type represented (a type code, enum or the specific value).
4. Make the subclass constructor/factory set that field.
5. Move subclass methods into the superclass, guarded by the field where behaviour differs (use Replace Conditional with Polymorphism only if variation is real).
6. Delete the subclass once nothing references it; run tests.

## Example sketch
`Female extends Person { isMale() false }` becomes `Person { boolean male; isMale() returns male }` with `Person.createFemale()`.

## Judgement
Do it when the hierarchy costs more than it earns: little behaviour, no extension point, serialisation or persistence mappings complicated by the subtype. Keep subclasses that carry real polymorphic behaviour.

## Verify
All tests pass at every step; searching the codebase finds no references to the removed class; serialised data or database discriminators are migrated if they used the class name.
