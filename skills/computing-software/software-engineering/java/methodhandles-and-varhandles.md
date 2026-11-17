---
id: computing-software.software-engineering.java.methodhandles-and-varhandles
name: methodhandles-and-varhandles
category: computing-software
field: software-engineering
product: java
tags: [java, java-reflection, methodhandles-varhandle, methodhandle, varhandle, invokedynamic, privatelookup, compareandset]
level: advanced
status: docs-checked
description: "Use MethodHandle (invokeExact vs invoke, access checked at creation) and VarHandle (access modes, compareAndSet, array element handles)."
sources:
  - https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/invoke/MethodHandle.html
  - https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/invoke/VarHandle.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MethodHandles and VarHandles

## MethodHandle
```java
private static final MethodHandle LENGTH;
static {
    try {
        LENGTH = MethodHandles.lookup().findVirtual(String.class, "length", MethodType.methodType(int.class));
    } catch (ReflectiveOperationException e) { throw new ExceptionInInitializerError(e); }
}
int n = (int) LENGTH.invokeExact("hello");
```
- `invokeExact` requires the call-site symbolic type descriptor (argument types and the cast of the result) to match the handle's type exactly. Plain `invoke` is more permissive: on mismatch it adjusts the handle as if by `asType`.
- On a mismatch the JVM throws `WrongMethodTypeException`, directly for `invokeExact`, or as a failed `asType` for `invoke`. Type errors that would be linkage errors in static code appear at run time.
- Both methods are declared to throw `Throwable`, so the call site must catch or declare it; anything thrown by the target propagates unchanged.
- Unlike Core Reflection, which checks access on every call, a method handle checks access when it is created. A handle to a non-public method can then be used by anyone who receives it, so do not leak such handles.
- `bindTo(Object)` and `asType(MethodType)` derive new handles.

## VarHandle
```java
private volatile int state;
private static final VarHandle STATE;
static { STATE = MethodHandles.lookup().findVarHandle(Foo.class, "state", int.class); }

STATE.compareAndSet(this, 0, 1);
STATE.getAndAdd(this, 5);
STATE.getAcquire(this); STATE.setRelease(this, 2);
```
- A VarHandle is a dynamically strongly typed reference to a variable or family of variables: static fields, instance fields, array elements, or off-heap components. It is immutable and cannot be subclassed.
- Each access mode is a signature-polymorphic method whose leading arguments are coordinate expressions (for a field, the object) and trailing arguments are values (expected and new for compare-and-set). Arity and types are checked dynamically against the access mode type; a runtime exception is thrown on mismatch.
- Access modes: plain (`get`/`set`), opaque, acquire/release, volatile, plus atomic update modes (`compareAndSet`, `getAndAdd`, `getAndSet`, bitwise operations).
- Plain access is bitwise atomic only for references and primitives of at most 32 bits. Opaque is bitwise atomic and coherently ordered per variable. Acquire reads are ordered after matching release writes. Volatile operations are totally ordered with each other.
- Array elements: `MethodHandles.arrayElementVarHandle(String[].class)` gives coordinates `(String[], int)`; use `avh.compareAndSet(sa, 10, "expected", "new")`.

## Verify
- [ ] A unit test confirms a mismatched `invokeExact` call (wrong return cast) throws `WrongMethodTypeException`.
- [ ] A multi-threaded test of the `compareAndSet` field shows exactly one winner.

## Checked
Method: docs-checked 2026-11-09 against the MethodHandle and VarHandle Javadoc (Java 21). Dropped the dev.java source (page not readable) and unconfirmed claims about static final constant folding, JIT inlining, speed relative to Method.invoke, privateLookupIn and module openness, combinators other than bindTo/asType, and advice about Spring or Jackson.
