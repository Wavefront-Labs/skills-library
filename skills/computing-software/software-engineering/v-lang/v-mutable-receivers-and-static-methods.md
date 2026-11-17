---
id: computing-software.software-engineering.v-lang.v-mutable-receivers-and-static-methods
name: v-mutable-receivers-and-static-methods
category: computing-software
field: software-engineering
product: v-lang
tags: [v-mutable-receivers-and-static-methods, methods, mut receiver, static method, constructor, new, t.new, factory, v-lang]
level: practitioner
status: docs-checked
description: "Mutate struct state with fn (mut s T), write static methods like User.new(), and know when pointer receivers apply."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mutable receivers and static methods

Goal: mutate state and write constructors.

- `fn (mut u User) register() { u.is_registered = true }` changes the object; declare the variable `mut user := User{}` and call `user.register()`. A field changed this way must itself be declared in a `mut:` section.
- A method with a `mut` receiver needs a mutable value; an immutable value parameter cannot call such a method because the mutation would only affect its copy.
- `fn (foo &Foo) bar()` forces pass by reference but `foo` is still immutable; use `(mut foo Foo)` to change it.
- Static methods are declared `fn User.new() User { return User{} }` and called `User.new()`. The docs recommend them over factory functions such as `new_user()`. They are plain functions, not constructors; V has no constructors or classes.
- A static method and an instance method may share a name; `User.draw(...)` is static, `user.draw(...)` is the instance one.
- Static methods can be used as function values: `make_user := User.new`.
- `@[noinit]` structs can only be created inside their module, so expose a factory function for them.
- Prefer returning values over mutating (`user = register(user)`).

Verify: increment twice and assert the field.

## Checked

Date: 2026-11-03. Confirmed in the V documentation (doc/docs.md, "Mutable arguments", "Static type methods", "`[noinit]` structs", "References"). Removed as not stated: builder-style `mut Self` remarks, the `new_xyz()` returning `&Xyz` convention (the docs prefer static methods), and `arr[i].inc()` on arrays.

Method: documentation only; no commands were run.
