---
id: computing-software.software-engineering.swift.swift-result-typed-throws
name: swift-result-typed-throws
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-errors, result-typed-throws]
level: advanced
status: docs-checked
description: "Use Result and typed throws where explicit error types help and know when not to."
sources: ["https://docs.swift.org/swift-book/documentation/the-swift-programming-language/errorhandling/", "https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Result type and typed throws
- `Result` stores the outcome of throwing code so other code can handle the error later. It lets you call throwing code from nonthrowing code: `Result { try listDownloadedPhotos(inGallery: "A Rainy Weekend") }` produces a `Result<[String], Error>`.
- Typed throws writes the error type after `throws`: `func summarize(_ ratings: [Int]) throws(StatisticsError)`. Inside, use the short form `throw .noRatings`, and the compiler rejects any other error type. Callers can catch it exhaustively: `do throws(StatisticsError) { try summarize(r) } catch { switch error { ... } }`, and a new enum case then breaks non-exhaustive `switch` statements at compile time.
- Plain `throws` is the same as `throws(any Error)`; a function that never throws can be written `throws(Never)`. If a function or `do` block throws errors of only one type, Swift infers typed throws; write `throws(any Error)` to opt out.
- Most Swift code does not specify error types, because you rarely know every error ahead of time and libraries add new ones. The book names three cases where a specific type fits: embedded systems without dynamic allocation (throwing `any Error` boxes the error and allocates, a specific type avoids heap allocation), errors that are an implementation detail of a library and always handled inside it, and code that only propagates errors described by generic parameters.
- A typed-throws function can be called from a regular throwing function, which then throws `any Error`.

Verify: declare an enum error, a `throws(MyError)` function and a `do throws(MyError)` block; add an enum case and confirm the `switch` fails to compile until updated.

## Checked
2026-11-08: read the Specifying the Error Type section (typed throws, `do throws`, `throws(Never)`, inference) of the Error Handling chapter, and the Defining and Calling Asynchronous Functions section of the Concurrency chapter (the `Result { try ... }` example), both from The Swift Programming Language (swift-book source on GitHub); the rest of Error Handling was not read. Removed: the `Result<Success, Failure: Error>` signature and `.get()` claim, the "arrived with Swift 6 / SE-0413" claim, the error-mapping advice, `swift --version` verification (not in these pages), and the landing-page sources.
Method: documentation only; no commands were run.
