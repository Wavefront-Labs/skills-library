---
id: computing-software.software-engineering.java.initialization-order-of-fields-and-constructors
name: initialization-order-of-fields-and-constructors
category: computing-software
field: software-engineering
product: java
tags: [java, java-oop, initialization-order, static-initializer, instance-initializer, constructor-chaining, class-initialization, this-escape]
level: advanced
status: docs-checked
description: "Predict Java class and instance initialization order, and avoid bugs from overridable calls in constructors, static init cycles and this-escape."
sources: ["https://docs.oracle.com/javase/specs/jls/se21/html/jls-12.html#jls-12.4", "https://docs.oracle.com/javase/specs/jls/se21/html/jls-12.html#jls-12.5"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Initialization order

## Class initialization (once, lazily, JLS 12.4)
Triggered by the first instance creation, static method call, or use or assignment of a static field that is not a constant variable. Initializing a class first initializes its superclass, and any superinterfaces that declare default methods; initializing an interface does not by itself initialize its superinterfaces. Then constants are set, and static field initializers and `static {}` blocks run in textual order as though one block. Initialization uses a per-class lock, so it is performed once and a thread waits while another is initializing the class.

## Instance creation (JLS 12.5)
1. Allocate; all instance variables, including those of superclasses, hold default values (0, null, false).
2. The constructor is entered; if it begins with `this(...)`, that constructor is processed recursively first. Otherwise it invokes the superclass constructor (`super(...)`, implicit if absent).
3. After `super(...)` returns: instance initializers and instance variable initializers of this class run in left-to-right textual order.
4. Rest of the constructor body.

```java
class A { A() { init(); } void init() {} }
class B extends A {
    String name = "b";
    @Override void init() { System.out.println(name); }   // prints null!
}
new B();
```
`B.init()` runs inside `A()`, before B's field initializers: `name` still has its default value, null.

## Rules
- Never call overridable methods (non-final, non-private, non-static) from a constructor; the override sees default values, as above.
- Do not publish `this` (register listeners, start threads) from a constructor; use a static factory that finishes construction first.
- Static initialization cycles (A's static init uses B whose static init uses A, on the same thread) see the not-yet-initialized default values; avoid with holder classes or explicit lazy init.
- Constructor chaining: put all validation in the one most-specific constructor and chain others with `this(...)`.

## Gotchas
- An exception from a static initializer is wrapped in `ExceptionInInitializerError` (unless it is already an `Error`), the class is left in an erroneous state, and later attempts to initialize it throw `NoClassDefFoundError`.
- Reading a `static final` constant variable (a primitive or String initialized with a constant expression) does not trigger class initialization.

## Verify
Add print lines (or a debugger watch) and run the `B` example.

## Checked
Checked 2026-11-08 against JLS 21 chapter 12 (sections 12.4 and 12.5, one page).
Removed as unconfirmed there: `Class.forName` as an initialization trigger (reflection is specified elsewhere), the claim about non-constant finals being visible as defaults, and the `javac -Xlint:this-escape` tip (a compiler feature not documented in the JLS).
Method: documentation only; no commands were run.
