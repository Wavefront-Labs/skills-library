---
id: computing-software.software-engineering.ocaml.classes-methods-and-inheritance
name: classes-methods-and-inheritance
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, classes-objects, ocaml-objects, class-definition, inheritance, virtual-class, object-methods]
level: advanced
status: docs-checked
description: "Define classes with instance variables, methods, inheritance, virtual classes and self-types; know when modules and records are better."
sources: ["https://ocaml.org/manual/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Classes and objects

```ocaml
class counter init = object (self)
  val mutable n = init
  method incr = n <- n + 1; self#get
  method get = n
end
let c = new counter 0
let () = ignore (c#incr)
class virtual shape = object method virtual area : float end
class circle r = object inherit shape method area = 3.14159 *. r *. r end
```

## Notes
- Method call: `obj#meth args`. Instance variables (`val`) are private to the class and subclasses.
- Class types are structural: any object with the right methods fits; subtyping is explicit, with coercion `(c :> shape)`.
- Use `object ... end` for immediate objects without a class; `initializer` runs after construction.
- OCaml code is idiomatically written with modules, records and variants; objects are used when you need open recursion or row-polymorphic structural typing (`< area : float; .. >`).

## Self-check
- [ ] `(circle_obj :> shape)` coerces without error.

## Checked

2026-11-03. Confirmed against the OCaml 5.5 manual: the object chapter (classes with val/method, initializer, immediate objects with object ... end, inherit, virtual methods, and the (e :> t) coercion form).

Removed or corrected: the unsourced performance claim about dynamic method lookup.

Method: documentation only; no commands were run.
