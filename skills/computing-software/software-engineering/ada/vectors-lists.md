---
id: computing-software.software-engineering.ada.vectors-lists
name: vectors-lists
category: computing-software
field: software-engineering
product: ada
tags: [ada, vectors-lists, ada-containers]
level: practitioner
status: docs-checked
description: "Ada.Containers.Vectors: instantiate, Append, First_Element, for-of iteration and sorting with Generic_Sorting."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/intro-to-ada/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vectors
```ada
with Ada.Containers.Vectors;
package Int_Vecs is new Ada.Containers.Vectors (Index_Type => Positive, Element_Type => Integer);
V : Int_Vecs.Vector;
V.Append (3);  V.Append (5);
for E of V loop Put_Line (E'Image); end loop;
X := V.First_Element;
```
- `Generic_Sorting` is a child generic of the vector package: instantiate it as a child of your instance, then `Sort` and `Merge` are available.
- A container package must be instantiated before use; `Index_Type` can be a restricted range.
- `for E of V` gives a reference to each element.
## Gotchas
- Each container type from the standard library needs its own instantiation.
## Self-check
Sort a vector with an instantiated `Generic_Sorting` and print it.

## Checked
2026-11-03. Confirmed in Introduction to Ada, Standard Library: Containers: instantiation, `Append`, `First_Element`, `for E of`, `Generic_Sorting` with `Sort`/`Merge`. Removed Doubly_Linked_Lists, Indefinite_Vectors, Reserve_Capacity, V (1) indexing and the Program_Error tampering claim (not on the pages read).
Method: documentation only; no commands were run.
