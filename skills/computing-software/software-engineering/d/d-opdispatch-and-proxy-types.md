---
id: computing-software.software-engineering.d.d-opdispatch-and-proxy-types
name: d-opdispatch-and-proxy-types
category: computing-software
field: software-engineering
product: d
tags: [d-opdispatch-and-proxy-types, operator-overloading, opdispatch, proxy, wrapper, alias-this, typecons, dynamic-dispatch, forwarding, d]
level: advanced
status: docs-checked
description: "Forward calls dynamically with opDispatch, compose wrappers with alias this and std.typecons Proxy/wrap, and implement dynamic-style APIs with checked names."
sources:
  - https://dlang.org/spec/operatoroverloading.html
  - https://dlang.org/spec/struct.html
  - https://dlang.org/phobos/std_typecons.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# opDispatch, alias this and proxy/wrapper types

Goal: build wrappers that behave like their target.

- `opDispatch`: `auto opDispatch(string name, Args...)(Args args) { return mixin("inner." ~ name ~ "(args)"); }` forwards any member name not found in the class or struct, e.g. `w.foo(1)`; constrain with `if (__traits(hasMember, Inner, name))`.
- `alias this` for implicit conversion/forwarding without loss of the wrapper's own members.
- `mixin Proxy!field;` from `std.typecons` generates forwarding for a field; `Typedef!(T, init, cookie)` makes a distinct type (`alias Meters = Typedef!(double, double.init, "m")`).
- `std.typecons.wrap!Interface(obj)` wraps an object to an interface it satisfies structurally; `unwrap!Type` extracts it.

Gotchas:
- `opDispatch` accepts any name, so constrain it to keep errors early.

Verify: unittest forwarding a method and a property through the wrapper.

## Checked
Checked 2026-11-03 against the D spec Operator Overloading page (forwarding with `opDispatch`), Structs page (`alias this`) and the std.typecons page (`Proxy`, `Typedef`, `wrap`, `unwrap`). Removed: property-style and setter claims, the identity and `==` remark, and the `opIndex` + `std.variant` JSON recipe (not confirmed).

Method: documentation only; no commands were run.
