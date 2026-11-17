---
id: computing-software.software-engineering.objective-c.spm-objc-targets
name: spm-objc-targets
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-packaging, spm-objc-targets]
level: practitioner
status: draft
description: "Package Objective-C code with SwiftPM using a C-language target, include/ public headers and publicHeadersPath."
sources:
  - https://www.swift.org/package-manager/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SwiftPM Objective-C targets
**Goal:** ship an Objective-C library as a package.

```
Sources/ABCKit/ABCThing.m
Sources/ABCKit/include/ABCThing.h        // public headers only
Package.swift
```
```swift
// swift-tools-version:5.9
import PackageDescription
let package = Package(
  name: "ABCKit",
  platforms: [.iOS(.v15), .macOS(.v12)],
  products: [.library(name: "ABCKit", targets: ["ABCKit"])],
  targets: [
    .target(name: "ABCKit", path: "Sources/ABCKit", publicHeadersPath: "include",
            cSettings: [.headerSearchPath("Private")]),
    .testTarget(name: "ABCKitTests", dependencies: ["ABCKit"])
  ]
)
```
- A target is C-family if its sources are .c/.m/.cpp/.mm; SwiftPM generates a module map from the `include` directory (it can generate an umbrella header named after the target when it exists).
- A single target cannot mix Swift and Objective-C sources; split into two targets.
- ARC is on by default for SwiftPM Objective-C targets (unconfirmed for every tools version; add `.unsafeFlags(["-fobjc-arc"])` only if needed, noting unsafeFlags block use as a dependency).
- Link system frameworks automatically through modules; add `.linkedFramework("Foundation")` in `linkerSettings` if needed.
- Commands: `swift build`, `swift test`, `swift package resolve`.

## Gotchas
- Headers outside `include` are not public.
- `unsafeFlags` disqualifies a package from being a dependency of others.

## Self-check
Create a Swift client package depending on it and import the Objective-C module.
