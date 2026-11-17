---
id: computing-software.software-engineering.swift.swift-swift6-migration
name: swift-swift6-migration
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-concurrency, swift6-migration]
level: advanced
status: docs-checked
description: "Migrate a target to the Swift 6 language mode in stages using strict-concurrency checking and upcoming-feature flags."
sources: ["https://github.com/swiftlang/swift-migration-guide/blob/main/Guide.docc/MigrationGuide.md", "https://github.com/swiftlang/swift-migration-guide/blob/main/Guide.docc/MigrationStrategy.md", "https://github.com/swiftlang/swift-migration-guide/blob/main/Guide.docc/EnableDataRaceSafety.md", "https://github.com/swiftlang/swift-migration-guide/blob/main/Guide.docc/IncrementalAdoption.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Swift 6 language mode migration
- The Swift 6 language mode makes the compiler guarantee concurrent programs are free of data races; checks that were optional become required. The mode is opt-in per target; existing projects do not switch without configuration changes. The Swift 6 compiler supports language modes 6, 5, 4.2 and 4, and targets in different modes interoperate.
- Strategy (a starting point, not a mandate): pick a module, enable stricter checking while staying in Swift 5 mode (issues surface only as warnings), then address warnings. Iterate. Start from the outermost root module, or from dependencies you control that have unsafe global state or trivially-`Sendable` types, which can cause many warnings elsewhere.
- Enable one upcoming feature at a time first, in any order: SE-0401 `DisableOutwardActorInference`, SE-0412 `GlobalConcurrency`, SE-0418 `InferSendableFromCaptures`. Then enable complete checking for the module.
- Guiding principle: express what is true now; resist refactoring. After reaching zero warnings, treat the unsafe opt-outs you applied as follow-on refactoring candidates.

```swift
// swift-tools-version: 6.0  -- all targets default to Swift 6 mode
.target(name: "FullyMigrated"),
.target(name: "NotQuiteReadyYet", swiftSettings: [.swiftLanguageMode(.v5)])
// Tools 5.9/5.10, complete checking as warnings:
//   .enableExperimentalFeature("StrictConcurrency")
// Tools 6.0+, target still in a pre-6 mode:
//   .enableUpcomingFeature("StrictConcurrency")
```

- Other switches: `swift build -Xswiftc -swift-version -Xswiftc 6`; `swift -swift-version 6 main.swift`; `-strict-concurrency=complete` (also via `-Xswiftc`) to gauge warnings; Xcode "Swift Language Version" 6 (`SWIFT_VERSION = 6`) and "Strict Concurrency Checking" Complete (`SWIFT_STRICT_CONCURRENCY = complete`).
- To keep supporting older toolchains while using per-target `swiftLanguageMode`, add a version-specific manifest such as `Package@swift-5.9.swift`. A single manifest on tools 5.9 can use `swiftLanguageVersions: [.version("6"), .v5]`.
- Incremental adoption: wrap callback APIs with `withCheckedContinuation` and resume exactly once; use `MainActor.assumeIsolated` for temporary dynamic isolation (use only as a stopgap); `await MainActor.run` helps during migration but is no substitute for static `@MainActor`; mark public types `@preconcurrency @MainActor` to stay source compatible with clients not yet checking; `@preconcurrency` also helps with non-Sendable types and protocol-conformance isolation mismatches from unmigrated dependencies.

Gotcha: a callback from an unmigrated module missing `@Sendable` can get wrong inferred `MainActor` isolation, compiling cleanly but crashing at runtime. Annotate the closure `@Sendable` at the call site, or report it to the library maintainer.

Verify: `swift build -Xswiftc -strict-concurrency=complete` reports no warnings, then switch the language mode to 6 and rebuild.

## Checked
2026-11-08: read in full the Swift migration guide pages Migrating to Swift 6, Migration Strategy, Enable data-race safety checking and Incremental Adoption (swiftlang/swift-migration-guide, Guide.docc). Removed: the swift.org blog source and Swift 6.0 release date (not read), the `ExistentialAny` flag example, the minimal/targeted/complete ordering claim, the leaf-first module-order advice (the guide says begin from the outside), and the `nonisolated(unsafe)` advice (the Common Problems page was not read).
Method: documentation only; no commands were run.
