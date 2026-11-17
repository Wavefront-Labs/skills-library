---
id: computing-software.software-engineering.software-architecture.visitor-pattern
name: visitor-pattern
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, behavioral-patterns, visitor-pattern, gof, double-dispatch, ast, pattern-matching]
level: practitioner
status: draft
description: "Apply the Visitor pattern to add operations over a stable class hierarchy (ASTs, document trees) via double dispatch, and when sealed types plus pattern matching replace it."
sources:
  - https://refactoring.guru/design-patterns/visitor
  - https://craftinginterpreters.com/representing-code.html#the-visitor-pattern
  - https://openjdk.org/jeps/441
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Visitor pattern

**Intent (GoF):** represent an operation to be performed on the elements of an object structure, letting you define new operations without changing the classes of the elements.

## Trade-off (the expression problem)
- Visitor makes adding **operations** easy (new visitor class) and adding **element types** hard (every visitor changes).
- Plain polymorphic methods make the opposite trade.
Use Visitor when the hierarchy is stable and operations keep growing: compiler ASTs (type check, optimise, codegen, pretty-print), document models, IR passes.

## Classic double dispatch
```java
interface Expr { <R> R accept(Visitor<R> v); }
record Num(double value) implements Expr { public <R> R accept(Visitor<R> v) { return v.visitNum(this); } }
record Add(Expr l, Expr r) implements Expr { public <R> R accept(Visitor<R> v) { return v.visitAdd(this); } }

interface Visitor<R> { R visitNum(Num n); R visitAdd(Add a); }

class Evaluator implements Visitor<Double> {
    public Double visitNum(Num n) { return n.value(); }
    public Double visitAdd(Add a) { return a.l().accept(this) + a.r().accept(this); }
}
```
The first dispatch picks `accept` by element type, the second picks `visitX` by visitor type.

## Modern replacement: sealed types + exhaustive matching
```java
sealed interface Expr permits Num, Add {}
static double eval(Expr e) {
    return switch (e) {
        case Num n -> n.value();
        case Add(Expr l, Expr r) -> eval(l) + eval(r);
    };   // compiler errors if a new permitted subtype is unhandled
}
```
Same idea in Rust `match` on enums, Kotlin `when` on sealed classes, TypeScript discriminated unions with a `never` check, Scala/F#/OCaml ADTs. Prefer this where available: less boilerplate, exhaustiveness checked by the compiler.

## Practical notes
- Provide a base visitor with default "visit children" traversal so concrete visitors override only the nodes they care about (ANTLR `BaseVisitor`, Python `ast.NodeVisitor`/`NodeTransformer`, Babel/ESLint visitor objects keyed by node type).
- Visitors that transform return new nodes rather than mutating during traversal.
- Deep trees: recursive visitors can blow the stack; use an explicit stack for very deep input.

## Verify
- [ ] Adding a node type produces compile errors in every visitor/switch (exhaustiveness), not silent fallthrough.
- [ ] Round-trip tests: parse -> print visitor -> parse yields an equal tree.
