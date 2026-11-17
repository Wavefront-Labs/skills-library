---
id: computing-software.software-engineering.swift.swift-package-manifest
name: swift-package-manifest
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-spm, package-manifest]
level: practitioner
status: docs-checked
description: "Write Package.swift with targets, dependencies, tools version and resolution."
sources: ["https://github.com/swiftlang/swift-package-manager/blob/main/Sources/PackageManagerDocs/Documentation.docc/CreatingSwiftPackage.md", "https://github.com/swiftlang/swift-package-manager/blob/main/Sources/PackageManagerDocs/Documentation.docc/Dependencies/AddingDependencies.md", "https://github.com/swiftlang/swift-package-manager/blob/main/Sources/PackageManagerDocs/Documentation.docc/ResolvingPackageVersions.md", "https://github.com/swiftlang/swift-package-manager/blob/main/Sources/PackageManagerDocs/Documentation.docc/SettingSwiftToolsVersion.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Package.swift manifest and dependencies
- A package is a directory with sources and a `Package.swift` manifest at its root, itself written in Swift using `PackageDescription`. `swift package init` creates a library layout (sources under `Sources/<target>`, tests under `Tests/<target>`); `--type executable` creates a "Hello World" executable, `--type tool` an argument-parser command-line tool, `--type macro` a macro package.
- The comment `// swift-tools-version:6.1` declares the minimum Swift compiler version and how the manifest is parsed. It conventionally sits on the first line, and must when the version is earlier than 6.0. The patch version defaults to `0`. A dependency whose tools version is newer than yours is ineligible and resolution tries the next-best version; `swift package tools-version` reports or sets it.
- Target kinds seen in the docs: `.target`, `.executableTarget`, `.testTarget`, `.macro`, `.plugin`, `.binaryTarget`.

```swift
// swift-tools-version:6.1
import PackageDescription
let package = Package(
    name: "MyPackage",
    dependencies: [
        .package(url: "https://github.com/apple/example-package-playingcard.git", from: "4.0.0"),
    ],
    targets: [
        .target(name: "MyPackage", dependencies: [
            .product(name: "PlayingCard", package: "example-package-playingcard")]),
        .testTarget(name: "MyPackageTests", dependencies: ["MyPackage"]),
    ]
)
```

- `from: "4.0.0"` accepts that version up to the next major version. A version requirement can be a range, a specific version, a branch name or a commit hash. Versions come from git tags read as semantic versions; tags need all three components (major, minor, patch).
- Local dependencies (`package(path:)`) enforce no version constraint and use whatever is at the path.
- `Package.resolved` records resolution results. It pins versions only for the top-level (leaf) package; a library's `Package.resolved` is ignored when it is resolved as someone's dependency. Keep it in source control for apps to coordinate versions. `swift package resolve --force-resolved-versions` uses the recorded versions; `swift package update` moves to the latest eligible versions and rewrites it.
- `swift run` and `swift build` resolve automatically.

Gotcha: a `.testTarget` cannot depend on another `.testTarget`; put shared code in a non-test target.

Verify: `swift package resolve`, then `swift build` and `swift test`.

## Checked
2026-11-08: read in full the SwiftPM docs pages Creating a Swift package, Adding dependencies to a Swift package, Resolving and updating dependencies and Setting the Swift tools version (swift-package-manager repository, PackageManagerDocs source). Removed: `.upToNextMinor(from:)` and `exact` method names and the claim about branch/revision dependencies of released packages (API reference not read), the `platforms` claim, the advice that libraries usually do not commit `Package.resolved` beyond what the page says, and the landing-page sources.
Method: documentation only; no commands were run.
