---
id: computing-software.software-engineering.mobile-development.swift-error-handling
name: swift-error-handling
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, ios, swift, swift-error-handling, throws, result, typed-throws, localizederror, optional-try]
level: intro
status: draft
description: "Handle errors in Swift idiomatically: Error enums, throws and try, do/catch patterns, Result, try? versus try!, LocalizedError and typed throws in Swift 6."
sources: ["https://docs.swift.org/swift-book/documentation/the-swift-programming-language/errorhandling/", "https://developer.apple.com/documentation/swift/error"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Swift error handling

```swift
enum ProfileError: Error, LocalizedError {
    case notFound(id: String)
    case network(underlying: Error)
    case decoding

    var errorDescription: String? {            // shown by error.localizedDescription
        switch self {
        case .notFound(let id): return "Profile \(id) was not found."
        case .network:          return "Check your connection and try again."
        case .decoding:         return "Unexpected response from the server."
        }
    }
}

func loadProfile(id: String) async throws -> Profile {
    do {
        let (data, response) = try await URLSession.shared.data(from: url(id))
        guard (response as? HTTPURLResponse)?.statusCode == 200 else { throw ProfileError.notFound(id: id) }
        return try JSONDecoder().decode(Profile.self, from: data)
    } catch let e as DecodingError { _ = e; throw ProfileError.decoding }
      catch let e as ProfileError   { throw e }
      catch                         { throw ProfileError.network(underlying: error) }
}
```

## Choosing the form
- `try` inside `do/catch` when you can act; propagate with `throws` otherwise.
- `try?` converts to an optional and discards the error: acceptable for best-effort work, wrong when failure should be shown or logged.
- `try!` crashes on failure; reserve for programmer-error cases such as a bundled resource that must exist.
- `Result<Success, Failure>` is for storing or passing outcomes (callbacks, async publishers); with async/await prefer `throws`.
- Typed throws (`throws(ProfileError)`) arrived in Swift 6.0; untyped `throws` remains the default for public APIs because it keeps evolution flexible.

## Gotchas
- `catch` order matters; the final bare `catch` must be last.
- Do not show `error.localizedDescription` for raw system errors to users; map to your own messages.
- Cancellation surfaces as `CancellationError` or `URLError.cancelled`; do not report it as a failure.

Verify: write unit tests with a stub client that throws each case and assert the mapped `ProfileError` and its `errorDescription`.
