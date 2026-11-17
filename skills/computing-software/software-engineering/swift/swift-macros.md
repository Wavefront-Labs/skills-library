---
id: computing-software.software-engineering.swift.swift-macros
name: swift-macros
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-api-design, swift-macros]
level: advanced
status: docs-checked
description: "Use and write Swift macros (freestanding and attached) with SwiftSyntax, declaration roles and testing."
sources: ["https://docs.swift.org/swift-book/documentation/the-swift-programming-language/macros/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Swift macros
Macros transform source code at compile time. Expansion is always additive: macros add code but never delete or modify existing code. Input and output are checked as valid Swift and type-correct, and an error in a macro implementation is a compilation error. Two families:
- Freestanding: called with a number sign, such as `#function` or `#warning("...")`; they produce a value or perform a compile-time action (expression role).
- Attached: called with an at sign, such as `@OptionSet<Int>`; they add code to the declaration they are attached to, for example a new method or a protocol conformance.

A macro has a declaration and a separate implementation. The declaration (introduced by `macro`, always `public`) names the macro, its parameters, its roles and the names it generates; `#externalMacro(module:type:)` points at the implementation. Attached macros use upper camel case names, freestanding ones lower camel case.

```swift
@attached(member, names: named(RawValue), named(rawValue),
        named(`init`), arbitrary)
@attached(extension, conformances: OptionSet)
public macro OptionSet<RawType>() =
        #externalMacro(module: "SwiftMacros", type: "OptionSetMacro")

@freestanding(expression)
public macro line<T: ExpressibleByIntegerLiteral>() -> T = /* location of the implementation */
```

Implementing one needs two targets built on SwiftSyntax: a `.macro` target holding the implementation and a library target that exposes it.

```swift
// swift-tools-version: 5.9
import CompilerPluginSupport
// targets:
.macro(name: "MyProjectMacros", dependencies: [
    .product(name: "SwiftSyntaxMacros", package: "swift-syntax"),
    .product(name: "SwiftCompilerPlugin", package: "swift-syntax")]),
.target(name: "MyProject", dependencies: ["MyProjectMacros"]),
```

- `swift package init --type macro` scaffolds a macro package. For an existing package set a tools version of 5.9 or later, import `CompilerPluginSupport`, and list macOS 10.15 or later as a deployment target.
- An expression macro's implementation type conforms to `ExpressionMacro` and implements `expansion(of:in:)`; throwing from it becomes a compiler error at the call site. A `CompilerPlugin` type marked `@main` lists the target's macros in `providingMacros`.

Gotchas:
- An implementation sees only the partial syntax tree of the macro call, runs in a sandbox with no file system or network access, and must not depend on things like the time of day, so it always expands the same way.
- When macros nest, the outer macro expands first.

Verify: unit-test an implementation by building a `SourceFileSyntax` from a string, calling `expand(macros:in:)` with a `BasicMacroExpansionContext`, and comparing the result's `description` with the expected source.

## Checked
2026-11-08: read the whole Macros chapter of The Swift Programming Language (swift-book source on GitHub). Confirmed all statements above against it. Removed: the SE-0382, SE-0389 and SE-0397 references and the evolution proposal source (not read), the `#stringify` example, the extra attached roles list (peer, accessor, member attribute), the trust-prompt and `-skipMacroValidation` advice, `-dump-macro-expansions`, `assertMacroExpansion` and the build-time remark, none of which are on the page. The description no longer mentions a trust prompt.
Method: documentation only; no commands were run.
