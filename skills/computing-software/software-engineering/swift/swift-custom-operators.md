---
id: computing-software.software-engineering.swift.swift-custom-operators
name: swift-custom-operators
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-api-design, custom-operators]
level: practitioner
status: docs-checked
description: "Overload existing operators and declare custom prefix, infix and postfix operators with precedence groups in Swift."
sources: ["https://docs.swift.org/swift-book/documentation/the-swift-programming-language/advancedoperators/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom operators and precedence
Overload an existing operator by writing a type method named for it; declare brand-new ones at global level with the `operator` keyword.

```swift
struct Vector2D { var x = 0.0, y = 0.0 }
extension Vector2D {
    static func + (l: Vector2D, r: Vector2D) -> Vector2D { .init(x: l.x + r.x, y: l.y + r.y) }
    static prefix func - (v: Vector2D) -> Vector2D { .init(x: -v.x, y: -v.y) }
    static func += (l: inout Vector2D, r: Vector2D) { l = l + r }
}

infix operator +-: AdditionPrecedence          // new operator, existing precedence group
extension Vector2D { static func +- (l: Vector2D, r: Vector2D) -> Vector2D { .init(x: l.x + r.x, y: l.y - r.y) } }

prefix operator +++                              // new prefix operator
```

- New operators are declared globally with `prefix`, `infix` or `postfix` before `operator`; the matching method also carries `prefix` or `postfix` (infix needs no modifier on the method).
- Compound assignment (`+=`) takes its left operand `inout`.
- Conform to `Equatable` and let Swift synthesise `==` where possible; `!=` then comes from the standard library by negating `==`.
- A custom infix operator belongs to a precedence group, which sets precedence and associativity. One not placed in a group gets a default group with precedence immediately higher than the ternary conditional operator.
- You do not specify a precedence for prefix or postfix operators; if both are applied to the same operand, the postfix one applies first.
- Only compound assignment operators can be overloaded: the default assignment `=` and the ternary `a ? b : c` cannot.
- Put an operator method that is not essential to a type in an extension.

Gotcha: Swift's precedence and associativity are simpler than C's but not identical, so recheck expressions when porting code. For precedence group syntax and the standard library's groups, see the Swift reference's Operator Declaration section and the standard library's operator declarations page.

Verify: compile a test that uses `a + b`, `-a`, `a += b` and `a +- b` on `Vector2D` and check the results.

## Checked
2026-11-08: read the Advanced Operators chapter of The Swift Programming Language (swift-book source on GitHub) from the overflow operators section to the end (operator methods, custom operators, precedence, result builders); the earlier bitwise section was not needed. Confirmed: operator methods, prefix/postfix, compound assignment, `Equatable`, custom operator declaration, default precedence group, postfix-first note, non-overloadable `=` and ternary. Removed: the `precedencegroup PowerPrecedence` block and `**` example and its verification (syntax lives in the Declarations chapter, not read), the claims about module-wide leakage of public operators and slow type-checking.
Method: documentation only; no commands were run.
