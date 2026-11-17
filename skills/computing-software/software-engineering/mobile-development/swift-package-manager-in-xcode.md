---
id: computing-software.software-engineering.mobile-development.swift-package-manager-in-xcode
name: swift-package-manager-in-xcode
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, ios, swift-package-manager, spm, package-swift, package-resolved, xcframework, modularization]
level: practitioner
status: draft
description: "Use Swift Package Manager in Xcode projects: add dependencies, pin with Package.resolved, write local packages for modularity, and resolve common SPM errors."
sources: ["https://www.swift.org/documentation/package-manager/", "https://developer.apple.com/documentation/xcode/adding-package-dependencies-to-your-app", "https://docs.swift.org/package-manager/PackageDescription/PackageDescription.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Swift Package Manager in Xcode

## Add a dependency
Xcode: File > Add Package Dependencies, enter the Git URL, choose a rule (Up to Next Major, Exact, Branch, Commit). Exact resolved commits are stored in `Package.resolved` inside the xcodeproj/xcworkspace; commit that file for reproducible builds.

## Local feature package (modularisation)
```swift
// swift-tools-version: 5.9
import PackageDescription
let package = Package(
    name: "Features",
    platforms: [.iOS(.v16)],
    products: [.library(name: "Profile", targets: ["Profile"])],
    dependencies: [.package(url: "https://github.com/pointfreeco/swift-dependencies", from: "1.0.0")],
    targets: [
        .target(name: "Profile", dependencies: [.product(name: "Dependencies", package: "swift-dependencies")]),
        .testTarget(name: "ProfileTests", dependencies: ["Profile"])
    ]
)
```
Drag the folder into the project (File > Add Files > local package) and link the product to the app target.

## CLI
```bash
swift package resolve
swift package update            # re-resolves within version rules
xcodebuild -resolvePackageDependencies -project App.xcodeproj -scheme App
```

## Gotchas
- Make types `public` explicitly; a package's default access is internal.
- Binary targets (`.binaryTarget(url:checksum:)`) need the checksum from `swift package compute-checksum`.
- CI: cache `~/Library/Developer/Xcode/DerivedData` and SourcePackages, and use `-disableAutomaticPackageResolution` with a committed `Package.resolved` for deterministic runs.
- Resolution failures after a force-pushed tag: clear caches with File > Packages > Reset Package Caches.

Verify: clean-clone the repo, run `xcodebuild -resolvePackageDependencies` then a build; the diff of `Package.resolved` afterwards must be empty.
