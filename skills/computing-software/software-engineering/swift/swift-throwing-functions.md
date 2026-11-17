---
id: computing-software.software-engineering.swift.swift-throwing-functions
name: swift-throwing-functions
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-errors, throwing-functions]
level: intro
status: docs-checked
description: "Declare, throw and handle errors with throws, try, try? and do-catch."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# throws try and catch
- Errors are types conforming to `Error`: `enum VendingMachineError: Error { case insufficientFunds(coinsNeeded: Int) }`; a throwing function is declared `func canThrowErrors() throws -> String` and called with `try`.
- Handle with `do { try ... } catch VendingMachineError.insufficientFunds(let coinsNeeded) { ... } catch { ... }`; catch clauses need not be exhaustive, and unmatched errors propagate.
- `try?` converts an error to an optional (detail is lost); `try!` gives a runtime error if an error is thrown.
- `defer` runs just before leaving the scope; multiple defers run last-written first. Use it for cleanup.
- `rethrows` marks a function that throws only if its closure parameter throws.
Verify: test each error case produces the expected catch branch.

## Checked
2026-11-03. Confirmed against the Swift Programming Language book (swiftlang/swift-book source): ErrorHandling chapter and Declarations reference (rethrows).
Removed: invented NetError and load examples, replaced with the book's own.
Method: documentation only; no commands were run.
