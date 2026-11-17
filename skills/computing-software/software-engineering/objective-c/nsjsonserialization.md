---
id: computing-software.software-engineering.objective-c.nsjsonserialization
name: nsjsonserialization
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-foundation-data, nsjsonserialization]
level: practitioner
status: draft
description: "Parse and generate JSON using NSJSONSerialization with options, error handling and defensive type checks on id results."
sources:
  - https://developer.apple.com/documentation/foundation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NSData and JSON
**Goal:** convert between bytes, JSON and model objects safely.

```objc
NSError *err = nil;
id obj = [NSJSONSerialization JSONObjectWithData:data options:NSJSONReadingMutableContainers error:&err];
if (!obj) { NSLog(@"parse: %@", err); return; }
if (![obj isKindOfClass:[NSDictionary class]]) return;
NSString *name = [obj[@"name"] isKindOfClass:[NSString class]] ? obj[@"name"] : nil;

NSData *out = [NSJSONSerialization dataWithJSONObject:@{@"a": @1} options:NSJSONWritingPrettyPrinted error:&err];
```
- Top-level can be array or dictionary; `NSJSONReadingFragmentsAllowed` permits scalars.
- Check `[NSJSONSerialization isValidJSONObject:obj]` before writing (only NSString, NSNumber, NSArray, NSDictionary, NSNull; dictionary keys must be strings; no NaN/Inf).
- JSON null decodes to `NSNull`, not nil; numbers decode to NSNumber, so check types before using.
- Dates and decimals need custom conversion (ISO 8601 string via `NSISO8601DateFormatter`).
- For NSData: `dataWithContentsOfURL:options:error:`, `writeToURL:options:error:`, `base64EncodedStringWithOptions:`, `subdataWithRange:`.

## Gotchas
- Server-supplied JSON is untrusted: never `valueForKey:` blindly or cast without checks.
- Large payloads: parse off the main thread.

## Self-check
Feed `{"a":null}` and confirm `NSNull` handling.
