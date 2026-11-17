---
id: computing-software.web-development.vapor.vapor-package-manifest-spm
name: vapor-package-manifest-spm
category: computing-software
field: web-development
product: vapor
tags: [vapor, package-swift, swiftpm, spm, dependencies, targets, package-resolved, manifest]
level: practitioner
status: docs-checked
description: "Read and edit a Vapor Package.swift: tools version, platforms, vapor dependency, targets, Package.resolved and updating dependencies."
sources:
  - https://docs.vapor.codes/getting-started/spm/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: understand and modify a Vapor project's SwiftPM manifest.

```swift
// swift-tools-version:5.8
import PackageDescription

let package = Package(
    name: "MyApp",
    platforms: [
       .macOS(.v12)
    ],
    dependencies: [
        .package(url: "https://github.com/vapor/vapor.git", from: "4.76.0"),
    ],
    targets: [
        .executableTarget(
            name: "App",
            dependencies: [
                .product(name: "Vapor", package: "vapor")
            ]
        ),
        .testTarget(name: "AppTests", dependencies: [
            .target(name: "App"),
            .product(name: "XCTVapor", package: "vapor"),
        ])
    ]
)
```

- Manifest must be named `Package.swift` in the project root. SPM has no central index: dependencies are Git URLs versioned by Git tags.
- First line = minimum Swift tools version; it also tells Swift how to parse the manifest.
- Package name: for a public package use the last segment of the Git URL.
- `platforms`: `.macOS(.v12)` requires macOS 12+, and Xcode sets that deployment target.
- `dependencies`: all Vapor apps need the vapor package. After adding a package, also list its products in the targets that use them; module names must be in a target's dependencies before you can import them.
- Targets: most Vapor apps have two (app + tests). Each `.target`/`.executableTarget` maps to a folder under `Sources`, each `.testTarget` to one under `Tests`. Targets may depend on other targets or on package products.
- `Package.resolved` is created on first build and pins versions; later builds reuse them. Update with `swift package update`.
- Xcode 11+ picks up manifest changes automatically; update via File > Swift Packages > Update To Latest Swift Package Versions. Consider adding `.swiftpm` to `.gitignore` (Xcode stores its project configuration there).

## Checked

2026-11-08: read in full the Swift Package Manager page at docs.vapor.codes/getting-started/spm/ (manifest example, tools version, platforms, targets, Package.resolved, Xcode notes). Every claim was found on the cited pages; nothing needed removing.

Method: docs-only read of cited pages, 2026-11-08
