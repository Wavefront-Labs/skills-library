---
id: computing-software.software-engineering.objective-c.nsstring-basics
name: nsstring-basics
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-foundation-text, nsstring-basics]
level: intro
status: draft
description: "Create, compare, search, split and edit strings using NSString and NSMutableString with correct encoding and locale handling."
sources:
  - https://developer.apple.com/documentation/foundation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NSString basics
**Goal:** the string operations used daily.

```objc
NSString *s = @"Hello, World";
NSRange r = [s rangeOfString:@"World" options:NSCaseInsensitiveSearch];
if (r.location != NSNotFound) { NSString *tail = [s substringFromIndex:NSMaxRange(r)]; }
NSArray *parts = [s componentsSeparatedByString:@", "];
NSString *joined = [parts componentsJoinedByString:@"-"];
BOOL eq = [s isEqualToString:other];
NSString *trim = [s stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]];
NSMutableString *m = [NSMutableString stringWithString:s]; [m appendString:@"!"];
NSData *utf8 = [s dataUsingEncoding:NSUTF8StringEncoding];
```
- `length` counts UTF-16 code units, not user-visible characters; use `rangeOfComposedCharacterSequenceAtIndex:` for emoji/combining marks.
- Compare with `isEqualToString:`; order with `compare:options:range:locale:`; use `localizedStandardCompare:` for user-facing sorting.
- Case: `lowercaseString` is locale-independent; use `localizedLowercaseString` for UI text.
- `containsString:` (iOS 8+/macOS 10.10+), `hasPrefix:`/`hasSuffix:`.
- File paths: use NSURL/`stringByAppendingPathComponent:` rather than manual `/`.

## Gotchas
- `substringToIndex:` beyond length raises `NSRangeException`.
- `[NSString stringWithFormat:@"%@", nil-object]` prints "(null)".

## Self-check
Test with "é" and an emoji to confirm length versus composed characters.
