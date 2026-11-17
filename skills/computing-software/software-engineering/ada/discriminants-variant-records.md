---
id: computing-software.software-engineering.ada.discriminants-variant-records
name: discriminants-variant-records
category: computing-software
field: software-engineering
product: ada
tags: [ada, discriminants-variant-records]
level: practitioner
status: draft
description: "Records with discriminants: constrained and unconstrained, defaults, variant parts with case, and mutable records."
sources:
  - https://www.ada-auth.org/standards/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Discriminants and variant records
```ada
type Shape_Kind is (Circle, Rect);
type Shape (K : Shape_Kind := Circle) is record
   case K is
      when Circle => R : Float;
      when Rect   => W, H : Float;
   end case;
end record;
S : Shape := (K => Rect, W => 2.0, H => 3.0);
```
- With a default discriminant the object is mutable: `S := (K => Circle, R => 1.0)`; without one it is constrained at declaration.
- Size discriminant: `type Buf (N : Natural) is record D : String (1 .. N); end record;`
## Gotchas
- Accessing the wrong variant raises `Constraint_Error`.
## Self-check
Read S.R while K = Rect and confirm Constraint_Error.
