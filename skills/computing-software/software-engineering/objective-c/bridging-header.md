---
id: computing-software.software-engineering.objective-c.bridging-header
name: bridging-header
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-swift-interop, bridging-header]
level: practitioner
status: draft
description: "Expose Objective-C to Swift with a bridging header or umbrella header and Swift to Objective-C with the generated -Swift.h header."
sources:
  - https://developer.apple.com/documentation/swift
  - https://developer.apple.com/documentation/xcode
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bridging header and generated header
**Goal:** call across the Swift/Objective-C boundary in an app or framework target.

- App target: set build setting `SWIFT_OBJC_BRIDGING_HEADER` to a header such as `<project>/App-Bridging-Header.h` and `#import` the Objective-C headers Swift should see.
- Framework target: Swift sees public headers listed in the umbrella header (`<Framework>/<Framework>.h`); bridging headers are not supported in frameworks.
- Swift to Objective-C: in a .m file `#import "<ProductModuleName>-Swift.h"` (app) or `#import <Framework/Framework-Swift.h>` (framework). The header is generated at build time (`SWIFT_INSTALL_OBJC_HEADER` / "Objective-C Generated Interface Header Name").
```objc
#import "MyApp-Swift.h"
SwiftThing *t = [[SwiftThing alloc] initWithName:@"x"];
```
- Only Swift declarations marked `@objc` (or classes inheriting NSObject with `@objcMembers`) appear in the generated header.
- In headers, use `@class SwiftThing;` forward declarations, and import `-Swift.h` only in .m files to avoid cycles.

## Gotchas
- Swift structs, enums with associated values and generics are not visible to Objective-C.
- Product module name with spaces/hyphens is mangled to underscores in the header name.

## Self-check
Build a mixed target and call one method in each direction.
