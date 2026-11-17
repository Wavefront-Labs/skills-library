---
id: computing-software.software-engineering.objective-c.xcframework
name: xcframework
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-packaging, xcframework]
level: advanced
status: draft
description: "Package a binary Objective-C library for several platforms into an XCFramework with xcodebuild -create-xcframework."
sources:
  - https://developer.apple.com/documentation/xcode
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# XCFramework
**Goal:** distribute one binary for device, simulator and Mac slices.

```bash
xcodebuild archive -scheme ABCKit -destination 'generic/platform=iOS' -archivePath build/ios SKIP_INSTALL=NO BUILD_LIBRARY_FOR_DISTRIBUTION=YES
xcodebuild archive -scheme ABCKit -destination 'generic/platform=iOS Simulator' -archivePath build/sim SKIP_INSTALL=NO BUILD_LIBRARY_FOR_DISTRIBUTION=YES
xcodebuild -create-xcframework \
  -framework build/ios.xcarchive/Products/Library/Frameworks/ABCKit.framework \
  -framework build/sim.xcarchive/Products/Library/Frameworks/ABCKit.framework \
  -output build/ABCKit.xcframework
```
- For static libraries use `-library libABCKit.a -headers include/`.
- Each platform needs its own slice; device and simulator arm64 cannot share one fat binary, which is why XCFrameworks exist.
- Distribute via SwiftPM `.binaryTarget(name:path:)` or `.binaryTarget(name:url:checksum:)` (checksum from `swift package compute-checksum`).
- Sign xcframeworks with `codesign` for release.
- `BUILD_LIBRARY_FOR_DISTRIBUTION=YES` matters for Swift module stability; for pure Objective-C it is harmless.

## Gotchas
- Archive destinations must match the slices you want to include.
- Headers must be public and self-contained.

## Self-check
Add the XCFramework to a clean app on both simulator and device builds.
