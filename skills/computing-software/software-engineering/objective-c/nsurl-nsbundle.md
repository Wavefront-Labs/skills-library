---
id: computing-software.software-engineering.objective-c.nsurl-nsbundle
name: nsurl-nsbundle
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-foundation-io, nsurl-nsbundle]
level: practitioner
status: draft
description: "Build and parse URLs with NSURL and NSURLComponents and load bundled resources with NSBundle, including test bundles."
sources:
  - https://developer.apple.com/documentation/foundation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NSURL and NSBundle
**Goal:** construct URLs safely and locate resources.

```objc
NSURLComponents *c = [NSURLComponents componentsWithString:@"https://example.com/search"];
c.queryItems = @[[NSURLQueryItem queryItemWithName:@"q" value:@"a b&c"]];   // encodes values
NSURL *url = c.URL;
NSURL *res = [[NSBundle mainBundle] URLForResource:@"config" withExtension:@"json"];
NSString *ver = [[NSBundle mainBundle] objectForInfoDictionaryKey:@"CFBundleShortVersionString"];
NSBundle *tb = [NSBundle bundleForClass:[self class]];     // inside XCTest, not mainBundle
```
- Build query strings with `NSURLComponents` / `NSURLQueryItem` rather than string concatenation.
- `stringByAddingPercentEncodingWithAllowedCharacters:` needs the correct set (`URLQueryAllowedCharacterSet` does not encode `&` or `+`; encode values by hand or use query items).
- `[NSURL URLWithString:]` returns nil for invalid strings; check.
- File URLs: `fileURLWithPath:`; resource keys via `getResourceValue:forKey:error:`.
- Localized resources resolve through `.lproj` folders automatically.

## Gotchas
- `mainBundle` in unit tests is the test host or xctest runner, not your framework; use `bundleForClass:`.
- Missing resource returns nil, not an error.

## Self-check
Round-trip a URL with spaces and ampersands and confirm the server sees the original value.
