---
id: computing-software.software-engineering.ada.generalized-iteration
name: generalized-iteration
category: computing-software
field: software-engineering
product: ada
tags: [ada, generalized-iteration, ada-iterators]
level: advanced
status: draft
description: "Make an Ada type iterable with Default_Iterator, Iterator_Element and a Cursor; 'for E of' and 'for C in'."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/advanced-ada/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Generalized iteration and for-of
```ada
type Bag is tagged private
  with Default_Iterator => Iterate, Iterator_Element => Integer,
       Constant_Indexing => Element_At;
```
- Provide `Iterate` returning `Iterator_Interface'Class` (see Ada.Iterator_Interfaces) and cursor ops `First/Next/Has_Element`.
- `for X of Bag` yields elements; `for C in Bag.Iterate` yields cursors.
## Gotchas
- Boilerplate heavy: copy the Ada.Containers pattern.
## Self-check
Iterate a custom bag in both forms and print elements.
