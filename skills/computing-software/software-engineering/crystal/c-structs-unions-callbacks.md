---
id: computing-software.software-engineering.crystal.c-structs-unions-callbacks
name: c-structs-unions-callbacks
category: computing-software
field: software-engineering
product: crystal
tags: [c-structs-unions-callbacks, c-bindings, c-struct, c-union, c-enum, callback, function-pointer, proc-to-c, boxing, userdata, crystal]
level: advanced
status: docs-checked
description: "Declare struct, union and enum in a Crystal lib, create them on the stack, pass Procs as C callbacks and pass closures through Box.box and @[Raises]."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/c_bindings/struct.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/c_bindings/union.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/c_bindings/enum.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/c_bindings/callbacks.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/annotations/built_in_annotations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# C structs, unions, enums and callbacks

Goal: bind richer C APIs.

```crystal
lib C
  struct TimeZone
    minutes_west : Int32
    dst_time : Int32
  end

  union IntOrFloat
    some_int : Int32
    some_float : Float64
  end

  enum SomeEnum : Int8
    Zero
    Two = 2
  end

  fun callback(f : Int32 -> Int32)
end

tz = C::TimeZone.new minutes_west: 1, dst_time: 2
```
- `Struct.new` allocates the struct on the stack with all fields zeroed; `uninitialized C::TimeZone` skips the zeroing. The same holds for unions. Fields of the same type can share a line (`minutes_west, dst_time : Int32`), and lib structs can `include` other lib structs.
- C structs and unions are passed and returned by value (copies), so a method that sets a field on its argument does not change the caller's value.
- A lib `enum` member type defaults to `Int32`, and its values can use `+ - * / & | << >> %`. A different type is chosen with `enum Name : Int8`.
- Callbacks are Procs: `X.callback ->(x) { x + 1 }` (parameter types may be omitted inline), `nil` passes NULL. They cannot form closures; the compiler errors at compile time or raises at runtime.
- To pass state, give the C function a `data : Void*` parameter, `box = Box.box(callback)`, pass `box` as the data, and inside the non-closure callback use `Box(typeof(callback)).unbox(data)`. Save the box in Crystal (for example `@@box`) so the GC does not collect it.
- If a C function runs a user callback that might raise, mark it `@[Raises]`; otherwise `begin/rescue` around the call may not work as expected.
- `@[Packed]` marks a C struct as packed (no padding between fields).

Gotchas:
- The C library stores the callback, but Crystal's GC cannot know that, so keep the box referenced.
- A `@[Extern(union: true)]` Crystal struct can behave like a C union.

Verify: the callback increments a counter stored in the boxed object.

## Checked

2026-11-03. Confirmed against the Crystal book pages for C struct, union, enum, callbacks (including Box and `@[Raises]`) and built-in annotations (`Packed`, `Extern`).
Removed: the one-line `struct Point; ...; end` form, `Pointer(...).malloc` heap allocation and `pointerof(p)` for structs, the "callbacks cannot raise exceptions across C frames safely" and "GC does not scan C-allocated memory" claims, and the "enum maps to a C enum (Int32)" wording (the type is configurable).
Method: documentation only; no commands were run.
