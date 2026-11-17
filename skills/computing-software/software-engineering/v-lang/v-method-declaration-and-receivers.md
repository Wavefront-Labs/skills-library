---
id: computing-software.software-engineering.v-lang.v-method-declaration-and-receivers
name: v-method-declaration-and-receivers
category: computing-software
field: software-engineering
product: v-lang
tags: [v-method-declaration-and-receivers, methods, receiver, fn p point, dot call, method syntax, v-lang]
level: intro
status: docs-checked
description: "Declare methods with fn (r T) name(), call them with dot syntax, use short receiver names, and add methods to imported types via aliases."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Methods and receivers

Goal: attach behaviour to types.

- `fn (u User) can_register() bool { return u.age > 16 }`; call `user.can_register()`. V has no classes; a method is a function with a receiver argument between `fn` and the name.
- Convention: short receiver names, preferably one letter, not `self` or `this`.
- Methods must be in the same module as the receiver type. To add methods to an imported type, declare a local alias and use it as the receiver; for a generic receiver the alias repeats the parameters (`type LocalBox[T] = other.Box[T]`).
- The receiver is an immutable argument unless declared `mut`; `fn (foo &Foo)` forces pass by reference but is still immutable.
- Instance methods can be used as unbound function values (`f := User.register`), the receiver becoming the first parameter (`f(mut user)`).
- Embedding a struct promotes its fields and methods (`button.area()` and `button.Size.area()`).

Verify: `assert User{age: 20}.can_register()`.

## Checked

Date: 2026-11-03. Confirmed in the V documentation (doc/docs.md, "Methods", "Embedded structs", "Static type methods", "Immutable function args by default", "References"). Removed as not stated: methods on enums and sum types, method names repeating across types, and the field-and-method name clash remark.

Method: documentation only; no commands were run.
