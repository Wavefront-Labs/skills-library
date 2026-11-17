---
id: computing-software.software-engineering.swift.swift-objc-interop
name: swift-objc-interop
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-interop, objc-interop]
level: advanced
status: draft
description: "Expose Swift to Objective-C with @objc and call C APIs, handling nullability and bridging."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Objective-C and C interop
- `@objc` / `@objcMembers` and `NSObject` subclassing expose members to Objective-C; bridging header or module map imports C/ObjC to Swift.
- ObjC nullability annotations (`_Nullable`, `NS_ASSUME_NONNULL`) become Swift optionals; unannotated imports as implicitly unwrapped.
- C pointers: `UnsafePointer`, `withUnsafeBytes`; keep pointers valid only inside closure scope.
Verify: build with Strict memory checks in Debug (Address Sanitizer).
