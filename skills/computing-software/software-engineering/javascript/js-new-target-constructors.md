---
id: computing-software.software-engineering.javascript.js-new-target-constructors
name: js-new-target-constructors
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, new-target, js-functions]
level: advanced
status: docs-checked
description: "Use new.target to detect construction without new and to see which class new was called on, including via Reflect.construct."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/new.target"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# new.target

- `new.target` is a constructable function or `undefined`. In a plain function call it is `undefined`, so `if (!new.target) throw new Error("Foo() must be called with new")` detects a missing `new`.
- In a class constructor it is the class `new` was called upon, which may be a subclass: with `class B extends A`, `new B()` makes `new.target.name` be `"B"` inside `A`'s constructor.
- If a constructor is called via `Reflect.construct()`, `new.target` is the `newTarget` argument (default: the target). `Base.call(this)` and `apply` call rather than construct, so `new.target` is `undefined` there.
- In arrow functions it is inherited from the surrounding scope; with no enclosing function or class binding it is a syntax error. In static initialization blocks it is `undefined`.
- It is available only inside function and class bodies; elsewhere it is a syntax error.
- Prefer `class` and `extends` over `Reflect.construct` for subclassing built-ins in ES6 code.

Self-check: `Foo()` without `new` throws; `new B()` logs `"B"` from `A`'s constructor.

## Checked

Date: 2026-11-03. Confirmed on MDN Operators/new.target: values in functions, classes, Reflect.construct, call/apply, arrows, static blocks, the syntax-error rule, class-over-Reflect advice. Removed as not stated there: which function kinds are constructible, hoisting differences, super and home-object remarks, and the `new (() => {})` self-check.

Method: documentation only; no commands were run.
